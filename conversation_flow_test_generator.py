#!/usr/bin/env python3
"""
Conversation Flow Test Generator
Generates test cases for multi-turn conversations with clarification responses
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import logging
from segment_intent_validator import SegmentIntentValidator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConversationFlowTestGenerator:
    """Generate test cases for multi-turn conversation flows"""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path)
        self.intents = {}
        self.responses = {}
        self.entities = {}
        self.profiles = {}
        self.conversation_tests = []
        self.validator = SegmentIntentValidator(base_path)
        
    def load_data(self):
        """Load all necessary data"""
        self._load_intents()
        self._load_responses()
        self._load_entities()
        self._load_profiles()
        
    def _load_intents(self):
        """Load intent definitions"""
        intents_path = self.base_path / 'intents'
        if intents_path.exists():
            for file in intents_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.intents[data.get('name', file.stem)] = data
                except Exception as e:
                    logger.error(f"Error loading intent {file}: {e}")
        logger.info(f"Loaded {len(self.intents)} intents")
    
    def _load_responses(self):
        """Load response definitions"""
        responses_path = self.base_path / 'responses'
        if responses_path.exists():
            for file in responses_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.responses[data.get('name', file.stem)] = data
                except Exception as e:
                    logger.error(f"Error loading response {file}: {e}")
        logger.info(f"Loaded {len(self.responses)} responses")
    
    def _load_entities(self):
        """Load entity definitions"""
        entities_path = self.base_path / 'entities'
        if entities_path.exists():
            for file in entities_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        self.entities[data.get('name', file.stem)] = data
                except Exception as e:
                    logger.error(f"Error loading entity {file}: {e}")
        logger.info(f"Loaded {len(self.entities)} entities")
    
    def _load_profiles(self):
        """Load user profiles"""
        profiles_path = self.base_path / 'profiles'
        if profiles_path.exists():
            for file in profiles_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        content = f.read().strip()
                        if content.startswith('"meta_fields":'):
                            content = '{' + content + '}'
                        data = json.loads(content)
                        self.profiles[file.stem] = data.get('meta_fields', [])
                except Exception as e:
                    logger.error(f"Error loading profile {file}: {e}")
        logger.info(f"Loaded {len(self.profiles)} profiles")
    
    def find_intents_with_clarifications(self) -> List[Dict]:
        """Find all intents that have clarification responses"""
        intents_with_clarifications = []
        
        for intent_name, intent_data in self.intents.items():
            webhook_params = intent_data.get('webhook_params', {})
            messages = webhook_params.get('messages', [])
            
            # Check if intent has clarification responses
            for message in messages:
                if 'clarify_response_name' in message:
                    clarification_info = {
                        'intent_name': intent_name,
                        'intent_data': intent_data,
                        'clarification_response': message['clarify_response_name'],
                        'slot_name': message.get('slot_name'),
                        'rules': webhook_params.get('rules', [])
                    }
                    intents_with_clarifications.append(clarification_info)
                    logger.info(f"Found clarification flow: {intent_name} → {message['clarify_response_name']}")
        
        return intents_with_clarifications
    
    def extract_quick_replies(self, response_name: str) -> List[Dict]:
        """Extract quick reply options from a response"""
        response_data = self.responses.get(response_name, {})
        default_response = response_data.get('default_response', {})
        quick_replies = default_response.get('quick_replies', [])
        
        return [{
            'payload': qr.get('payload', ''),
            'label': qr.get('label', ''),
            'type': qr.get('type', 'TEXT')
        } for qr in quick_replies]
    
    def find_matching_rule(self, rules: List[Dict], slot_name: str, value: str) -> Optional[str]:
        """Find the matching rule for a given slot value"""
        for rule in rules:
            conditions = rule.get('conditions', {})
            payload = conditions.get('payload', {})
            
            # Check if this rule matches the slot and value
            if (payload.get('slot') == slot_name and 
                payload.get('value', '').lower() == value.lower()):
                return rule.get('response_name')
        
        logger.warning(f"No matching rule found for {slot_name}={value}")
        return None
    
    def generate_conversation_flow_tests(self) -> List[Dict]:
        """Generate test cases for all conversation flows"""
        conversation_tests = []
        
        # Find all intents with clarification flows
        intents_with_clarifications = self.find_intents_with_clarifications()
        
        for clarification_info in intents_with_clarifications:
            intent_name = clarification_info['intent_name']
            intent_data = clarification_info['intent_data']
            clarification_response = clarification_info['clarification_response']
            slot_name = clarification_info['slot_name']
            rules = clarification_info['rules']
            
            # Get quick replies from clarification response
            quick_replies = self.extract_quick_replies(clarification_response)
            
            if not quick_replies:
                logger.warning(f"No quick replies found for {clarification_response}")
                continue
            
            # Get initial trigger for the intent
            initial_trigger = self._get_intent_trigger(intent_name)
            
            # Generate a test case for each quick reply option
            for quick_reply in quick_replies:
                payload_value = quick_reply['payload']
                label = quick_reply['label']
                
                # Find the expected response for this payload value
                expected_response_name = self.find_matching_rule(rules, slot_name, payload_value)
                
                if not expected_response_name:
                    logger.warning(f"No matching rule found for {slot_name}={payload_value} in {intent_name}")
                    continue
                
                # Get the expected response content
                expected_response_data = self.responses.get(expected_response_name, {})
                
                # Get valid segments for this intent
                valid_segments = self.validator.get_valid_segments_for_intent(intent_name)
                
                if not valid_segments:
                    logger.warning(f"No valid segments found for {intent_name}, skipping test generation")
                    continue
                
                # Create test case for each valid segment
                # Get clarification response content
                clarification_response_data = self.responses.get(clarification_response, {})
                clarification_response_content = self._extract_response_text(clarification_response_data)
                
                for segment in valid_segments:
                    # Create multi-turn test case
                    test_case = {
                        'test_type': 'conversation_flow',
                        'intent': intent_name,
                        'segment': segment,
                        'turns': [
                            {
                                'turn': 1,
                                'user_input': initial_trigger,
                                'expected_intent': intent_name,
                                'expected_response': clarification_response,
                                'expected_response_content': clarification_response_content,
                                'expected_quick_replies': [qr['label'] for qr in quick_replies]
                            },
                            {
                                'turn': 2,
                                'user_input': payload_value,
                                'user_input_label': label,
                                'slot_name': slot_name,
                                'expected_response': expected_response_name,
                                'expected_response_content': self._extract_response_text(expected_response_data)
                            }
                        ],
                        'description': f"Test {intent_name} clarification flow with {label} option (segment: {segment})"
                    }
                    
                    conversation_tests.append(test_case)
                    logger.info(f"Generated test: {intent_name} → {clarification_response} → {payload_value} → {expected_response_name} (segment: {segment})")
        
        return conversation_tests
    
    def _get_intent_trigger(self, intent_name: str) -> str:
        """Get a trigger phrase for an intent"""
        intent_data = self.intents.get(intent_name, {})
        
        # Try display_sentence first
        if 'display_sentence' in intent_data:
            return intent_data['display_sentence']
        
        # Try to load from intent_data file with different naming patterns
        intent_name_lower = intent_name.lower()
        possible_files = [
            self.base_path / 'intent_data' / f'{intent_name_lower}_train.json',
            self.base_path / 'intent_data' / f'{intent_name_lower}_test.json',
            self.base_path / 'intent_data' / f'{intent_name_lower}_seed.json',
            self.base_path / 'intent_data' / f'intent_data_{intent_name_lower}.json'
        ]
        
        for intent_data_file in possible_files:
            if intent_data_file.exists():
                try:
                    with open(intent_data_file, 'r') as f:
                        file_data = json.load(f)
                    
                    # Handle different file formats
                    if isinstance(file_data, list) and len(file_data) > 0 and 'data' in file_data[0]:
                        # New format: [{data: [...]}]
                        data = file_data[0].get('data', [])
                    elif isinstance(file_data, dict) and 'data' in file_data:
                        # Dict format: {data: [...]}
                        data = file_data.get('data', [])
                    elif isinstance(file_data, list):
                        # Direct array format
                        data = file_data
                    else:
                        data = []
                    
                    if isinstance(data, list) and len(data) > 0:
                        for item in data:
                            if item.get('trigger_sentence'):
                                return item['trigger_sentence']
                except:
                    pass
        
        # Fallback
        clean_name = intent_name.replace('bt_', '').replace('_', ' ')
        return f"help with {clean_name}"
    
    def _extract_response_text(self, response_data: Dict) -> str:
        """Extract text content from response data"""
        if not response_data:
            return ""
        
        default_response = response_data.get('default_response', {})
        message_contents = default_response.get('message_contents', [])
        
        texts = []
        for content in message_contents:
            if content.get('type') == 'TEXT':
                text = content.get('payload', {}).get('text', '')
                if text:
                    texts.append(text)
        
        return ' '.join(texts)
    
    def generate_comprehensive_flow_tests(self):
        """Generate comprehensive conversation flow test suite"""
        logger.info("Generating conversation flow tests...")
        
        # Generate basic conversation flow tests
        conversation_tests = self.generate_conversation_flow_tests()
        
        # Add variations for each conversation test
        enhanced_tests = []
        for test in conversation_tests:
            # Original test
            enhanced_tests.append(test)
            
            # Add variations of the initial trigger
            variations = self._generate_trigger_variations(test['turns'][0]['user_input'])
            for var_trigger in variations[:3]:  # Limit to 3 variations
                var_test = json.loads(json.dumps(test))  # Deep copy
                var_test['turns'][0]['user_input'] = var_trigger
                var_test['description'] += f" (variation: {var_trigger[:30]}...)"
                enhanced_tests.append(var_test)
        
        # Add edge cases for conversation flows
        edge_cases = self._generate_conversation_edge_cases(conversation_tests)
        enhanced_tests.extend(edge_cases)
        
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_intents_with_clarifications': len(self.find_intents_with_clarifications()),
                'total_conversation_tests': len(enhanced_tests)
            },
            'conversation_tests': enhanced_tests,
            'statistics': self._calculate_statistics(enhanced_tests)
        }
    
    def _generate_trigger_variations(self, trigger: str) -> List[str]:
        """Generate variations of a trigger phrase"""
        variations = []
        
        # Add politeness
        variations.append(f"please {trigger}")
        variations.append(f"can you {trigger}")
        
        # Question form
        if not trigger.endswith('?'):
            variations.append(f"{trigger}?")
        
        # Typos
        words = trigger.split()
        if len(words) > 2:
            # Swap two words
            words[0], words[1] = words[1], words[0]
            variations.append(' '.join(words))
        
        return variations
    
    def _generate_conversation_edge_cases(self, base_tests: List[Dict]) -> List[Dict]:
        """Generate edge cases for conversation flows"""
        edge_cases = []
        
        # Select a few tests for edge case generation
        for test in base_tests[:5]:
            intent_name = test['intent']
            
            # Edge case 1: Invalid option in clarification
            edge_test = json.loads(json.dumps(test))
            edge_test['test_type'] = 'conversation_edge_case'
            edge_test['turns'][1]['user_input'] = 'invalid_option_xyz'
            edge_test['turns'][1]['expected_behavior'] = 'Handle invalid option gracefully'
            edge_test['description'] = f"Edge case: {intent_name} with invalid clarification option"
            edge_cases.append(edge_test)
            
            # Edge case 2: Interruption during clarification
            interrupt_test = {
                'test_type': 'conversation_interruption',
                'intent': intent_name,
                'turns': [
                    test['turns'][0],  # First turn as normal
                    {
                        'turn': 2,
                        'user_input': 'actually, show me my balance instead',
                        'expected_behavior': 'Handle interruption and context switch',
                        'description': 'User interrupts clarification with different intent'
                    }
                ],
                'description': f"Interruption test: {intent_name} interrupted during clarification"
            }
            edge_cases.append(interrupt_test)
        
        return edge_cases
    
    def _calculate_statistics(self, tests: List[Dict]) -> Dict:
        """Calculate statistics about the test suite"""
        stats = {
            'total_tests': len(tests),
            'conversation_flow_tests': len([t for t in tests if t['test_type'] == 'conversation_flow']),
            'edge_case_tests': len([t for t in tests if 'edge_case' in t['test_type']]),
            'interruption_tests': len([t for t in tests if 'interruption' in t['test_type']]),
            'unique_intents': len(set(t['intent'] for t in tests)),
            'total_turns': sum(len(t['turns']) for t in tests)
        }
        return stats
    
    def export_to_csv(self, test_suite: Dict, output_file: str = 'conversation_flow_tests.csv'):
        """Export conversation tests to CSV format"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'test_id', 'test_type', 'intent', 'turn_number', 
                'user_input', 'expected_intent', 'expected_response', 
                'expected_quick_replies', 'slot_name', 'description'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            test_id = 1
            for test in test_suite['conversation_tests']:
                for turn in test['turns']:
                    writer.writerow({
                        'test_id': f'CFT_{test_id:04d}',
                        'test_type': test['test_type'],
                        'intent': test['intent'],
                        'turn_number': turn['turn'],
                        'user_input': turn.get('user_input', ''),
                        'expected_intent': turn.get('expected_intent', ''),
                        'expected_response': turn.get('expected_response', ''),
                        'expected_quick_replies': '|'.join(turn.get('expected_quick_replies', [])),
                        'slot_name': turn.get('slot_name', ''),
                        'description': test['description']
                    })
                test_id += 1
        
        logger.info(f"Exported {test_id - 1} conversation flow tests to {output_file}")
    
    def export_to_json(self, test_suite: Dict, output_file: str = 'conversation_flow_tests.json'):
        """Export test suite to JSON format"""
        with open(output_file, 'w') as f:
            json.dump(test_suite, f, indent=2)
        
        logger.info(f"Exported conversation flow test suite to {output_file}")
    
    def export_test_documentation(self, test_suite: Dict, output_file: str = 'conversation_flow_tests.md'):
        """Export human-readable documentation of test cases"""
        with open(output_file, 'w') as f:
            f.write("# Conversation Flow Test Cases\n\n")
            f.write(f"Generated: {test_suite['metadata']['generated_at']}\n\n")
            f.write("## Summary\n\n")
            
            stats = test_suite['statistics']
            f.write(f"- Total Tests: {stats['total_tests']}\n")
            f.write(f"- Conversation Flow Tests: {stats['conversation_flow_tests']}\n")
            f.write(f"- Edge Case Tests: {stats['edge_case_tests']}\n")
            f.write(f"- Interruption Tests: {stats['interruption_tests']}\n")
            f.write(f"- Unique Intents: {stats['unique_intents']}\n\n")
            
            f.write("## Test Cases\n\n")
            
            current_intent = None
            for test in test_suite['conversation_tests']:
                if test['intent'] != current_intent:
                    current_intent = test['intent']
                    f.write(f"\n### {current_intent}\n\n")
                
                f.write(f"#### {test['description']}\n\n")
                
                for turn in test['turns']:
                    f.write(f"**Turn {turn['turn']}:**\n")
                    f.write(f"- User: `{turn.get('user_input', 'N/A')}`\n")
                    
                    if 'expected_intent' in turn:
                        f.write(f"- Expected Intent: `{turn['expected_intent']}`\n")
                    
                    if 'expected_response' in turn:
                        f.write(f"- Expected Response: `{turn['expected_response']}`\n")
                    
                    if 'expected_quick_replies' in turn and turn['expected_quick_replies']:
                        f.write(f"- Expected Quick Replies: {', '.join(turn['expected_quick_replies'])}\n")
                    
                    if 'expected_response_content' in turn:
                        content = turn['expected_response_content'][:200] + '...' if len(turn['expected_response_content']) > 200 else turn['expected_response_content']
                        f.write(f"- Expected Content: \"{content}\"\n")
                    
                    if 'expected_behavior' in turn:
                        f.write(f"- Expected Behavior: {turn['expected_behavior']}\n")
                    
                    f.write("\n")
        
        logger.info(f"Exported test documentation to {output_file}")


