#!/usr/bin/env python3
"""
CAPI Batch Processor
Processes a specific batch of tests from the CSV file.
"""

import csv
import json
import argparse
import logging
import os
import sys
import time
from datetime import datetime
from typing import List, Dict, Optional

# Import the main test runner
from capi_test_runner import CAPITestRunner


class BatchProcessor:
    """Processes a specific batch of tests."""
    
    def __init__(self, test_file: str, start_idx: int, end_idx: int, 
                 batch_num: int, log_file: str):
        self.test_file = test_file
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.batch_num = batch_num
        self.log_file = log_file
        self.batch_status_file = f"batch_status_{batch_num:04d}.json"
        self.batch_results_file = f"batch_results_{batch_num:04d}.json"
        self.batch_checkpoint_file = f"batch_checkpoint_{batch_num:04d}.json"
        
        # Setup logging
        self.setup_logging()
        
        # Initialize test runner
        self.runner = CAPITestRunner()
        # Override checkpoint settings for batch processing
        self.runner.checkpoint_interval = 5  # Save more frequently in batch mode
        
    def setup_logging(self):
        """Setup logging for this batch."""
        logging.basicConfig(
            level=logging.INFO,
            format=f'Batch {self.batch_num} - %(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def save_batch_status(self, status: Dict):
        """Save batch execution status."""
        status_data = {
            "batch_num": self.batch_num,
            "start_idx": self.start_idx,
            "end_idx": self.end_idx,
            "test_file": self.test_file,
            "timestamp": datetime.now().isoformat(),
            **status
        }
        
        with open(self.batch_status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def save_batch_checkpoint(self, current_idx: int, results: List[Dict]):
        """Save batch checkpoint for resumability."""
        checkpoint_data = {
            "batch_num": self.batch_num,
            "current_idx": current_idx,
            "completed_in_batch": len(results),
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
        
        # Atomic write
        temp_file = f"{self.batch_checkpoint_file}.tmp"
        with open(temp_file, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        
        os.replace(temp_file, self.batch_checkpoint_file)
    
    def load_batch_checkpoint(self) -> Optional[Dict]:
        """Load batch checkpoint if exists."""
        if os.path.exists(self.batch_checkpoint_file):
            try:
                with open(self.batch_checkpoint_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load batch checkpoint: {e}")
        return None
    
    def load_test_cases(self) -> List[Dict]:
        """Load test cases for this batch from CSV."""
        test_cases = []
        
        with open(self.test_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for idx, row in enumerate(reader):
                if self.start_idx <= idx < self.end_idx:
                    # Skip inactive segments if standard format
                    if 'segment_active' in row and row.get('segment_active', '').lower() != 'yes':
                        continue
                    test_cases.append(row)
                elif idx >= self.end_idx:
                    break
        
        return test_cases
    
    def process_batch(self):
        """Process the batch of tests."""
        self.logger.info(f"Starting batch {self.batch_num} processing")
        self.logger.info(f"Test range: {self.start_idx} to {self.end_idx}")
        
        # Update status
        self.save_batch_status({
            "status": "running",
            "start_time": datetime.now().isoformat()
        })
        
        # Check for existing checkpoint
        checkpoint = self.load_batch_checkpoint()
        start_from = 0
        results = []
        
        if checkpoint:
            start_from = checkpoint.get('current_idx', 0) - self.start_idx
            results = checkpoint.get('results', [])
            self.logger.info(f"Resuming from checkpoint: {len(results)} tests completed")
        
        # Load test cases
        test_cases = self.load_test_cases()
        total_tests = len(test_cases)
        self.logger.info(f"Loaded {total_tests} test cases for this batch")
        
        # Process tests
        completed = len(results)
        failed_count = 0
        
        for idx, test_case in enumerate(test_cases[start_from:], start_from):
            try:
                self.logger.info(f"Processing test {idx + 1}/{total_tests}")
                
                # Determine format and run test
                if 'test_case_summary_id' in test_case:
                    # HOOT format - need to parse differently
                    self.logger.warning("HOOT format detected - using standard runner")
                    result = self.runner.run_test_case(test_case)
                else:
                    # Standard format
                    result = self.runner.run_test_case(test_case)
                
                results.append(result)
                completed += 1
                
                # Log progress
                if result['status'] != 'PASSED':
                    failed_count += 1
                
                success_rate = ((completed - failed_count) / completed * 100) if completed > 0 else 0
                self.logger.info(f"Progress: {completed}/{total_tests} | Success rate: {success_rate:.1f}%")
                
                # Save checkpoint periodically
                if completed % 5 == 0:
                    self.save_batch_checkpoint(self.start_idx + idx + 1, results)
                    self.save_batch_status({
                        "status": "running",
                        "progress": f"{completed}/{total_tests}",
                        "success_rate": success_rate
                    })
                
                # Small delay between tests
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                self.logger.info("Batch processing interrupted by user")
                self.save_batch_checkpoint(self.start_idx + idx, results)
                self.save_batch_status({
                    "status": "interrupted",
                    "completed": completed,
                    "total": total_tests
                })
                raise
                
            except Exception as e:
                self.logger.error(f"Error processing test {idx}: {e}")
                # Continue with next test
                continue
        
        # Save final results
        self.logger.info(f"Batch {self.batch_num} completed: {completed} tests processed")
        
        with open(self.batch_results_file, 'w') as f:
            json.dump({
                "batch_num": self.batch_num,
                "start_idx": self.start_idx,
                "end_idx": self.end_idx,
                "total_tests": total_tests,
                "completed_tests": completed,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2)
        
        # Final status update
        final_success_rate = ((completed - failed_count) / completed * 100) if completed > 0 else 0
        self.save_batch_status({
            "status": "completed",
            "end_time": datetime.now().isoformat(),
            "total_tests": total_tests,
            "completed_tests": completed,
            "failed_tests": failed_count,
            "success_rate": final_success_rate
        })
        
        # Clean up checkpoint
        if os.path.exists(self.batch_checkpoint_file):
            os.remove(self.batch_checkpoint_file)
        
        return results


def main():
    parser = argparse.ArgumentParser(description='Process a batch of CAPI tests')
    parser.add_argument('--test-file', required=True, help='CSV file with test cases')
    parser.add_argument('--start', type=int, required=True, help='Start index (0-based)')
    parser.add_argument('--end', type=int, required=True, help='End index (exclusive)')
    parser.add_argument('--batch-num', type=int, required=True, help='Batch number')
    parser.add_argument('--log-file', default=None, help='Log file path')
    
    args = parser.parse_args()
    
    # Set default log file if not provided
    if not args.log_file:
        args.log_file = f"batch_{args.batch_num:04d}.log"
    
    # Create processor and run
    processor = BatchProcessor(
        test_file=args.test_file,
        start_idx=args.start,
        end_idx=args.end,
        batch_num=args.batch_num,
        log_file=args.log_file
    )
    
    try:
        processor.process_batch()
        sys.exit(0)
    except Exception as e:
        print(f"Batch processing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()