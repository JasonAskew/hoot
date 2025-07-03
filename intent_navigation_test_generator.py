#!/usr/bin/env python3
"""
Intent Navigation Test Generator
Generates test cases for intent navigation through quick reply buttons
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class IntentNavigationTestGenerator:
    """Generate test cases for intent navigation flows"""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path)
        self.intents = {}
        self.responses = {}
        self.navigation_tests = []
        
        # Intent patterns to exclude (feedback, survey, thumbs up/down)
        self.excluded_patterns = [
            r'feedback',
            r'survey', 
            r'thumbs',
            r'rating',
            r'csat',
            r'nps',
            r'binary'
        ]
        
    def load_data(self):
        """Load all necessary data"""
        self._load_intents()
        self._load_responses()
        
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
    
    def should_exclude_intent(self, intent_name: str) -> bool:
        """Check if intent should be excluded based on patterns"""
        intent_lower = intent_name.lower()
        for pattern in self.excluded_patterns:
            if re.search(pattern, intent_lower):
                return True
        return False
    
    def extract_intent_quick_replies(self, response_data: Dict) -> List[Dict]:
        """Extract quick replies that navigate to other intents"""
        intent_quick_replies = []
        
        # Check default response
        default_response = response_data.get('default_response', {})
        self._extract_from_response(default_response, intent_quick_replies, 'default')
        
        # Check segment responses
        segment_responses = response_data.get('segment_responses', [])
        for seg_resp in segment_responses:
            segment_name = seg_resp.get('segment_name', '')
            response = seg_resp.get('response', {})
            self._extract_from_response(response, intent_quick_replies, segment_name)
        
        return intent_quick_replies
    
    def _extract_from_response(self, response: Dict, intent_quick_replies: List, segment: str):
        """Extract intent quick replies from a response structure"""
        # Check quick_replies
        quick_replies = response.get('quick_replies', [])
        for qr in quick_replies:
            if qr.get('type') == 'INTENT' and qr.get('intent', {}).get('name'):
                intent_name = qr['intent']['name']
                if not self.should_exclude_intent(intent_name):
                    intent_quick_replies.append({
                        'type': 'quick_reply',
                        'intent': intent_name,
                        'label': qr.get('label', ''),
                        'payload': qr.get('payload', ''),
                        'segment': segment
                    })
        
        # Check message_contents for BUTTON type with INTENT
        message_contents = response.get('message_contents', [])
        for content in message_contents:
            if content.get('type') == 'BUTTON':
                payload = content.get('payload', {})
                if payload.get('type') == 'INTENT' and payload.get('intent', {}).get('name'):
                    intent_name = payload['intent']['name']
                    if not self.should_exclude_intent(intent_name):
                        intent_quick_replies.append({
                            'type': 'button',
                            'intent': intent_name,
                            'label': payload.get('label', ''),
                            'payload': payload.get('label', ''),  # For buttons, payload is usually the label
                            'segment': segment
                        })
    
    def find_responses_with_intent_navigation(self) -> Dict[str, List[Dict]]:
        """Find all responses that have intent navigation"""
        navigation_map = {}
        
        for response_name, response_data in self.responses.items():
            intent_quick_replies = self.extract_intent_quick_replies(response_data)
            
            if intent_quick_replies:
                navigation_map[response_name] = intent_quick_replies
                logger.info(f"Found {len(intent_quick_replies)} intent navigations in {response_name}")
        
        return navigation_map
    
    def find_intent_response_mapping(self) -> Dict[str, str]:
        """Map intents to their primary response names"""
        intent_response_map = {}
        
        for intent_name, intent_data in self.intents.items():
            # Check webhook_params for response_name
            webhook_params = intent_data.get('webhook_params', {})
            response_name = webhook_params.get('response_name')
            
            if response_name:
                intent_response_map[intent_name] = response_name
            else:
                # Try common patterns
                if f"{intent_name}_response" in self.responses:
                    intent_response_map[intent_name] = f"{intent_name}_response"
                elif intent_name in self.responses:
                    intent_response_map[intent_name] = intent_name
        
        return intent_response_map
    
    def get_intent_trigger(self, intent_name: str) -> str:
        """Get a trigger phrase for an intent"""
        intent_data = self.intents.get(intent_name, {})
        
        # Try display_sentence first
        if 'display_sentence' in intent_data:
            return intent_data['display_sentence']
        
        # Try to load from intent_data file
        intent_data_file = self.base_path / 'intent_data' / f'intent_data_{intent_name.lower()}.json'
        
        if intent_data_file.exists():
            try:
                with open(intent_data_file, 'r') as f:
                    data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    for item in data:
                        if item.get('trigger_sentence'):
                            # Clean entity placeholders
                            trigger = item['trigger_sentence']
                            trigger = re.sub(r'{@\w+\s+([^}]+)}', r'\1', trigger)
                            return trigger
            except:
                pass
        
        # Fallback
        clean_name = intent_name.replace('bt_', '').replace('_', ' ')
        return f"help with {clean_name}"
    
    def generate_navigation_tests(self) -> List[Dict]:
        """Generate test cases for all intent navigation flows"""
        navigation_tests = []
        navigation_map = self.find_responses_with_intent_navigation()
        intent_response_map = self.find_intent_response_mapping()
        
        # For each intent, find its response and check for navigations
        for intent_name, intent_data in self.intents.items():
            # Find the response for this intent
            response_name = intent_response_map.get(intent_name)
            if not response_name:
                continue
            
            # Check if this response has intent navigations
            if response_name in navigation_map:
                navigations = navigation_map[response_name]
                
                # Get initial trigger
                initial_trigger = self.get_intent_trigger(intent_name)
                
                # Create test for each navigation
                for nav in navigations:
                    target_intent = nav['intent']
                    button_label = nav['label']
                    nav_type = nav['type']
                    segment = nav['segment']
                    
                    # Find expected response for target intent
                    target_response_name = intent_response_map.get(target_intent)
                    if not target_response_name:
                        logger.warning(f"No response found for target intent {target_intent}")
                        continue
                    
                    # Get expected response content
                    target_response_data = self.responses.get(target_response_name, {})
                    expected_content = self._extract_response_text(target_response_data, segment)
                    
                    # Create navigation test
                    test_case = {
                        'test_type': 'intent_navigation',
                        'source_intent': intent_name,
                        'source_response': response_name,
                        'target_intent': target_intent,
                        'target_response': target_response_name,
                        'navigation_type': nav_type,
                        'segment': segment,
                        'turns': [
                            {
                                'turn': 1,
                                'user_input': initial_trigger,
                                'expected_intent': intent_name,
                                'expected_response': response_name,
                                'expected_navigation_options': [n['label'] for n in navigations]
                            },
                            {
                                'turn': 2,
                                'user_input': button_label,
                                'user_action': f"click_{nav_type}",
                                'expected_intent': target_intent,
                                'expected_response': target_response_name,
                                'expected_response_content': expected_content
                            }
                        ],
                        'description': f"Navigate from {intent_name} to {target_intent} via '{button_label}' {nav_type}"
                    }
                    
                    navigation_tests.append(test_case)
                    logger.info(f"Generated test: {intent_name} → '{button_label}' → {target_intent}")
        
        return navigation_tests
    
    def _extract_response_text(self, response_data: Dict, segment: str = 'default') -> str:
        """Extract text content from response data for a specific segment"""
        if not response_data:
            return ""
        
        # First try segment-specific response
        if segment != 'default':
            segment_responses = response_data.get('segment_responses', [])
            for seg_resp in segment_responses:
                if seg_resp.get('segment_name') == segment:
                    response = seg_resp.get('response', {})
                    text = self._extract_text_from_response(response)
                    if text:
                        return text
        
        # Fall back to default response
        default_response = response_data.get('default_response', {})
        return self._extract_text_from_response(default_response)
    
    def _extract_text_from_response(self, response: Dict) -> str:
        """Extract text from a response structure"""
        message_contents = response.get('message_contents', [])
        texts = []
        
        for content in message_contents:
            if content.get('type') == 'TEXT':
                text = content.get('payload', {}).get('text', '')
                if text:
                    texts.append(text)
        
        return ' '.join(texts)
    
    def generate_comprehensive_navigation_tests(self):
        """Generate comprehensive intent navigation test suite"""
        logger.info("Generating intent navigation tests...")
        
        # Generate basic navigation tests
        navigation_tests = self.generate_navigation_tests()
        
        # Add multi-hop navigation tests (A → B → C)
        multi_hop_tests = self._generate_multi_hop_tests(navigation_tests)
        navigation_tests.extend(multi_hop_tests)
        
        # Add edge cases
        edge_cases = self._generate_navigation_edge_cases(navigation_tests)
        navigation_tests.extend(edge_cases)
        
        # Remove duplicates
        unique_tests = self._deduplicate_tests(navigation_tests)
        
        return {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_responses_scanned': len(self.responses),
                'total_intents': len(self.intents),
                'total_navigation_tests': len(unique_tests)
            },
            'navigation_tests': unique_tests,
            'statistics': self._calculate_statistics(unique_tests)
        }
    
    def _generate_multi_hop_tests(self, base_tests: List[Dict]) -> List[Dict]:
        """Generate tests for multi-hop navigation (A → B → C)"""
        multi_hop_tests = []
        
        # Create a map of target intents to their navigations
        intent_to_navigations = {}
        for test in base_tests:
            target_intent = test['target_intent']
            if target_intent not in intent_to_navigations:
                intent_to_navigations[target_intent] = []
            intent_to_navigations[target_intent].append(test)
        
        # Find chains
        for test in base_tests[:10]:  # Limit to prevent explosion
            target_intent = test['target_intent']
            
            # Check if the target intent has its own navigations
            if target_intent in intent_to_navigations:
                for next_test in intent_to_navigations[target_intent][:2]:  # Limit chains
                    # Create 3-turn test
                    multi_hop = {
                        'test_type': 'multi_hop_navigation',
                        'chain': [test['source_intent'], target_intent, next_test['target_intent']],
                        'turns': [
                            test['turns'][0],  # Initial trigger
                            test['turns'][1],  # First navigation
                            {
                                'turn': 3,
                                'user_input': next_test['turns'][1]['user_input'],
                                'user_action': next_test['turns'][1]['user_action'],
                                'expected_intent': next_test['target_intent'],
                                'expected_response': next_test['target_response']
                            }
                        ],
                        'description': f"Multi-hop: {test['source_intent']} → {target_intent} → {next_test['target_intent']}"
                    }
                    multi_hop_tests.append(multi_hop)
        
        return multi_hop_tests
    
    def _generate_navigation_edge_cases(self, base_tests: List[Dict]) -> List[Dict]:
        """Generate edge cases for navigation testing"""
        edge_cases = []
        
        # Select a few tests for edge cases
        for test in base_tests[:5]:
            # Edge case: Navigate then go back
            back_test = {
                'test_type': 'navigation_back',
                'base_test': test['source_intent'],
                'turns': [
                    test['turns'][0],
                    test['turns'][1],
                    {
                        'turn': 3,
                        'user_input': 'go back',
                        'expected_behavior': 'Handle back navigation or context switch'
                    }
                ],
                'description': f"Navigate then go back: {test['source_intent']} → {test['target_intent']} → back"
            }
            edge_cases.append(back_test)
        
        return edge_cases
    
    def _deduplicate_tests(self, tests: List[Dict]) -> List[Dict]:
        """Remove duplicate tests based on key attributes"""
        seen = set()
        unique = []
        
        for test in tests:
            # Create a key from source, target, and navigation type
            if 'source_intent' in test and 'target_intent' in test:
                key = (
                    test.get('source_intent'),
                    test.get('target_intent'),
                    test.get('navigation_type', ''),
                    test.get('segment', 'default')
                )
            else:
                # For multi-hop or edge cases
                key = (test.get('test_type'), test.get('description'))
            
            if key not in seen:
                seen.add(key)
                unique.append(test)
        
        return unique
    
    def _calculate_statistics(self, tests: List[Dict]) -> Dict:
        """Calculate statistics about the test suite"""
        stats = {
            'total_tests': len(tests),
            'intent_navigation_tests': len([t for t in tests if t.get('test_type') == 'intent_navigation']),
            'multi_hop_tests': len([t for t in tests if t.get('test_type') == 'multi_hop_navigation']),
            'edge_case_tests': len([t for t in tests if 'edge' in t.get('test_type', '') or 'back' in t.get('test_type', '')]),
            'unique_source_intents': len(set(t.get('source_intent', '') for t in tests if t.get('source_intent'))),
            'unique_target_intents': len(set(t.get('target_intent', '') for t in tests if t.get('target_intent'))),
            'by_navigation_type': {}
        }
        
        # Count by navigation type
        for test in tests:
            nav_type = test.get('navigation_type', 'unknown')
            stats['by_navigation_type'][nav_type] = stats['by_navigation_type'].get(nav_type, 0) + 1
        
        return stats
    
    def export_to_csv(self, test_suite: Dict, output_file: str = 'intent_navigation_tests.csv'):
        """Export navigation tests to CSV format"""
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'test_id', 'test_type', 'source_intent', 'target_intent',
                'navigation_type', 'segment', 'turn_1_input', 'turn_2_input',
                'expected_final_response', 'description'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            test_id = 1
            for test in test_suite['navigation_tests']:
                if test.get('test_type') == 'intent_navigation':
                    writer.writerow({
                        'test_id': f'INT_{test_id:04d}',
                        'test_type': test['test_type'],
                        'source_intent': test.get('source_intent', ''),
                        'target_intent': test.get('target_intent', ''),
                        'navigation_type': test.get('navigation_type', ''),
                        'segment': test.get('segment', 'default'),
                        'turn_1_input': test['turns'][0]['user_input'],
                        'turn_2_input': test['turns'][1]['user_input'],
                        'expected_final_response': test.get('target_response', ''),
                        'description': test['description']
                    })
                test_id += 1
        
        logger.info(f"Exported {test_id - 1} intent navigation tests to {output_file}")
    
    def export_to_json(self, test_suite: Dict, output_file: str = 'intent_navigation_tests.json'):
        """Export test suite to JSON format"""
        with open(output_file, 'w') as f:
            json.dump(test_suite, f, indent=2)
        
        logger.info(f"Exported intent navigation test suite to {output_file}")
    
    def export_navigation_map(self, output_file: str = 'intent_navigation_map.md'):
        """Export a visual map of intent navigations"""
        navigation_map = self.find_responses_with_intent_navigation()
        intent_response_map = self.find_intent_response_mapping()
        
        with open(output_file, 'w') as f:
            f.write("# Intent Navigation Map\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Group by source intent
            intent_navigations = {}
            for response_name, navigations in navigation_map.items():
                # Find intent for this response
                source_intent = None
                for intent, resp in intent_response_map.items():
                    if resp == response_name:
                        source_intent = intent
                        break
                
                if source_intent:
                    intent_navigations[source_intent] = navigations
            
            # Write navigation flows
            f.write("## Navigation Flows\n\n")
            for intent, navigations in sorted(intent_navigations.items()):
                f.write(f"### {intent}\n\n")
                for nav in navigations:
                    nav_type = "button" if nav['type'] == 'button' else "quick reply"
                    segment = f" [{nav['segment']}]" if nav['segment'] != 'default' else ""
                    f.write(f"- **{nav['label']}** ({nav_type}{segment}) → `{nav['intent']}`\n")
                f.write("\n")
            
            # Write statistics
            f.write("## Statistics\n\n")
            f.write(f"- Total intents with navigations: {len(intent_navigations)}\n")
            f.write(f"- Total navigation links: {sum(len(navs) for navs in intent_navigations.values())}\n")
        
        logger.info(f"Exported navigation map to {output_file}")


def main():
    """Main function"""
    generator = IntentNavigationTestGenerator()
    
    logger.info("Loading data...")
    generator.load_data()
    
    logger.info("Generating intent navigation tests...")
    test_suite = generator.generate_comprehensive_navigation_tests()
    
    # Print statistics
    stats = test_suite['statistics']
    logger.info("\nIntent Navigation Test Statistics:")
    logger.info(f"  Total Tests: {stats['total_tests']}")
    logger.info(f"  Intent Navigation Tests: {stats['intent_navigation_tests']}")
    logger.info(f"  Multi-hop Tests: {stats['multi_hop_tests']}")
    logger.info(f"  Edge Case Tests: {stats['edge_case_tests']}")
    logger.info(f"  Unique Source Intents: {stats['unique_source_intents']}")
    logger.info(f"  Unique Target Intents: {stats['unique_target_intents']}")
    
    logger.info("\nNavigation Types:")
    for nav_type, count in stats['by_navigation_type'].items():
        logger.info(f"  {nav_type}: {count}")
    
    # Export to files
    generator.export_to_csv(test_suite)
    generator.export_to_json(test_suite)
    generator.export_navigation_map()
    
    logger.info("\nIntent navigation test generation completed!")
    
    # Show sample test
    if test_suite['navigation_tests']:
        logger.info("\nSample intent navigation test:")
        sample = test_suite['navigation_tests'][0]
        logger.info(f"Type: {sample.get('test_type')}")
        logger.info(f"Description: {sample.get('description')}")
        if 'turns' in sample:
            for turn in sample['turns']:
                logger.info(f"  Turn {turn.get('turn', 'N/A')}: {turn.get('user_input', 'N/A')}")


if __name__ == '__main__':
    main()