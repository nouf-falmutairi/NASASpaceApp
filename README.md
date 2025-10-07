# NASASpaceApp

**A Semantic Search Tool for NASA Datasets**  
Built for the **2025 NASA Space Apps Challenge**, NASASpaceApp helps users discover the most relevant NASA research studies using natural language queries.

---

## 🚀 Overview

NASASpaceApp is a web application that leverages **NLP and machine learning** to perform semantic search over NASA datasets. Users can enter a query in plain English, and the app retrieves the **top 5 relevant studies** from multiple data sources including NASA OSDR, EBI PRIDE, NIH GEO, and MG-RAST.

The project aligns with the **2025 Space Apps Challenge theme: "Learn, Launch, Lead"** by transforming open data into actionable insights and making NASA research more accessible.

---

## 🌟 Features

- **Semantic Search**: Find relevant studies using natural language queries.
- **NLP Preprocessing**: Tokenization, lemmatization, and stop-word removal with **spaCy**.
- **Similarity Ranking**: TF-IDF & LSI models identify the most semantically relevant studies.
- **Interactive Web Interface**: Built with **Flask**, serving HTML, CSS, and JavaScript.
- **Multi-Source Dataset Links**: Direct links to NASA OSDR, EBI PRIDE, NIH GEO, MG-RAST.
- **Error Handling**: Graceful handling of missing queries or API errors.

---

## 🛠️ Technologies Used

- **Backend**: Python, Flask, asyncio, httpx  
- **NLP & Machine Learning**: spaCy, Gensim, TF-IDF, LSI  
- **Data Handling**: Pandas, JSON  
- **Frontend**: HTML, CSS, JavaScript  

---

## 📂 Repository Structure

```

NASASpaceApp/
│
├── app.py                 # Main backend and Flask app
├── templates/             # HTML templates
├── static/                # CSS and JS files
├── requirements.txt       # Python dependencies
├── setup.py               # Setup script for installation
└── .github/               # GitHub workflows (optional)

````

---

## 🔧 How It Works

1. User enters a search term in the web interface.  
2. The app queries the **NASA OSDR API** to fetch relevant study data.  
3. Titles and descriptions are tokenized and preprocessed with NLP.  
4. TF-IDF and LSI models rank studies based on semantic similarity.  
5. Top 5 studies are returned with direct links to their source datasets.  

---

## 📈 Impact

NASASpaceApp simplifies access to NASA research, making it easier for **students, researchers, and space enthusiasts** to explore and use scientific data effectively.

---

## ⚡ Getting Started

1. Clone the repository:  
```bash
git clone https://github.com/nouf-falmutairi/NASASpaceApp.git
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

4. Open your browser at `http://127.0.0.1:5000/`

---
## ⚡ perview

Website recording: 
**https://drive.google.com/file/d/1PaLGwDmPtxo4ciEhl4l_kyPDGETm4xQW/view**

slideshow :
**https://docs.google.com/presentation/d/1Vb9BE51q78c989uyVYyyjFZSMaxzUAaD/edit?slide=id.p1#slide=id.p1**

## 📄 License

This project is open-source.

---

## 🌐 NASA Space Apps Challenge

Learn more about the **2025 NASA Space Apps Challenge**: [https://www.nasa.gov/nasa-space-apps-challenge-2025](https://www.nasa.gov/nasa-space-apps-challenge-2025)

