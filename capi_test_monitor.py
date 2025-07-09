#!/usr/bin/env python3
"""
CAPI Test Monitor
Real-time monitoring of CAPI test execution progress.
"""

import os
import json
import time
import glob
import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class TestMonitor:
    """Monitors CAPI test execution progress."""
    
    def __init__(self):
        self.status_file = "capi_test_status.json"
        self.checkpoint_file = "test_checkpoint.json"
        self.pid_file = "capi_test_runner.pid"
        
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in human-readable format."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"
    
    def load_json_file(self, filepath: str) -> Optional[Dict]:
        """Safely load JSON file."""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def get_process_status(self) -> Tuple[bool, Optional[int]]:
        """Check if test process is running."""
        pid_data = self.load_json_file(self.pid_file)
        if isinstance(pid_data, dict):
            pid = pid_data.get('pid')
        else:
            # Handle simple PID file
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
            except:
                return False, None
        
        if pid:
            try:
                # Check if process exists
                os.kill(pid, 0)
                return True, pid
            except OSError:
                return False, pid
        
        return False, None
    
    def get_checkpoint_stats(self) -> Dict:
        """Get statistics from checkpoint file."""
        # Try to read just the essential info without loading entire file
        stats = {
            "tests_completed": 0,
            "last_update": None,
            "current_segment": None,
            "current_intent": None
        }
        
        if os.path.exists(self.checkpoint_file):
            try:
                # Read first few lines to get basic info
                with open(self.checkpoint_file, 'r') as f:
                    first_chunk = f.read(2048)  # Read first 2KB
                    
                # Extract key information
                if '"test_index":' in first_chunk:
                    test_idx = first_chunk.split('"test_index":')[1].split(',')[0].strip()
                    stats["tests_completed"] = int(test_idx)
                
                if '"timestamp":' in first_chunk:
                    timestamp = first_chunk.split('"timestamp":')[1].split(',')[0].strip().strip('"')
                    stats["last_update"] = timestamp
                
                if '"completed_tests":' in first_chunk:
                    completed = first_chunk.split('"completed_tests":')[1].split(',')[0].strip()
                    stats["tests_completed"] = int(completed)
                    
            except Exception as e:
                pass
        
        return stats
    
    def get_batch_status(self) -> Dict:
        """Get status of batch execution."""
        batch_stats = {
            "total_batches": 0,
            "completed_batches": 0,
            "running_batches": 0,
            "failed_batches": 0,
            "batch_details": []
        }
        
        # Find all batch status files
        batch_status_files = glob.glob("batch_status_*.json")
        batch_stats["total_batches"] = len(batch_status_files)
        
        for status_file in sorted(batch_status_files):
            status = self.load_json_file(status_file)
            if status:
                batch_num = status.get("batch_num", 0)
                state = status.get("status", "unknown")
                
                if state == "completed":
                    batch_stats["completed_batches"] += 1
                elif state == "running":
                    batch_stats["running_batches"] += 1
                elif state in ["failed", "error"]:
                    batch_stats["failed_batches"] += 1
                
                batch_stats["batch_details"].append({
                    "batch_num": batch_num,
                    "status": state,
                    "progress": status.get("progress", ""),
                    "success_rate": status.get("success_rate", 0)
                })
        
        return batch_stats
    
    def calculate_eta(self, completed: int, total: int, elapsed_seconds: float) -> str:
        """Calculate estimated time of arrival."""
        if completed == 0 or elapsed_seconds == 0:
            return "Calculating..."
        
        rate = completed / elapsed_seconds
        remaining = total - completed
        eta_seconds = remaining / rate
        
        return self.format_duration(eta_seconds)
    
    def display_progress_bar(self, completed: int, total: int, width: int = 50) -> str:
        """Create a progress bar string."""
        if total == 0:
            return "[" + " " * width + "]"
        
        progress = completed / total
        filled = int(width * progress)
        bar = "[" + "#" * filled + "-" * (width - filled) + "]"
        percentage = f" {progress * 100:.1f}%"
        
        return bar + percentage
    
    def monitor_standard_execution(self, refresh_interval: int = 5):
        """Monitor standard (non-batch) test execution."""
        print("Monitoring CAPI test execution...")
        print("Press Ctrl+C to stop monitoring (tests will continue running)")
        print("-" * 80)
        
        while True:
            try:
                self.clear_screen()
                
                # Header
                print("=" * 80)
                print("CAPI Test Execution Monitor".center(80))
                print("=" * 80)
                print()
                
                # Check process status
                is_running, pid = self.get_process_status()
                
                # Load execution status
                exec_status = self.load_json_file(self.status_file)
                if exec_status:
                    method = exec_status.get("method", "unknown")
                    start_time = exec_status.get("start_time", "")
                    test_file = exec_status.get("test_file", "")
                    
                    print(f"Execution Method: {method}")
                    print(f"Test File: {test_file}")
                    print(f"Process ID: {pid}")
                    print(f"Status: {'RUNNING' if is_running else 'STOPPED'}")
                    print(f"Started: {start_time}")
                    
                    # Calculate elapsed time
                    if start_time:
                        start_dt = datetime.fromisoformat(start_time)
                        elapsed = datetime.now() - start_dt
                        print(f"Elapsed: {self.format_duration(elapsed.total_seconds())}")
                    print()
                
                # Get checkpoint statistics
                checkpoint_stats = self.get_checkpoint_stats()
                completed = checkpoint_stats["tests_completed"]
                
                # Estimate total tests (from test file)
                total_tests = 0
                if exec_status and "test_file" in exec_status:
                    try:
                        with open(exec_status["test_file"], 'r') as f:
                            total_tests = sum(1 for line in f) - 1
                    except:
                        total_tests = 4180  # Fallback estimate
                
                print(f"Tests Completed: {completed:,} / {total_tests:,}")
                
                # Progress bar
                progress_bar = self.display_progress_bar(completed, total_tests)
                print(f"Progress: {progress_bar}")
                
                # Calculate rates and ETA
                if exec_status and start_time and completed > 0:
                    start_dt = datetime.fromisoformat(start_time)
                    elapsed_seconds = (datetime.now() - start_dt).total_seconds()
                    
                    rate = completed / elapsed_seconds
                    print(f"Rate: {rate:.1f} tests/second")
                    
                    eta = self.calculate_eta(completed, total_tests, elapsed_seconds)
                    print(f"ETA: {eta}")
                
                # Last update
                if checkpoint_stats["last_update"]:
                    print(f"\nLast Update: {checkpoint_stats['last_update']}")
                
                # Log file info
                if exec_status and "log_file" in exec_status:
                    print(f"\nLog File: {exec_status['log_file']}")
                    print(f"View logs: tail -f {exec_status['log_file']}")
                
                print("\n" + "-" * 80)
                print(f"Refreshing every {refresh_interval} seconds...")
                
                time.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped. Tests continue running in background.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(refresh_interval)
    
    def monitor_batch_execution(self, refresh_interval: int = 5):
        """Monitor batch test execution."""
        print("Monitoring CAPI batch test execution...")
        print("Press Ctrl+C to stop monitoring")
        print("-" * 80)
        
        while True:
            try:
                self.clear_screen()
                
                # Header
                print("=" * 80)
                print("CAPI Batch Test Execution Monitor".center(80))
                print("=" * 80)
                print()
                
                # Get batch status
                batch_stats = self.get_batch_status()
                
                print(f"Total Batches: {batch_stats['total_batches']}")
                print(f"Completed: {batch_stats['completed_batches']}")
                print(f"Running: {batch_stats['running_batches']}")
                print(f"Failed: {batch_stats['failed_batches']}")
                print()
                
                # Overall progress
                if batch_stats['total_batches'] > 0:
                    overall_progress = batch_stats['completed_batches'] / batch_stats['total_batches']
                    progress_bar = self.display_progress_bar(
                        batch_stats['completed_batches'], 
                        batch_stats['total_batches']
                    )
                    print(f"Overall Progress: {progress_bar}")
                    print()
                
                # Batch details
                print("Batch Details:")
                print("-" * 60)
                print(f"{'Batch':>6} {'Status':>12} {'Progress':>15} {'Success Rate':>12}")
                print("-" * 60)
                
                for batch in sorted(batch_stats['batch_details'], key=lambda x: x['batch_num'])[:20]:
                    status_emoji = {
                        "completed": "✅",
                        "running": "🔄",
                        "failed": "❌",
                        "unknown": "❓"
                    }.get(batch['status'], "")
                    
                    print(f"{batch['batch_num']:>6} {status_emoji} {batch['status']:>10} "
                          f"{batch['progress']:>15} {batch['success_rate']:>10.1f}%")
                
                # Summary statistics
                print("\n" + "-" * 80)
                
                # Calculate total tests processed
                total_completed_tests = 0
                total_failed_tests = 0
                
                for results_file in glob.glob("batch_results_*.json"):
                    results = self.load_json_file(results_file)
                    if results:
                        total_completed_tests += results.get("completed_tests", 0)
                        # Count failures in results
                        for result in results.get("results", []):
                            if result.get("status") not in ["PASSED", "PARTIAL_PASS"]:
                                total_failed_tests += 1
                
                if total_completed_tests > 0:
                    overall_success_rate = ((total_completed_tests - total_failed_tests) / 
                                          total_completed_tests * 100)
                    print(f"Total Tests Processed: {total_completed_tests:,}")
                    print(f"Overall Success Rate: {overall_success_rate:.1f}%")
                
                print(f"\nRefreshing every {refresh_interval} seconds...")
                
                time.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(refresh_interval)
    
    def generate_summary_report(self):
        """Generate a summary report of test execution."""
        print("Generating test execution summary report...")
        
        report_file = f"capi_test_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("CAPI Test Execution Summary Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Execution status
            exec_status = self.load_json_file(self.status_file)
            if exec_status:
                f.write("Execution Details:\n")
                f.write(f"  Method: {exec_status.get('method', 'N/A')}\n")
                f.write(f"  Test File: {exec_status.get('test_file', 'N/A')}\n")
                f.write(f"  Start Time: {exec_status.get('start_time', 'N/A')}\n")
                
                if exec_status.get('method') == 'batch':
                    f.write(f"  Batch Size: {exec_status.get('batch_size', 'N/A')}\n")
                    f.write(f"  Parallel Workers: {exec_status.get('parallel_workers', 'N/A')}\n")
                f.write("\n")
            
            # Results summary
            if exec_status and exec_status.get('method') == 'batch':
                # Batch execution summary
                batch_stats = self.get_batch_status()
                f.write("Batch Execution Summary:\n")
                f.write(f"  Total Batches: {batch_stats['total_batches']}\n")
                f.write(f"  Completed: {batch_stats['completed_batches']}\n")
                f.write(f"  Failed: {batch_stats['failed_batches']}\n")
                f.write("\n")
                
                # Aggregate results
                total_tests = 0
                passed_tests = 0
                failed_tests = 0
                
                for results_file in glob.glob("batch_results_*.json"):
                    results = self.load_json_file(results_file)
                    if results:
                        for result in results.get("results", []):
                            total_tests += 1
                            if result.get("status") == "PASSED":
                                passed_tests += 1
                            else:
                                failed_tests += 1
                
                f.write("Test Results Summary:\n")
                f.write(f"  Total Tests: {total_tests}\n")
                f.write(f"  Passed: {passed_tests}\n")
                f.write(f"  Failed: {failed_tests}\n")
                if total_tests > 0:
                    f.write(f"  Success Rate: {(passed_tests/total_tests*100):.1f}%\n")
                
            else:
                # Standard execution summary
                checkpoint_stats = self.get_checkpoint_stats()
                f.write("Test Progress:\n")
                f.write(f"  Tests Completed: {checkpoint_stats['tests_completed']}\n")
                f.write(f"  Last Update: {checkpoint_stats['last_update']}\n")
            
            f.write("\n" + "=" * 80 + "\n")
        
        print(f"Summary report saved to: {report_file}")
        return report_file


def main():
    parser = argparse.ArgumentParser(description='Monitor CAPI test execution')
    parser.add_argument('--interval', type=int, default=5, 
                        help='Refresh interval in seconds')
    parser.add_argument('--summary', action='store_true',
                        help='Generate summary report and exit')
    
    args = parser.parse_args()
    
    monitor = TestMonitor()
    
    if args.summary:
        monitor.generate_summary_report()
        return
    
    # Check execution method
    exec_status = monitor.load_json_file(monitor.status_file)
    if exec_status and exec_status.get('method') == 'batch':
        monitor.monitor_batch_execution(args.interval)
    else:
        monitor.monitor_standard_execution(args.interval)


if __name__ == "__main__":
    main()