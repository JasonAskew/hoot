#!/usr/bin/env python3
"""
Test the intent navigation generator to see why it's not producing tests
"""

import json
from intent_navigation_test_generator import IntentNavigationTestGenerator

def main():
    generator = IntentNavigationTestGenerator()
    
    print("Loading data...")
    generator.load_data()
    
    print(f"Loaded {len(generator.intents)} intents")
    print(f"Loaded {len(generator.responses)} responses")
    
    # Try to generate navigation tests
    print("\nGenerating navigation tests...")
    test_suite = generator.generate_comprehensive_navigation_tests()
    
    print(f"\nTest suite generated:")
    print(f"Total navigation tests: {len(test_suite.get('navigation_tests', []))}")
    
    # Print statistics
    stats = test_suite.get('statistics', {})
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show a sample test if available
    nav_tests = test_suite.get('navigation_tests', [])
    if nav_tests:
        print(f"\nSample test:")
        sample = nav_tests[0]
        print(json.dumps(sample, indent=2))
    else:
        print("\nNo navigation tests were generated!")
        
        # Check for any responses with quick replies
        print("\nChecking for responses with quick replies...")
        found_quick_replies = False
        for response_name, response_data in generator.responses.items():
            quick_replies = generator.extract_intent_quick_replies(response_data)
            if quick_replies:
                print(f"\nFound quick replies in {response_name}:")
                print(json.dumps(quick_replies[:3], indent=2))  # Show first 3
                found_quick_replies = True
                break
        
        if not found_quick_replies:
            print("No quick replies found in any responses!")


if __name__ == '__main__':
    main()