#!/usr/bin/env python3
"""
Quick status check for CAPI test execution
"""

import os
import json
from datetime import datetime

def main():
    print("=" * 80)
    print("CAPI Test Execution Status Check")
    print("=" * 80)
    print()
    
    # Check for checkpoint
    if os.path.exists("test_checkpoint.json"):
        print("✓ Checkpoint file found")
        try:
            # Read just the beginning of the file
            with open("test_checkpoint.json", 'r') as f:
                first_line = f.readline()
                second_line = f.readline()
                third_line = f.readline()
                fourth_line = f.readline()
                
            # Extract info from the lines
            if '"test_index":' in second_line:
                test_index = int(second_line.split(':')[1].strip().rstrip(','))
                print(f"  Last test index: {test_index}")
                
            if '"timestamp":' in third_line:
                timestamp = third_line.split(':', 1)[1].strip().strip('",')
                print(f"  Last update: {timestamp}")
                
            if '"completed_tests":' in fourth_line:
                completed = int(fourth_line.split(':')[1].strip().rstrip(','))
                print(f"  Tests completed: {completed}")
                
        except Exception as e:
            print(f"  Error reading checkpoint: {e}")
    else:
        print("✗ No checkpoint file found")
    
    print()
    
    # Check test file
    test_file = "consolidated_tests_capi_20250709_095005.csv"
    if os.path.exists(test_file):
        with open(test_file, 'r') as f:
            total_lines = sum(1 for line in f)
        total_tests = total_lines - 1  # Subtract header
        print(f"✓ Test file found: {test_file}")
        print(f"  Total tests: {total_tests:,}")
    else:
        print(f"✗ Test file not found: {test_file}")
        total_tests = 0
    
    print()
    
    # Check if process is running
    if os.path.exists("capi_test_runner.pid"):
        try:
            with open("capi_test_runner.pid", 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process exists
            try:
                os.kill(pid, 0)
                print(f"✓ Test process is running (PID: {pid})")
            except OSError:
                print(f"✗ Test process is NOT running (stale PID: {pid})")
        except:
            print("✗ Could not read PID file")
    else:
        print("✗ No test process running")
    
    print()
    print("=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    
    if os.path.exists("test_checkpoint.json") and total_tests > 0:
        if 'completed' in locals() and completed < total_tests:
            remaining = total_tests - completed
            print(f"• {remaining:,} tests remaining to complete")
            print(f"• Resume testing with: ./run_capi_tests_background.sh")
            print(f"• Or use batch mode for faster execution:")
            print(f"  ./run_capi_tests_background.sh --method batch --parallel 4")
    else:
        print("• Start fresh test run with:")
        print("  ./run_capi_tests_background.sh --method batch --parallel 4")
    
    print()
    print("• Monitor progress with: python3 capi_test_monitor.py")
    print("• View detailed guide: cat BACKGROUND_TEST_EXECUTION_GUIDE.md")
    print()


if __name__ == "__main__":
    main()