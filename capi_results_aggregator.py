#!/usr/bin/env python3
"""
CAPI Results Aggregator
Combines results from multiple batch executions into a single report.
"""

import json
import glob
import csv
import os
from datetime import datetime
from typing import Dict, List
import argparse


class ResultsAggregator:
    """Aggregates results from multiple test executions."""
    
    def __init__(self):
        self.all_results = []
        self.summary_stats = {
            "total_tests": 0,
            "passed": 0,
            "partial_pass": 0,
            "failed": 0,
            "by_status": {},
            "by_segment": {},
            "by_intent": {}
        }
    
    def load_batch_results(self, pattern: str = "batch_results_*.json") -> int:
        """Load results from batch execution files."""
        batch_files = sorted(glob.glob(pattern))
        print(f"Found {len(batch_files)} batch result files")
        
        loaded_count = 0
        for batch_file in batch_files:
            try:
                with open(batch_file, 'r') as f:
                    batch_data = json.load(f)
                    
                results = batch_data.get("results", [])
                self.all_results.extend(results)
                loaded_count += len(results)
                
                print(f"Loaded {len(results)} results from {batch_file}")
            except Exception as e:
                print(f"Error loading {batch_file}: {e}")
        
        return loaded_count
    
    def load_standard_results(self, pattern: str = "test_results_*.json") -> int:
        """Load results from standard execution files."""
        result_files = sorted(glob.glob(pattern))
        print(f"Found {len(result_files)} standard result files")
        
        loaded_count = 0
        for result_file in result_files:
            try:
                with open(result_file, 'r') as f:
                    results = json.load(f)
                    
                if isinstance(results, list):
                    self.all_results.extend(results)
                    loaded_count += len(results)
                    print(f"Loaded {len(results)} results from {result_file}")
            except Exception as e:
                print(f"Error loading {result_file}: {e}")
        
        return loaded_count
    
    def analyze_results(self):
        """Analyze all loaded results."""
        for result in self.all_results:
            self.summary_stats["total_tests"] += 1
            
            # Status analysis
            status = result.get("status", "UNKNOWN")
            self.summary_stats["by_status"][status] = \
                self.summary_stats["by_status"].get(status, 0) + 1
            
            if status == "PASSED":
                self.summary_stats["passed"] += 1
            elif status == "PARTIAL_PASS":
                self.summary_stats["partial_pass"] += 1
            else:
                self.summary_stats["failed"] += 1
            
            # Segment analysis
            segment = result.get("segment", "unknown")
            if segment not in self.summary_stats["by_segment"]:
                self.summary_stats["by_segment"][segment] = {
                    "total": 0, "passed": 0, "failed": 0
                }
            self.summary_stats["by_segment"][segment]["total"] += 1
            if status == "PASSED":
                self.summary_stats["by_segment"][segment]["passed"] += 1
            else:
                self.summary_stats["by_segment"][segment]["failed"] += 1
            
            # Intent analysis
            intent = result.get("intent", "unknown")
            if intent not in self.summary_stats["by_intent"]:
                self.summary_stats["by_intent"][intent] = {
                    "total": 0, "passed": 0, "failed": 0
                }
            self.summary_stats["by_intent"][intent]["total"] += 1
            if status == "PASSED":
                self.summary_stats["by_intent"][intent]["passed"] += 1
            else:
                self.summary_stats["by_intent"][intent]["failed"] += 1
    
    def save_aggregated_results(self, output_file: str = None):
        """Save all aggregated results to a single file."""
        if not output_file:
            output_file = f"aggregated_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                "summary": self.summary_stats,
                "results": self.all_results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"Aggregated results saved to: {output_file}")
        return output_file
    
    def save_csv_report(self, output_file: str = None):
        """Save results as CSV for easy analysis."""
        if not output_file:
            output_file = f"aggregated_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not self.all_results:
            print("No results to save")
            return None
        
        # Determine if we have HOOT or standard format
        is_hoot = "validations" in self.all_results[0]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if is_hoot:
                fieldnames = [
                    'test_number', 'test_case_id', 'test_case_name', 'segment',
                    'trigger_text', 'status', 'validation_count', 'passed_validations',
                    'failed_validations', 'session_id', 'timestamp'
                ]
            else:
                fieldnames = [
                    'test_number', 'segment', 'intent', 'example_trigger',
                    'status', 'actual_intent', 'text_similarity', 'expected_response',
                    'actual_response', 'session_id', 'timestamp'
                ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, result in enumerate(self.all_results, 1):
                if is_hoot:
                    validations = result.get('validations', [])
                    passed_validations = len([v for v in validations if v.get('status') == 'PASSED'])
                    failed_validations = len(validations) - passed_validations
                    
                    row = {
                        'test_number': i,
                        'test_case_id': result.get('test_case_id', ''),
                        'test_case_name': result.get('test_case_name', ''),
                        'segment': result.get('segment', ''),
                        'trigger_text': result.get('trigger_text', ''),
                        'status': result.get('status', ''),
                        'validation_count': len(validations),
                        'passed_validations': passed_validations,
                        'failed_validations': failed_validations,
                        'session_id': result.get('session_id', ''),
                        'timestamp': result.get('timestamp', '')
                    }
                else:
                    comparison = result.get('comparison', {})
                    row = {
                        'test_number': i,
                        'segment': result.get('segment', ''),
                        'intent': result.get('intent', ''),
                        'example_trigger': result.get('example_trigger', ''),
                        'status': result.get('status', ''),
                        'actual_intent': result.get('actual_intent', ''),
                        'text_similarity': f"{comparison.get('text_similarity', 0):.3f}" if comparison else '',
                        'expected_response': result.get('expected_response', ''),
                        'actual_response': result.get('actual_response', ''),
                        'session_id': result.get('session_id', ''),
                        'timestamp': result.get('timestamp', '')
                    }
                
                writer.writerow(row)
        
        print(f"CSV report saved to: {output_file}")
        return output_file
    
    def generate_summary_report(self, output_file: str = None):
        """Generate a detailed summary report."""
        if not output_file:
            output_file = f"test_summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CAPI Test Execution Summary Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Overall summary
            total = self.summary_stats["total_tests"]
            if total > 0:
                success_rate = (self.summary_stats["passed"] / total * 100)
                f.write("Overall Results:\n")
                f.write(f"  Total Tests: {total:,}\n")
                f.write(f"  Passed: {self.summary_stats['passed']:,} ({self.summary_stats['passed']/total*100:.1f}%)\n")
                f.write(f"  Partial Pass: {self.summary_stats['partial_pass']:,} ({self.summary_stats['partial_pass']/total*100:.1f}%)\n")
                f.write(f"  Failed: {self.summary_stats['failed']:,} ({self.summary_stats['failed']/total*100:.1f}%)\n")
                f.write(f"  Success Rate: {success_rate:.1f}%\n")
                f.write("\n")
            
            # Status breakdown
            f.write("Results by Status:\n")
            for status, count in sorted(self.summary_stats["by_status"].items()):
                percentage = (count / total * 100) if total > 0 else 0
                f.write(f"  {status}: {count} ({percentage:.1f}%)\n")
            f.write("\n")
            
            # Segment performance
            f.write("Results by Segment:\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Segment':<40} {'Total':>8} {'Passed':>8} {'Failed':>8} {'Rate':>8}\n")
            f.write("-" * 70 + "\n")
            
            for segment, stats in sorted(self.summary_stats["by_segment"].items()):
                rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
                f.write(f"{segment:<40} {stats['total']:>8} {stats['passed']:>8} "
                        f"{stats['failed']:>8} {rate:>7.1f}%\n")
            
            f.write("\n")
            
            # Top failing intents
            f.write("Top 20 Failing Intents:\n")
            f.write("-" * 70 + "\n")
            
            # Sort intents by failure count
            intent_failures = []
            for intent, stats in self.summary_stats["by_intent"].items():
                if stats['failed'] > 0:
                    intent_failures.append((intent, stats['failed'], stats['total']))
            
            intent_failures.sort(key=lambda x: x[1], reverse=True)
            
            for intent, failed, total in intent_failures[:20]:
                failure_rate = (failed / total * 100) if total > 0 else 0
                f.write(f"{intent:<50} {failed:>5}/{total:<5} ({failure_rate:>5.1f}%)\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Summary report saved to: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(description='Aggregate CAPI test results')
    parser.add_argument('--batch-pattern', default="batch_results_*.json",
                        help='Pattern for batch result files')
    parser.add_argument('--standard-pattern', default="test_results_*.json",
                        help='Pattern for standard result files')
    parser.add_argument('--output-json', help='Output JSON file name')
    parser.add_argument('--output-csv', help='Output CSV file name')
    parser.add_argument('--output-report', help='Output summary report file name')
    
    args = parser.parse_args()
    
    aggregator = ResultsAggregator()
    
    # Load results
    print("Loading test results...")
    batch_count = aggregator.load_batch_results(args.batch_pattern)
    standard_count = aggregator.load_standard_results(args.standard_pattern)
    
    total_loaded = batch_count + standard_count
    print(f"\nTotal results loaded: {total_loaded}")
    
    if total_loaded == 0:
        print("No results found to aggregate")
        return
    
    # Analyze results
    print("\nAnalyzing results...")
    aggregator.analyze_results()
    
    # Save outputs
    print("\nGenerating reports...")
    aggregator.save_aggregated_results(args.output_json)
    aggregator.save_csv_report(args.output_csv)
    aggregator.generate_summary_report(args.output_report)
    
    # Print summary
    print("\nSummary:")
    print(f"  Total tests: {aggregator.summary_stats['total_tests']:,}")
    print(f"  Passed: {aggregator.summary_stats['passed']:,}")
    print(f"  Failed: {aggregator.summary_stats['failed']:,}")
    if aggregator.summary_stats['total_tests'] > 0:
        success_rate = (aggregator.summary_stats['passed'] / 
                       aggregator.summary_stats['total_tests'] * 100)
        print(f"  Success rate: {success_rate:.1f}%")


if __name__ == "__main__":
    main()