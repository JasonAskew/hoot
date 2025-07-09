#!/usr/bin/env python3
"""
Debug conversation flow tests to understand why they're failing
"""

import csv
import json
from pathlib import Path

def analyze_conversation_tests():
    """Analyze conversation flow tests in the targeted subset"""
    
    # Read the CSV file
    csv_file = 'targeted_subset_capi_20250709_125925.csv'
    
    print(f"Analyzing conversation flow tests in {csv_file}\n")
    
    # First, print the CSV headers
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        print("CSV Headers:")
        for i, header in enumerate(headers):
            print(f"{i}: {header}")
        print()
        
        # Find conversation flow tests
        conversation_tests = []
        for row in reader:
            if row.get('test_source') == 'conversation_flow':
                conversation_tests.append(row)
        
        print(f"Found {len(conversation_tests)} conversation flow tests\n")
        
        # Analyze the first conversation test in detail
        if conversation_tests:
            test = conversation_tests[0]
            print("First conversation flow test structure:")
            print("-" * 60)
            for key, value in test.items():
                if value:  # Only print non-empty fields
                    print(f"{key}: {value}")
            print("-" * 60)
            
            # Check if the test has multi-turn information
            print("\nMulti-turn fields:")
            print(f"total_turns: {test.get('total_turns', 'NOT FOUND')}")
            print(f"turn_2_input: {test.get('turn_2_input', 'NOT FOUND')}")
            print(f"turn_2_expected_response: {test.get('turn_2_expected_response', 'NOT FOUND')}")
            print(f"turn_2_expected_content: {test.get('turn_2_expected_content', 'NOT FOUND')}")
            print(f"slot_name: {test.get('slot_name', 'NOT FOUND')}")
            print(f"user_input_label: {test.get('user_input_label', 'NOT FOUND')}")


def check_test_runner_handling():
    """Check how the test runner handles conversation tests"""
    
    print("\n\nChecking capi_test_runner.py for conversation flow handling...\n")
    
    # Read the test runner code
    with open('capi_test_runner.py', 'r') as f:
        content = f.read()
    
    # Check for key terms
    checks = [
        ('test_source', 'Checks test_source field'),
        ('test_type', 'Checks test_type field'),
        ('conversation_flow', 'Mentions conversation_flow'),
        ('total_turns', 'Handles multiple turns'),
        ('turn_2', 'Handles second turn'),
        ('slot_name', 'Handles slot names'),
    ]
    
    for term, description in checks:
        if term in content:
            print(f"✓ {description} - FOUND")
            # Find context
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if term in line and not line.strip().startswith('#'):
                    print(f"  Line {i+1}: {line.strip()}")
                    break
        else:
            print(f"✗ {description} - NOT FOUND")


def suggest_fix():
    """Suggest how to fix conversation flow tests"""
    
    print("\n\nPROBLEM DIAGNOSIS:")
    print("-" * 60)
    print("1. Conversation flow tests require multi-turn interactions:")
    print("   - Turn 1: Send initial trigger, expect clarification response")
    print("   - Turn 2: Send user's choice, expect final response")
    print()
    print("2. Current capi_test_runner.py only handles single-turn tests")
    print("   - It sends example_trigger")
    print("   - It expects expected_response") 
    print("   - It doesn't handle turn_2_input or turn_2_expected_response")
    print()
    print("SUGGESTED FIX:")
    print("-" * 60)
    print("The test runner needs to be updated to:")
    print("1. Check test_source or test_type field")
    print("2. If it's 'conversation_flow', execute multi-turn logic:")
    print("   a. Send example_trigger")
    print("   b. Verify expected_response (clarification)")
    print("   c. Send turn_2_input") 
    print("   d. Verify turn_2_expected_response")
    print()
    print("The conversation flow tests are structured correctly in the CSV,")
    print("but the test runner doesn't have the logic to execute them properly.")


def check_failed_tests():
    """Check the actual failed conversation tests from results"""
    
    print("\n\nChecking actual test results...\n")
    
    # Try to read the test results
    result_files = ['test_results_20250709_130314.json', 'test_results_20250709_130410.csv']
    
    for file in result_files:
        if Path(file).exists():
            if file.endswith('.json'):
                with open(file, 'r') as f:
                    data = json.load(f)
                    # Handle both dict and list formats
                    if isinstance(data, dict):
                        results = data.get('results', [])
                    else:
                        results = data
                    failed_conv_tests = [
                        test for test in results
                        if 'conversation_flow' in str(test.get('description', ''))
                    ]
                    if failed_conv_tests:
                        print(f"Failed conversation test example from {file}:")
                        test = failed_conv_tests[0]
                        print(f"Status: {test.get('status')}")
                        print(f"Error: {test.get('error', 'Unknown error')}")
                        print(f"Intent: {test.get('intent')}")
                        print(f"Example trigger: {test.get('example_trigger')}")
                        break


def main():
    print("CONVERSATION FLOW TEST DEBUGGING")
    print("=" * 60)
    
    analyze_conversation_tests()
    check_test_runner_handling()
    check_failed_tests()
    suggest_fix()


if __name__ == '__main__':
    main()