def main():
    """Main function"""
    generator = ConversationFlowTestGenerator()
    
    logger.info("Loading data...")
    generator.load_data()
    
    logger.info("Generating conversation flow tests...")
    test_suite = generator.generate_comprehensive_flow_tests()
    
    # Print statistics
    stats = test_suite['statistics']
    logger.info("\nConversation Flow Test Statistics:")
    logger.info(f"  Total Tests: {stats['total_tests']}")
    logger.info(f"  Conversation Flow Tests: {stats['conversation_flow_tests']}")
    logger.info(f"  Edge Case Tests: {stats['edge_case_tests']}")
    logger.info(f"  Interruption Tests: {stats['interruption_tests']}")
    logger.info(f"  Unique Intents Covered: {stats['unique_intents']}")
    logger.info(f"  Total Conversation Turns: {stats['total_turns']}")
    
    # Export to files
    generator.export_to_csv(test_suite)
    generator.export_to_json(test_suite)
    generator.export_test_documentation(test_suite)
    
    logger.info("\nConversation flow test generation completed!")
    
    # Show sample test
    if test_suite['conversation_tests']:
        logger.info("\nSample conversation flow test:")
        sample = test_suite['conversation_tests'][0]
        logger.info(f"Intent: {sample['intent']}")
        for turn in sample['turns']:
            logger.info(f"  Turn {turn['turn']}: {turn.get('user_input', 'N/A')} → {turn.get('expected_response', 'N/A')}")


if __name__ == '__main__':
    main()