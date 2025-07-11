# PubMed Paper Fetcher

Command-line tool to fetch PubMed research papers that include at least one non-academic author affiliated with a pharmaceutical or biotech company.

## ✅ Features

- Search any PubMed query using full syntax
- Parse author affiliations
- Filter non-academic authors (e.g., pharma/biotech companies)
- Save results as CSV

## 📦 Output CSV Columns

- PubmedID
- Title
- Publication Date
- Non-academic Author(s)
- Company Affiliation(s)
- Corresponding Author Email

## 🛠 Usage

```bash
python fetch_pubmed.py "covid vaccine" -f results.csv -d
