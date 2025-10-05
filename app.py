# -*- coding: utf-8 -*-
# Full backend + Flask wrapper

# ------------------------
# IMPORTS
# ------------------------
import httpx
import asyncio
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import re
import json
from urllib.parse import quote
from gensim import corpora, models, similarities
from flask import Flask, request, jsonify, render_template, send_from_directory
import nest_asyncio
nest_asyncio.apply()

# ------------------------
# INITIALIZE NLP
# ------------------------
spacy_nlp = spacy.load('en_core_web_sm')
punctuations = string.punctuation
stop_words = STOP_WORDS

# ------------------------
# BACKEND FUNCTIONS
# ------------------------

async def query_osdr_api_with_keywords(query):
    """Query OSDR API"""
    base_url = "https://osdr.nasa.gov/osdr/data/search"
    keyword = quote(query)
    url = f"{base_url}?term={keyword}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        data = json.loads(response.text)
    records = data["hits"]["hits"]
    df = pd.json_normalize(records, sep="_")
    return df

def spacy_tokenizer(sentence):
    """Text preprocessing and tokenization"""
    sentence = re.sub(r'\'','',sentence)
    sentence = re.sub(r'\w*\d\w*','',sentence)
    sentence = re.sub(r' +',' ',sentence)
    sentence = re.sub(r'\n: \'\'.*','',sentence)
    sentence = re.sub(r'\n!.*','',sentence)
    sentence = re.sub(r'^:\'\'.*','',sentence)
    sentence = re.sub(r'\n',' ',sentence)
    sentence = re.sub(r'[^\w\s]',' ',sentence)
    tokens = spacy_nlp(sentence)
    tokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]
    return tokens

def study_tokenizer(df):
    df["Study_Description_tokenized"] = df["_source_Study Description"].astype(str).map(lambda x: spacy_tokenizer(x))
    df["Study_Title_tokenized"] = df["_source_Study Title"].astype(str).map(lambda x: spacy_tokenizer(x))
    study_description = df['Study_Description_tokenized']
    study_title = df['Study_Title_tokenized']
    return study_description, study_title

def dictionaries(study_description, study_title):
    describe_dictionary = corpora.Dictionary(study_description)
    title_dictionary = corpora.Dictionary(study_title)
    stoplist = set('hello and if this can would should could tell ask stop come go')
    describe_stop_ids = [describe_dictionary.token2id[stopword] for stopword in stoplist if stopword in describe_dictionary.token2id]
    describe_dictionary.filter_tokens(describe_stop_ids)
    title_stop_ids = [title_dictionary.token2id[stopword] for stopword in stoplist if stopword in title_dictionary.token2id]
    title_dictionary.filter_tokens(title_stop_ids)
    return describe_dictionary, title_dictionary

def search_similar_study_titles(search_term, title_dictionary, title_tfidf_model, title_lsi_model, study_title_index, df):
    query_bow = title_dictionary.doc2bow(spacy_tokenizer(search_term))
    query_tfidf = title_tfidf_model[query_bow]
    query_lsi = title_lsi_model[query_tfidf]
    study_title_index.num_best = 5
    study_title_list = study_title_index[query_lsi]
    study_title_list.sort(key=lambda x: x[1], reverse=True)
    study_title_names = []
    osdr_base_url = "https://osdr.nasa.gov/bio/repo/data/studies/"
    ebi_pride_base_url = "https://www.ebi.ac.uk/pride/archive/projects/"
    nih_base_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="
    mg_rast_base_url = "https://www.mg-rast.org/mgmain.html?mgpage=project&project="
    for j, study in enumerate(study_title_list):
        study_ID = df['_source_Accession'][study[0]]
        if df['_source_Data Source Type'][study[0]] == 'ebi_pride':
            base_url = ebi_pride_base_url
        elif df['_source_Data Source Type'][study[0]] == 'nih_geo_gse':
            base_url = nih_base_url
        elif df['_source_Data Source Type'][study[0]] == 'mg_rast':
            base_url = mg_rast_base_url
        else:
            base_url = osdr_base_url
        study_title_names.append({
            'Relevance': round((study[1] * 100),2),
            'study Title': df['_source_Study Title'][study[0]],
            'study description': df['_source_Study Description'][study[0]],
            'study ID': df['_source_Accession'][study[0]],
            'study URL': f"{base_url}{study_ID}"
        })
        if j == (study_title_index.num_best-1):
            break
    return pd.DataFrame(study_title_names, columns=['Relevance','study ID','study Title','study URL','study description'])

# ------------------------
# FLASK APP
# ------------------------
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/semantic-search", methods=["GET"])
def semantic_search():
    search_term = request.args.get("query", "")
    if not search_term:
        return jsonify({"error": "No query provided"}), 400
    try:
        studies = asyncio.run(query_osdr_api_with_keywords(search_term))
        study_description, study_title = study_tokenizer(studies)
        describe_dictionary, title_dictionary = dictionaries(study_description, study_title)
        describe_corpus = [describe_dictionary.doc2bow(desc) for desc in study_description]
        title_corpus = [title_dictionary.doc2bow(desc) for desc in study_title]

        title_tfidf_model = models.TfidfModel(title_corpus, id2word=title_dictionary)
        title_lsi_model = models.LsiModel(title_tfidf_model[title_corpus], id2word=title_dictionary, num_topics=300)
        study_title_index = similarities.MatrixSimilarity(title_lsi_model[title_corpus], num_features=title_lsi_model.num_topics)

        results_df = search_similar_study_titles(
            search_term,
            title_dictionary,
            title_tfidf_model,
            title_lsi_model,
            study_title_index,
            studies
        )
        return results_df.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/styles.css")
def styles():
    return send_from_directory("static", "styles.css")

@app.route("/script.js")
def script():
    return send_from_directory("static", "script.js")

if __name__ == "__main__":
    app.run(debug=True)


