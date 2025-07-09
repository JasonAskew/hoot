#!/usr/bin/env python3
"""
Add conversation flow test support to capi_test_runner.py
"""

import os

def create_conversation_flow_handler():
    """Create the conversation flow handler method"""
    
    method_code = '''
    def run_conversation_flow_test(self, test_case: Dict) -> Dict:
        """Run a multi-turn conversation flow test."""
        segment = test_case['segment']
        intent = test_case['intent']
        example_trigger = test_case['example_trigger']
        expected_response = test_case['expected_response']  # This is the clarification response name
        expected_buttons = test_case.get('expected_buttons', '')
        total_turns = int(test_case.get('total_turns', 1))
        
        # Turn 2 fields
        turn_2_input = test_case.get('turn_2_input', '')
        turn_2_expected_response = test_case.get('turn_2_expected_response', '')
        turn_2_expected_content = test_case.get('turn_2_expected_content', '')
        slot_name = test_case.get('slot_name', '')
        
        logger.info(f"Testing conversation flow: {segment} | {intent} | {example_trigger[:30]}...")
        logger.info(f"  Turn 1: Expecting clarification response")
        logger.info(f"  Turn 2: Sending '{turn_2_input}' -> expecting {turn_2_expected_response}")
        
        # Load profile metadata
        meta_fields = self.load_profile(segment)
        
        # Start session
        session_id = self.start_session(segment, meta_fields)
        if not session_id:
            return {
                'segment': segment,
                'intent': intent,
                'example_trigger': example_trigger,
                'expected_response': expected_response,
                'actual_response': None,
                'session_id': None,
                'status': 'FAILED_SESSION',
                'error': 'Failed to start session',
                'test_type': 'conversation_flow'
            }
        
        # TURN 1: Send initial message
        response_data_1 = self.send_user_message(session_id, segment, meta_fields, example_trigger)
        if not response_data_1:
            return {
                'segment': segment,
                'intent': intent,
                'example_trigger': example_trigger,
                'expected_response': expected_response,
                'actual_response': None,
                'session_id': session_id,
                'status': 'FAILED_MESSAGE',
                'error': 'Failed to send initial message',
                'test_type': 'conversation_flow'
            }
        
        # Extract turn 1 response
        actual_content_1 = self.extract_response_content(response_data_1)
        actual_intent_1 = self.extract_intent_name(response_data_1)
        
        # For clarification intents, we expect the clarification response
        # The expected_response field contains the response name, not the content
        # So we need to load the actual response to compare
        expected_clarify_response = None
        if expected_response and expected_response in self.responses:
            response_data = self.responses[expected_response]
            extracted = self.extract_response_text(response_data.get('default_response', {}))
            expected_clarify_response = extracted['text']
            expected_clarify_buttons = extracted['buttons']
        else:
            # Fallback to treating expected_response as text
            expected_clarify_response = expected_response
            expected_clarify_buttons = expected_buttons.split('|') if expected_buttons else []
        
        # Check if turn 1 matches expected clarification
        turn_1_match = False
        if expected_clarify_response and actual_content_1.get('text'):
            similarity = self.calculate_similarity(
                actual_content_1['text'], 
                expected_clarify_response
            )
            turn_1_match = similarity > 0.8
            
        if not turn_1_match and actual_intent_1 != intent:
            return {
                'segment': segment,
                'intent': intent,
                'example_trigger': example_trigger,
                'expected_response': expected_response,
                'actual_response': actual_content_1.get('text', ''),
                'session_id': session_id,
                'status': 'FAILED_RESPONSE',
                'error': 'Turn 1 failed - did not get expected clarification response',
                'test_type': 'conversation_flow',
                'turn_1_response': actual_content_1
            }
        
        # TURN 2: Send user's choice
        if total_turns >= 2 and turn_2_input:
            logger.info(f"  Sending turn 2 input: {turn_2_input}")
            
            response_data_2 = self.send_user_message(session_id, segment, meta_fields, turn_2_input)
            if not response_data_2:
                return {
                    'segment': segment,
                    'intent': intent,
                    'example_trigger': example_trigger,
                    'expected_response': turn_2_expected_response,
                    'actual_response': None,
                    'session_id': session_id,
                    'status': 'FAILED_MESSAGE',
                    'error': 'Failed to send turn 2 message',
                    'test_type': 'conversation_flow'
                }
            
            # Extract turn 2 response
            actual_content_2 = self.extract_response_content(response_data_2)
            
            # Compare with expected turn 2 response
            comparison = self.compare_responses(
                actual_content_2,
                {'text': turn_2_expected_content, 'buttons': []}
            )
            
            if comparison['overall_match']:
                status = 'PASSED'
            elif comparison['text_similarity'] > 0.8:
                status = 'PARTIAL_PASS'
            else:
                status = 'FAILED_RESPONSE'
            
            return {
                'segment': segment,
                'intent': intent,
                'example_trigger': example_trigger,
                'expected_response': turn_2_expected_content,
                'actual_response': actual_content_2.get('text', ''),
                'actual_buttons': actual_content_2.get('buttons', []),
                'expected_buttons': [],
                'session_id': session_id,
                'status': status,
                'comparison': comparison,
                'test_type': 'conversation_flow',
                'turn_1_response': actual_content_1,
                'turn_2_input': turn_2_input,
                'turn_2_response': actual_content_2,
                'full_response': response_data_2,
                'timestamp': datetime.now().isoformat()
            }
        
        # If we only have 1 turn, return turn 1 results
        return {
            'segment': segment,
            'intent': intent,
            'example_trigger': example_trigger,
            'expected_response': expected_clarify_response,
            'actual_response': actual_content_1.get('text', ''),
            'actual_buttons': actual_content_1.get('buttons', []),
            'expected_buttons': expected_clarify_buttons,
            'session_id': session_id,
            'status': 'PASSED' if turn_1_match else 'FAILED_RESPONSE',
            'test_type': 'conversation_flow',
            'full_response': response_data_1,
            'timestamp': datetime.now().isoformat()
        }
'''
    
    return method_code


