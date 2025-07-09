#!/usr/bin/env python3
"""
Patch to add test case numbers to test generation
"""

def create_consolidated_test_generator_patch():
    """Create patch for consolidated_test_generator.py"""
    
    patch = '''
--- Original consolidated_test_generator.py
+++ Modified consolidated_test_generator.py

@@ -467,6 +467,14 @@ def generate_consolidated_test_suite(self, format_type: str = "standard"):
         # Combine all tests
         all_tests = matrix_tests + conversation_tests + navigation_tests
         
+        # Add test case numbers to CAPI format tests
+        if format_type != "hoot":
+            test_case_number = 1
+            for test in all_tests:
+                test['test_case_number'] = test_case_number
+                test_case_number += 1
+            logger.info(f"✅ Added test case numbers to {len(all_tests)} tests")
+        
         # Remove duplicates
         all_tests = self._remove_duplicate_tests(all_tests, format_type)
         
@@ -483,6 +491,7 @@ def generate_consolidated_test_suite(self, format_type: str = "standard"):
             output_file = f"consolidated_tests_capi_{self.timestamp}.csv"
             # Use comprehensive fieldnames for CAPI format
             fieldnames = [
+                'test_case_number',  # Add test case number as first field
                 'test_source', 'test_type', 'segment', 'segment_description', 'segment_active',
                 'intent', 'intent_display_name', 'intent_active', 'enabled_for_segment',
                 'example_trigger', 'response_type', 'expected_response', 'expected_buttons',
'''
    
    print("Patch for consolidated_test_generator.py:")
    print(patch)
    print("\n" + "="*60 + "\n")


def create_filter_tests_subset_patch():
    """Create patch for filter_tests_subset.py"""
    
    patch = '''
--- Original filter_tests_subset.py
+++ Modified filter_tests_subset.py

@@ -58,7 +58,11 @@ def filter_tests_capi(self, input_file: str, top_intents: List[str], top_segment
                         
                         # Check if this test should be included
                         should_include = False
-                        test_key = None
+                        test_key = None
+                        
+                        # Preserve test case number if it exists
+                        test_case_number = row.get('test_case_number', '')
+                        
                         segment = row.get('segment', '').strip()
                         intent = row.get('intent', '').strip()

@@ -115,6 +119,9 @@ def filter_tests_capi(self, input_file: str, top_intents: List[str], top_segment
                         if should_include and test_key not in seen_tests:
                             seen_tests.add(test_key)
                             filtered_tests.append(row)
+                            # Make sure test_case_number is preserved
+                            if test_case_number:
+                                row['test_case_number'] = test_case_number
         
         logger.info(f"✅ Filtered {len(filtered_tests)} tests from {len(all_tests)} total tests")
         return filtered_tests
'''
    
    print("Patch for filter_tests_subset.py:")
    print(patch)


def main():
    print("TEST CASE NUMBER PATCHES")
    print("="*60)
    print("\nThese patches will add test case numbers to the generated test CSV files.")
    print("\nTo apply these patches manually:\n")
    
    print("1. For consolidated_test_generator.py:")
    print("   - Add test case numbering after combining all tests (around line 467)")
    print("   - Add 'test_case_number' as the first field in CAPI fieldnames (line 483)")
    
    print("\n2. For filter_tests_subset.py:")
    print("   - Preserve test_case_number when filtering tests")
    print("   - Ensure the field is carried through to the output")
    
    print("\n" + "="*60 + "\n")
    
    create_consolidated_test_generator_patch()
    create_filter_tests_subset_patch()


if __name__ == '__main__':
    main()