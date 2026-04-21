import requests
import xml.etree.ElementTree as ET
import pandas as pd

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query="PCOS risk factors", retmax=10):
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json"
    }

    response = requests.get(BASE_URL + "esearch.fcgi", params=params)
    data = response.json()

    return data["esearchresult"]["idlist"]


def fetch_pubmed_details(id_list):
    if not id_list:
        return pd.DataFrame(columns=["pmid", "title", "year", "abstract", "keywords", "risk_factors"])

    params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    }

    response = requests.get(BASE_URL + "efetch.fcgi", params=params)
    root = ET.fromstring(response.content)

    articles = []

    # simple list of risk factors to search for
    risk_terms = [
        "insulin resistance",
        "obesity",
        "hormonal imbalance",
        "androgen",
        "inflammation",
        "genetics",
        "lifestyle",
        "diet",
        "stress"
    ]

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        year = article.findtext(".//PubDate/Year")

        abstract_parts = article.findall(".//AbstractText")
        abstract = " ".join([part.text for part in abstract_parts if part.text]) if abstract_parts else ""

        keyword_elems = article.findall(".//Keyword")
        keywords = ", ".join([kw.text for kw in keyword_elems if kw.text]) if keyword_elems else ""

        found_risks = []
        abstract_lower = abstract.lower()

        for term in risk_terms:
            if term in abstract_lower:
                found_risks.append(term)

        articles.append({
            "pmid": pmid,
            "title": title,
            "year": year,
            "abstract": abstract,
            "keywords": keywords,
            "risk_factors": ", ".join(found_risks)
        })

    return pd.DataFrame(articles)

if __name__ == "__main__":
    ids = search_pubmed(query="PCOS risk factors", retmax=50)
    df = fetch_pubmed_details(ids)

    print("PubMed data loaded successfully.")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nNumber of papers with at least one detected risk factor:")
    print((df["risk_factors"] != "").sum())

    print("\nMost common detected risk factors:")
    risk_counts = (
        df["risk_factors"]
        .str.split(", ")
        .explode()
        .replace("", pd.NA)
        .dropna()
        .value_counts()
    )
    print(risk_counts.head(10))