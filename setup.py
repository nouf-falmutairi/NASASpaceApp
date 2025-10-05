from setuptools import setup, find_packages

setup(
    name="nasa_study_search",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask",
	"serverless-wsgi",
        "httpx",
        "pandas",
        "spacy",
		"scipy",
        "gensim"
    ],
    entry_points={
        "console_scripts": [
            "nasa-app=app:app",
        ],
    },
)

