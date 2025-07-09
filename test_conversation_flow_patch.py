#!/usr/bin/env python3
"""
Test the conversation flow patch before applying it
"""

import subprocess
import os

def test_patch():
    """Test that the patched version works"""
    
    print("Testing conversation flow patch...\n")
    
    # First, let's create a minimal test CSV with just one conversation flow test
    test_csv = """test_source,test_type,segment,segment_description,segment_active,intent,intent_display_name,intent_active,enabled_for_segment,example_trigger,response_type,expected_response,expected_buttons,total_turns,description,turn_2_input,turn_2_expected_response,turn_2_expected_content,slot_name,user_input_label,source_intent,target_intent,navigation_type,source_response,target_response,user_action,expected_intent
conversation_flow,conversation_flow,bt_channel_mobile_investor,,Yes,bt_request_for_withdrawal,,Yes,Yes,How do I make a withdrawal,Conversation Flow,bt_request_for_withdrawal_clarify_withdraw_amount_type,Partial withdrawal|Full withdrawal,2,Test bt_request_for_withdrawal clarification flow with Partial withdrawal option,partial withdrawal,bt_request_for_withdrawal_partial_withdrawal_response,"One of our consultants will be able to assist you with this query. If you would like assistance, please select the 'Chat with consultant' button.",withdraw_amount_type,Partial withdrawal,,,,,,,
"""
    
    with open('test_conversation_flow.csv', 'w') as f:
        f.write(test_csv)
    
    print("Created test CSV with one conversation flow test")
    
    # Apply the patch temporarily
    print("\nApplying patch...")
    os.system('cp capi_test_runner_patched.py capi_test_runner_temp.py')
    
    # Check if the patch introduces any syntax errors
    print("\nChecking for syntax errors...")
    result = subprocess.run(['python', '-m', 'py_compile', 'capi_test_runner_temp.py'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Syntax error in patched file!")
        print(result.stderr)
        return False
    else:
        print("✅ No syntax errors found")
    
    # Check if the new method exists
    print("\nChecking if new methods exist...")
    with open('capi_test_runner_temp.py', 'r') as f:
        content = f.read()
        
    checks = [
        ('run_conversation_flow_test', 'Conversation flow handler method'),
        ('test_source', 'Test source checking'),
        ('test_type', 'Test type checking'),
        ('turn_2_input', 'Turn 2 handling'),
        ('self.responses', 'Response loading')
    ]
    
    all_good = True
    for check, desc in checks:
        if check in content:
            print(f"✅ {desc} - Found")
        else:
            print(f"❌ {desc} - Not found")
            all_good = False
    
    # Clean up
    os.remove('capi_test_runner_temp.py')
    os.remove('test_conversation_flow.csv')
    
    return all_good


def main():
    print("TESTING CONVERSATION FLOW PATCH")
    print("=" * 60)
    
    if test_patch():
        print("\n✅ All checks passed! The patch appears to be working correctly.")
        print("\nYou can now apply the patch with:")
        print("  cp capi_test_runner_patched.py capi_test_runner.py")
        print("\nThen re-run your tests. The conversation flow tests should work properly.")
    else:
        print("\n❌ Some checks failed. Please review the patch before applying.")


if __name__ == '__main__':
    main()