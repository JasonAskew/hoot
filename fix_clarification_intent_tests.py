#!/usr/bin/env python3
"""
Fix the test generation logic for ClarificationIntents
"""

import json
from pathlib import Path

def update_matrix_generator():
    """Update the matrix generator to handle ClarificationIntents correctly"""
    
    # Read the current generator
    generator_file = Path('generate_matrix_with_segment_matching.py')
    with open(generator_file, 'r') as f:
        content = f.read()
    
    # Find the get_intent_response_name method and replace it
    old_method = '''    def get_intent_response_name(self, intent_name: str) -> Optional[str]:
        """Get the response name for an intent"""
        intent = self.intents.get(intent_name, {})
        
        # Check webhook_params first
        webhook_params = intent.get('webhook_params', {})
        if 'response_name' in webhook_params:
            return webhook_params['response_name']
        elif 'default_response_name' in webhook_params:
            return webhook_params['default_response_name']
        
        # Check responses array
        responses = intent.get('responses', [])
        if responses:
            return responses[0]
        
        # Try common patterns
        if f"{intent_name}_response" in self.responses:
            return f"{intent_name}_response"
        elif intent_name in self.responses:
            return intent_name
        
        return None'''
    
    new_method = '''    def get_intent_response_name(self, intent_name: str) -> Optional[str]:
        """Get the response name for an intent"""
        intent = self.intents.get(intent_name, {})
        
        # Check if this is a ClarificationIntent
        webhook_name = intent.get('webhook_name', '')
        if webhook_name == 'ClarificationIntent':
            # For ClarificationIntents, the first response should be the clarification response
            webhook_params = intent.get('webhook_params', {})
            messages = webhook_params.get('messages', [])
            if messages and 'clarify_response_name' in messages[0]:
                return messages[0]['clarify_response_name']
        
        # Check webhook_params for regular intents
        webhook_params = intent.get('webhook_params', {})
        if 'response_name' in webhook_params:
            return webhook_params['response_name']
        elif 'default_response_name' in webhook_params:
            return webhook_params['default_response_name']
        
        # Check responses array
        responses = intent.get('responses', [])
        if responses:
            return responses[0]
        
        # Try common patterns
        if f"{intent_name}_response" in self.responses:
            return f"{intent_name}_response"
        elif intent_name in self.responses:
            return intent_name
        
        return None'''
    
    # Replace the method
    updated_content = content.replace(old_method, new_method)
    
    # Write back
    with open(generator_file, 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated matrix generator to handle ClarificationIntents correctly")
    
    # Also add a method to check if an intent is a ClarificationIntent
    check_clarification = '''
    def is_clarification_intent(self, intent_name: str) -> bool:
        """Check if an intent is a ClarificationIntent"""
        intent = self.intents.get(intent_name, {})
        return intent.get('webhook_name', '') == 'ClarificationIntent'
    '''
    
    # Find a good place to insert this method (after get_intent_response_name)
    insertion_point = updated_content.find('        return None\n    \n    def resolve_response_for_profile')
    if insertion_point > 0:
        updated_content = updated_content[:insertion_point] + '        return None\n    ' + check_clarification + '\n    def resolve_response_for_profile' + updated_content[insertion_point + len('        return None\n    \n    def resolve_response_for_profile'):]
        
        with open(generator_file, 'w') as f:
            f.write(updated_content)
        
        print("✅ Added is_clarification_intent method")


def verify_clarification_intents():
    """Check which intents are ClarificationIntents"""
    intents_path = Path('intents')
    clarification_intents = []
    
    for intent_file in intents_path.glob('*.json'):
        with open(intent_file, 'r') as f:
            data = json.load(f)
            if data.get('webhook_name') == 'ClarificationIntent':
                intent_name = data.get('name', intent_file.stem)
                messages = data.get('webhook_params', {}).get('messages', [])
                if messages and 'clarify_response_name' in messages[0]:
                    clarify_response = messages[0]['clarify_response_name']
                    clarification_intents.append({
                        'intent': intent_name,
                        'clarify_response': clarify_response
                    })
    
    print(f"\nFound {len(clarification_intents)} ClarificationIntents:")
    for ci in clarification_intents:
        print(f"  - {ci['intent']} → {ci['clarify_response']}")
    
    return clarification_intents


def main():
    print("Fixing ClarificationIntent test generation logic...\n")
    
    # First, verify which intents are ClarificationIntents
    clarification_intents = verify_clarification_intents()
    
    # Update the matrix generator
    update_matrix_generator()
    
    print("\n✅ Fix complete! Re-run the test generation to create correct tests for ClarificationIntents.")
    print("\nFor ClarificationIntents, matrix tests will now expect:")
    print("  1. First response: The clarification response (asking which option)")
    print("  2. Conversation flow tests handle the full multi-turn flow")


if __name__ == '__main__':
    main()