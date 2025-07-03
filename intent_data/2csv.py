import os
import json
import csv

def collect_json_records(root_dir):
    all_records = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_records.extend(data)
                        else:
                            print(f"Skipping non-list JSON structure in {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return all_records

def write_csv(records, output_file):
    if not records:
        print("No records to write.")
        return

    fieldnames = sorted({key for record in records for key in record.keys()})
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

if __name__ == "__main__":
    input_directory = "./"  # Replace with your actual directory path
    output_csv_file = "combined_output.csv"

    all_records = collect_json_records(input_directory)
    write_csv(all_records, output_csv_file)

    print(f"CSV written to {output_csv_file} with {len(all_records)} records.")
