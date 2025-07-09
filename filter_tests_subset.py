#!/usr/bin/env python3
"""
Filter test files to create a targeted subset based on specific intents and segments
"""

import csv
import os
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_filter_criteria():
    """Load intents and segments from filter files"""
    # Load top intents
    top_intents = set()
    with open('top_intents.txt', 'r') as f:
        for line in f:
            intent = line.strip()
            if intent:  # Skip empty lines
                top_intents.add(intent)
    
    # Load top segments
    top_segments = set()
    with open('top_segments.txt', 'r') as f:
        for line in f:
            segment = line.strip()
            if segment:  # Skip empty lines
                top_segments.add(segment)
    
    logger.info(f"Loaded {len(top_intents)} intents from top_intents.txt")
    logger.info(f"Loaded {len(top_segments)} segments from top_segments.txt")
    
    return top_intents, top_segments


def filter_test_file(input_file, output_file, top_intents, top_segments):
    """Filter a test file to include only specified intents and segments"""
    filtered_count = 0
    total_count = 0
    seen_tests = set()  # For deduplication
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                total_count += 1
                
                # Get test source to determine how to filter
                test_source = row.get('test_source', 'matrix')
                segment = row.get('segment', '').strip()
                
                # Check if segment is in our filter list
                if segment not in top_segments:
                    continue
                
                # Check intents based on test type
                should_include = False
                test_key = None
                
                if test_source == 'intent_navigation':
                    # For navigation tests, check both source and target intents
                    source_intent = row.get('source_intent', '').strip()
                    target_intent = row.get('target_intent', '').strip()
                    
                    # Include if either source or target intent is in our list
                    if source_intent in top_intents or target_intent in top_intents:
                        should_include = True
                        test_key = f"nav_{source_intent}_{target_intent}_{segment}"
                else:
                    # For matrix and conversation flow tests
                    intent = row.get('intent', '').strip()
                    
                    if intent in top_intents:
                        should_include = True
                        test_type = row.get('test_type', '')
                        turn_2_input = row.get('turn_2_input', '')
                        test_key = f"{test_source}_{intent}_{segment}_{test_type}_{turn_2_input}"
                
                # Write row if it should be included and is not a duplicate
                if should_include and test_key and test_key not in seen_tests:
                    seen_tests.add(test_key)
                    writer.writerow(row)
                    filtered_count += 1
    
    logger.info(f"Filtered {input_file}: {filtered_count}/{total_count} tests retained")
    return filtered_count, total_count


def generate_statistics_report(stats, output_file='targeted_subset_report.md'):
    """Generate a report about the filtered subset"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(output_file, 'w') as f:
        f.write(f"# Targeted Test Subset Report\n\n")
        f.write(f"Generated: {timestamp}\n\n")
        
        f.write("## Filter Criteria\n\n")
        f.write(f"- Intents: {stats['num_intents']} selected\n")
        f.write(f"- Segments: {stats['num_segments']} selected\n\n")
        
        f.write("## Filtering Results\n\n")
        for format_type, format_stats in stats['formats'].items():
            f.write(f"### {format_type.upper()} Format\n")
            f.write(f"- Original tests: {format_stats['total']}\n")
            f.write(f"- Filtered tests: {format_stats['filtered']}\n")
            f.write(f"- Retention rate: {format_stats['percentage']:.1f}%\n\n")
        
        f.write("## Intents Included\n\n")
        for intent in sorted(stats['intents']):
            f.write(f"- {intent}\n")
        
        f.write("\n## Segments Included\n\n")
        for segment in sorted(stats['segments']):
            f.write(f"- {segment}\n")
    
    logger.info(f"Generated statistics report: {output_file}")


def main():
    """Main function"""
    # Load filter criteria
    top_intents, top_segments = load_filter_criteria()
    
    # Find the latest test files
    import glob
    
    # Get the most recent CAPI and HOOT files
    capi_files = sorted(glob.glob('consolidated_tests_capi_*.csv'))
    hoot_files = sorted(glob.glob('consolidated_tests_hoot_*.csv'))
    
    if not capi_files or not hoot_files:
        logger.error("Could not find consolidated test files")
        return
    
    latest_capi = capi_files[-1]
    latest_hoot = hoot_files[-1]
    
    logger.info(f"Using CAPI file: {latest_capi}")
    logger.info(f"Using HOOT file: {latest_hoot}")
    
    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_capi = f'targeted_subset_capi_{timestamp}.csv'
    output_hoot = f'targeted_subset_hoot_{timestamp}.csv'
    
    # Filter the files
    stats = {
        'num_intents': len(top_intents),
        'num_segments': len(top_segments),
        'intents': list(top_intents),
        'segments': list(top_segments),
        'formats': {}
    }
    
    # Filter CAPI file
    capi_filtered, capi_total = filter_test_file(latest_capi, output_capi, top_intents, top_segments)
    stats['formats']['capi'] = {
        'filtered': capi_filtered,
        'total': capi_total,
        'percentage': (capi_filtered / capi_total * 100) if capi_total > 0 else 0
    }
    
    # Filter HOOT file
    hoot_filtered, hoot_total = filter_test_file(latest_hoot, output_hoot, top_intents, top_segments)
    stats['formats']['hoot'] = {
        'filtered': hoot_filtered,
        'total': hoot_total,
        'percentage': (hoot_filtered / hoot_total * 100) if hoot_total > 0 else 0
    }
    
    # Generate report
    generate_statistics_report(stats)
    
    logger.info("\nFiltering complete!")
    logger.info(f"CAPI subset: {output_capi} ({capi_filtered} tests)")
    logger.info(f"HOOT subset: {output_hoot} ({hoot_filtered} tests)")
    
    # Also create a summary CSV showing the intent/segment combinations
    summary_file = f'targeted_subset_summary_{timestamp}.csv'
    with open(summary_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Intent', 'Segment', 'Expected Tests'])
        
        for intent in sorted(top_intents):
            for segment in sorted(top_segments):
                writer.writerow([intent, segment, '1'])
    
    logger.info(f"Summary file: {summary_file}")


if __name__ == '__main__':
    main()