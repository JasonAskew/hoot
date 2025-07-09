#!/usr/bin/env python3
"""
Fix JSON format in segments and intents directories
Converts files from [{}] format to {} format
"""
import json
import os
from pathlib import Path

def fix_json_files(directory):
    """Fix JSON files in the specified directory"""
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Directory {directory} does not exist")
        return
    
    fixed_count = 0
    error_count = 0
    
    for file_path in dir_path.glob('*.json'):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check if data is a list with one element
            if isinstance(data, list) and len(data) == 1:
                # Extract the dictionary from the list
                fixed_data = data[0]
                
                # Write back as a dictionary
                with open(file_path, 'w') as f:
                    json.dump(fixed_data, f, indent=2)
                
                fixed_count += 1
                print(f"✓ Fixed: {file_path.name}")
            else:
                print(f"- Skipped: {file_path.name} (not a single-element list)")
                
        except Exception as e:
            error_count += 1
            print(f"✗ Error processing {file_path.name}: {e}")
    
    return fixed_count, error_count

def main():
    """Main function"""
    print("Fixing JSON format issues...")
    print("=" * 60)
    
    # Fix segments
    print("\nFixing segments directory...")
    segments_fixed, segments_errors = fix_json_files('segments')
    
    # Fix intents
    print("\nFixing intents directory...")
    intents_fixed, intents_errors = fix_json_files('intents')
    
    # Fix responses
    print("\nFixing responses directory...")
    responses_fixed, responses_errors = fix_json_files('responses')
    
    # Fix entities
    print("\nFixing entities directory...")
    entities_fixed, entities_errors = fix_json_files('entities')
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"Segments: {segments_fixed} fixed, {segments_errors} errors")
    print(f"Intents: {intents_fixed} fixed, {intents_errors} errors")
    print(f"Responses: {responses_fixed} fixed, {responses_errors} errors")
    print(f"Entities: {entities_fixed} fixed, {entities_errors} errors")
    print(f"Total: {segments_fixed + intents_fixed + responses_fixed + entities_fixed} files fixed")
    print("=" * 60)

if __name__ == "__main__":
    main()