import json
from urllib.request import urlopen, Request
from urllib.parse import quote
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Load data
with open("extracted_database.json", "r") as f:
    data = json.load(f)

# SNOMED API configuration for related terms
baseUrl = 'https://browser.ihtsdotools.org/snowstorm/snomed-ct'
edition = 'MAIN'
version = '2024-10-01'
user_agent = 'manucianhh@gmail.com'

def urlopen_with_header(url):
    req = Request(url)
    req.add_header('User-Agent', user_agent)
    return urlopen(req)

def getSnomedCode(searchTerm):
    url = f"{baseUrl}/browser/{edition}/{version}/descriptions?term={quote(searchTerm)}&conceptActive=true&groupByConcept=false&searchMode=STANDARD&offset=0&limit=50"
    response = urlopen_with_header(url).read()
    data = json.loads(response.decode('utf-8'))

    for term in data['items']:
        if searchTerm.lower() == term['term'].lower():
            return term['concept']['conceptId']

def getConceptById(concept_id):
    url = f"{baseUrl}/browser/{edition}/{version}/concepts/{concept_id}"
    response = urlopen_with_header(url).read()
    return json.loads(response.decode('utf-8'))

def getRelatedTerms(concept):
    terms = []
    for item in concept['descriptions']:
        if item['active']:
            terms.append(item['term'])
    return terms

def finetuneTerms(originalTerm, relatedTerms):
    terms = []
    for term in relatedTerms:
        if (originalTerm.lower() != term.lower()) and  ("(" not in term):
            terms.append(term)
    return terms

# Route for the home page (index)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        originalTerm = request.form["search_term"]
        id = getSnomedCode(originalTerm)
        concept = getConceptById(id)
        relatedTerms = getRelatedTerms(concept)
        relatedTerms = finetuneTerms(originalTerm, relatedTerms)

        # Select Candidates
        candidates = []
        for item in data:
            if (item["definition"] != "Definition not found"):
                if (originalTerm.lower().strip() in item["term"].lower().strip()):
                    candidates.append(item)
                else:
                    for term in relatedTerms:
                        if (term.lower().strip() in item["term"].lower().strip()):
                            candidates.append(item)
                            break

        # Extract definitions for similarity computation
        definitions = [entry["definition"] for entry in candidates]

        # Create a TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([originalTerm] + definitions)

        # Calculate cosine similarity between the medical term and each definition
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Add cosine similarity scores to the dataset and rank
        for i, entry in enumerate(candidates):
            entry["cosine_similarity"] = similarities[i]

        # Sort data by similarity
        ranked_results = sorted(candidates, key=lambda x: x["cosine_similarity"], reverse=True)

        # Add numerical order column
        for index, entry in enumerate(ranked_results, start=1):
            entry["rank"] = index

        # Convert to pandas DataFrame for better display
        df = pd.DataFrame(ranked_results, columns=["rank", "term", "definition", "symptoms", "diagnosis", "treatment", "risk_factors", "cosine_similarity"])

        # Render the results page with the data
        return render_template("index.html", originalTerm=originalTerm, relatedTerms=relatedTerms, df=df.head(20))

    return render_template("index.html", originalTerm=None, relatedTerms=None, df=None)

if __name__ == "__main__":
    app.run(debug=True)
