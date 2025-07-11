import argparse
import urllib.request
import xml.etree.ElementTree as ET
import csv
import json
import re

PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query: str, retmax: int = 10) -> list[str]:
    url = f"{PUBMED_SEARCH}?db=pubmed&term={query}&retmode=json&retmax={retmax}"
    with urllib.request.urlopen(url) as response:
        result = json.load(response)
        return result["esearchresult"]["idlist"]

def fetch_details(pubmed_ids: list[str]) -> bytes:
    ids = ",".join(pubmed_ids)
    url = f"{PUBMED_FETCH}?db=pubmed&id={ids}&retmode=xml"
    with urllib.request.urlopen(url) as response:
        return response.read()

def parse_papers(xml_data: bytes) -> list[list[str]]:
    root = ET.fromstring(xml_data)
    results = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle") or "No Title"
        pub_date = article.findtext(".//PubDate/Year") or "Unknown"
        email = "N/A"
        authors = []
        companies = []

        for author in article.findall(".//Author"):
            affil = author.findtext(".//AffiliationInfo/Affiliation")
            if affil:
                if "@" in affil and email == "N/A":
                    match = re.search(r"[\w\.-]+@[\w\.-]+", affil)
                    if match:
                        email = match.group()
                if any(word in affil.lower() for word in ["pharma", "biotech", "inc", "ltd", "therapeutics", "laboratories"]):
                    name = f"{author.findtext('ForeName') or ''} {author.findtext('LastName') or ''}".strip()
                    authors.append(name)
                    companies.append(affil)

        if authors:
            results.append([pmid, title, pub_date, "; ".join(authors), "; ".join(companies), email])
    return results

def save_to_csv(data: list[list[str]], filename: str):
    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="PubMed Paper Fetcher")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-f", "--file", help="CSV filename to save results")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug prints")
    args = parser.parse_args()

    ids = search_pubmed(args.query)
    if args.debug:
        print(f"[DEBUG] Fetched IDs: {ids}")

    xml_data = fetch_details(ids)
    rows = parse_papers(xml_data)

    if args.file:
        save_to_csv(rows, args.file)
        print(f"[INFO] Results saved to {args.file}")
    else:
        for row in rows:
            print(row)

if __name__ == "__main__":
    main()