def patch_test_runner():
    """Patch the test runner to handle conversation flow tests"""
    
    print("Patching capi_test_runner.py to support conversation flow tests...\n")
    
    # Read the current test runner
    with open('capi_test_runner.py', 'r') as f:
        content = f.read()
    
    # Find where to insert the new method (after run_test_case)
    insert_point = content.find('    def run_test_case(self, test_case: Dict) -> Dict:')
    if insert_point == -1:
        print("ERROR: Could not find run_test_case method!")
        return False
    
    # Find the end of run_test_case method
    method_end = content.find('\n    def ', insert_point + 1)
    if method_end == -1:
        method_end = len(content)
    
    # Insert the new method
    new_method = create_conversation_flow_handler()
    content = content[:method_end] + '\n' + new_method + '\n' + content[method_end:]
    
    # Now update the main test execution loop to check test type
    # Find the line where run_test_case is called
    run_test_call = content.find('result = self.run_test_case(row)')
    if run_test_call == -1:
        print("ERROR: Could not find run_test_case call!")
        return False
    
    # Replace with conditional logic
    old_line = 'result = self.run_test_case(row)'
    new_lines = '''# Check test type and run appropriate handler
                        test_source = row.get('test_source', 'matrix')
                        test_type = row.get('test_type', '')
                        
                        if test_source == 'conversation_flow' or test_type == 'conversation_flow':
                            result = self.run_conversation_flow_test(row)
                        else:
                            result = self.run_test_case(row)'''
    
    content = content.replace(old_line, new_lines)
    
    # Also need to add response loading to __init__
    init_method = content.find('def __init__(self')
    if init_method != -1:
        # Find the end of __init__
        init_end = content.find('\n    def ', init_method + 1)
        if init_end == -1:
            init_end = content.find('\n\n', init_method)
        
        # Add response loading before the end of __init__
        response_loading = '''
        # Load responses for conversation flow tests
        self.responses = {}
        responses_path = Path('responses')
        if responses_path.exists():
            for file in responses_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.responses[data.get('name', file.stem)] = data
                except:
                    pass
'''
        
        # Insert before the last line of __init__
        insert_at = content.rfind('\n', init_method, init_end)
        content = content[:insert_at] + response_loading + content[insert_at:]
    
    # Add necessary imports
    if 'from pathlib import Path' not in content:
        import_point = content.find('import json')
        if import_point != -1:
            content = content[:import_point] + 'from pathlib import Path\n' + content[import_point:]
    
    # Write the patched file
    backup_file = 'capi_test_runner_backup.py'
    patched_file = 'capi_test_runner_patched.py'
    
    # Save backup
    with open('capi_test_runner.py', 'r') as f:
        with open(backup_file, 'w') as backup:
            backup.write(f.read())
    
    # Write patched version
    with open(patched_file, 'w') as f:
        f.write(content)
    
    print(f"✓ Created backup: {backup_file}")
    print(f"✓ Created patched version: {patched_file}")
    print("\nTo apply the patch:")
    print(f"  cp {patched_file} capi_test_runner.py")
    print("\nTo revert:")
    print(f"  cp {backup_file} capi_test_runner.py")
    
    return True


def main():
    print("ADDING CONVERSATION FLOW SUPPORT TO TEST RUNNER")
    print("=" * 60)
    
    if patch_test_runner():
        print("\n✅ Patch created successfully!")
        print("\nThe patched test runner will:")
        print("1. Check test_source/test_type fields")
        print("2. Run conversation_flow tests with multi-turn logic")
        print("3. Handle clarification responses correctly")
        print("4. Validate both turns of the conversation")
    else:
        print("\n❌ Failed to create patch!")


if __name__ == '__main__':
    main()