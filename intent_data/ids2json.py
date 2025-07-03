#!/usr/bin/env python3
import csv
import json
import argparse
import sys

def extract_fields(csv_path):
    """
    Reads a CSV file with headers and extracts 'id', 'intent_name' and 'scope'
    from each row. Returns a list of dicts.
    """
    records = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # ensure required columns exist
            for field in ('id', 'intent_name', 'scope'):
                if field not in reader.fieldnames:
                    print(f"Error: Missing required column '{field}' in CSV.", file=sys.stderr)
                    sys.exit(1)

            for row in reader:
                records.append({
                    "id": row["id"].strip(),
                    "intent_name": row["intent_name"].strip(),
                    "scope": row["scope"].strip()
                })
    except FileNotFoundError:
        print(f"Error: File not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        sys.exit(1)

    return records

def write_to_json(data, json_path):
    """
    Writes the list of dicts to json_path with indentation.
    """
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Extract 'id', 'intent_name', and 'scope' from a CSV into a JSON file."
    )
    parser.add_argument('csv_input', help="Path to the input CSV file")
    parser.add_argument('json_output', help="Path to the output JSON file")
    args = parser.parse_args()

    data = extract_fields(args.csv_input)
    write_to_json(data, args.json_output)
    print(f"Wrote {len(data)} records to '{args.json_output}'.")

if __name__ == '__main__':
    main()
