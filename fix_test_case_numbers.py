#!/usr/bin/env python3
"""
Fix test case number preservation in capi_test_runner.py
"""

def create_test_runner_patch():
    """Create patch to preserve test case numbers from input to output"""
    
    patch = '''
The following changes need to be made to capi_test_runner.py:

1. In run_test_case() method (around line 844), add test_case_number to the result:
   
   Change the return statement (around line 919) FROM:
   
        return {
            'segment': segment,
            'actual_segments': actual_segments,
            ...
        }
   
   TO:
   
        return {
            'test_case_number': test_case.get('test_case_number', ''),  # Add this line
            'segment': segment,
            'actual_segments': actual_segments,
            ...
        }

2. In run_conversation_flow_test() method (around line 938), add test_case_number to the result:
   
   In the return statements (around lines 977 and 1048), add:
   
        'test_case_number': test_case.get('test_case_number', ''),

3. In run_hoot_test_case() method (around line 766), add test_case_number to the result:
   
   In all return statements, add:
   
        'test_case_number': test_case.get('test_case_number', ''),

4. In save_results_to_csv() method (around line 1297), update the fieldnames:
   
   Change FROM:
   
        fieldnames = [
            'test_number', 'segment', 'actual_segments', ...
        ]
   
   TO:
   
        fieldnames = [
            'test_case_number', 'test_number', 'segment', 'actual_segments', ...
        ]

5. In the same method, update the row dictionary (around line 1310):
   
   Add this line:
   
        row = {
            'test_case_number': result.get('test_case_number', ''),  # Add this line
            'test_number': i,
            'segment': result.get('segment', ''),
            ...
        }
'''
    
    print("PATCH FOR PRESERVING TEST CASE NUMBERS")
    print("="*60)
    print(patch)
    print("\n" + "="*60 + "\n")
    
    # Create the actual patch file
    patch_content = '''
--- a/capi_test_runner.py
+++ b/capi_test_runner.py
@@ -917,6 +917,7 @@ class CAPITestRunner:
             status = 'FAILED_RESPONSE'  # Poor match
         
         return {
+            'test_case_number': test_case.get('test_case_number', ''),
             'segment': segment,
             'actual_segments': actual_segments,
             'intent': intent,
@@ -974,6 +975,7 @@ class CAPITestRunner:
         
         if not session_id:
             return {
+                'test_case_number': test_case.get('test_case_number', ''),
                 'segment': segment,
                 'intent': intent,
                 'example_trigger': example_trigger,
@@ -1045,6 +1047,7 @@ class CAPITestRunner:
             status = 'FAILED_RESPONSE'
         
         return {
+            'test_case_number': test_case.get('test_case_number', ''),
             'segment': segment,
             'actual_segments': actual_segments,
             'intent': intent,
@@ -1296,6 +1299,7 @@ class CAPITestRunner:
                 else:
                     # Define CSV columns for standard format
                     fieldnames = [
+                        'test_case_number',
                         'test_number', 'segment', 'actual_segments', 'intent', 'actual_intent', 'example_trigger', 
                         'status', 'text_match', 'text_similarity', 'buttons_match',
                         'expected_response', 'actual_response', 
@@ -1309,6 +1313,7 @@ class CAPITestRunner:
                     for i, result in enumerate(self.results, 1):
                         comparison = result.get('comparison', {})
                         row = {
+                            'test_case_number': result.get('test_case_number', ''),
                             'test_number': i,
                             'segment': result.get('segment', ''),
                             'actual_segments': '|'.join(result.get('actual_segments', [])) if result.get('actual_segments') else '',
'''
    
    with open('preserve_test_numbers.patch', 'w') as f:
        f.write(patch_content)
    
    print("Created patch file: preserve_test_numbers.patch")
    print("\nTo apply this patch:")
    print("  patch -p1 < preserve_test_numbers.patch")


def main():
    create_test_runner_patch()


if __name__ == '__main__':
    main()