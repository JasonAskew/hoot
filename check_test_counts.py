#!/usr/bin/env python3
"""
Check how many tests would be generated
"""

import json
from pathlib import Path

def count_potential_tests():
    base_path = Path('.')
    
    # Count segments
    segments_path = base_path / 'segments'
    segments = list(segments_path.glob('*.json'))
    print(f"Total segments: {len(segments)}")
    
    # Count intents
    intents_path = base_path / 'intents'
    intents = list(intents_path.glob('*.json'))
    print(f"Total intents: {len(intents)}")
    
    # Estimate matrix tests (not all combinations are valid)
    print(f"\nPotential matrix tests: {len(segments)} x {len(intents)} = {len(segments) * len(intents)}")
    
    # Count intents with clarifications
    clarification_intents = 0
    for intent_file in intents:
        try:
            with open(intent_file, 'r') as f:
                data = json.load(f)
                webhook_params = data.get('webhook_params', {})
                messages = webhook_params.get('messages', [])
                for msg in messages:
                    if 'clarify_response_name' in msg:
                        clarification_intents += 1
                        break
        except:
            pass
    
    print(f"\nIntents with clarifications: {clarification_intents}")
    
    # Count navigation possibilities
    nav_count = 0
    responses_path = base_path / 'responses'
    for response_file in responses_path.glob('*.json'):
        try:
            with open(response_file, 'r') as f:
                data = json.load(f)
                # Check default response
                default_resp = data.get('default_response', {})
                message_contents = default_resp.get('message_contents', [])
                for content in message_contents:
                    if content.get('type') == 'BUTTON':
                        payload = content.get('payload', {})
                        if payload.get('type') == 'INTENT':
                            nav_count += 1
                
                # Check segment responses
                for seg_resp in data.get('segment_responses', []):
                    resp = seg_resp.get('response', {})
                    message_contents = resp.get('message_contents', [])
                    for content in message_contents:
                        if content.get('type') == 'BUTTON':
                            payload = content.get('payload', {})
                            if payload.get('type') == 'INTENT':
                                nav_count += 1
        except:
            pass
    
    print(f"\nTotal intent navigation buttons found: {nav_count}")
    
    # Estimate conversation flow tests
    # Assuming 4 quick reply options per clarification on average
    avg_quick_replies = 4
    print(f"\nEstimated conversation flow tests: {clarification_intents} intents x {len(segments)} segments x {avg_quick_replies} options = {clarification_intents * len(segments) * avg_quick_replies}")
    
    # Estimate navigation tests
    print(f"\nEstimated navigation tests: ~{nav_count} (not all may generate valid tests)")
    
    # Total estimate
    matrix_estimate = len(segments) * len(intents) * 0.75  # Assume 75% are valid
    conv_estimate = clarification_intents * len(segments) * avg_quick_replies
    nav_estimate = nav_count
    
    print(f"\n--- TOTAL ESTIMATE ---")
    print(f"Matrix tests: ~{int(matrix_estimate)}")
    print(f"Conversation tests: ~{int(conv_estimate)}")
    print(f"Navigation tests: ~{int(nav_estimate)}")
    print(f"TOTAL: ~{int(matrix_estimate + conv_estimate + nav_estimate)} tests")

if __name__ == '__main__':
    count_potential_tests()