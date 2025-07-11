import argparse
from .fetcher import search_pubmed, fetch_details, parse_papers, save_to_csv

def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors from pharma/biotech.")
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("-f", "--file", help="CSV file to save results")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    ids = search_pubmed(args.query)
    if args.debug:
        print(f"[DEBUG] Fetched PubMed IDs: {ids}")

    xml_data = fetch_details(ids)
    rows = parse_papers(xml_data)

    if args.file:
        save_to_csv(rows, args.file)
        print(f"[INFO] Results saved to {args.file}")
    else:
        for row in rows:
            print(row)
