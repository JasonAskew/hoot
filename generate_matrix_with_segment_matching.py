#!/usr/bin/env python3
"""
Enhanced Matrix Generator with Segment Matching Logic
Correctly resolves responses based on meta field matching and list order
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import logging
from segment_intent_validator import SegmentIntentValidator

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class SegmentMatchingMatrixGenerator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.segments = {}
        self.intents = {}
        self.responses = {}
        self.profiles = {}  # Store profile metadata
        self.segment_rules = {}  # Store segment matching rules
        self.validator = SegmentIntentValidator(base_path)  # Initialize the validator
        
    def load_all_data(self):
        """Load all data from files including profiles"""
        logger.info("Loading data from files...")
        
        # Load segments
        segments_path = self.base_path / 'segments'
        if segments_path.exists():
            for file in segments_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        self.segments[name] = data
                except Exception as e:
                    logger.error(f"Error loading segment {file}: {e}")
        
        logger.info(f"  Loaded {len(self.segments)} segments")
        
        # Load profiles to understand meta fields
        profiles_path = self.base_path / 'profiles'
        if profiles_path.exists():
            for file in profiles_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        content = f.read().strip()
                        # Handle various profile file formats
                        if content.startswith('"meta_fields":'):
                            content = '{' + content + '}'
                        elif content.startswith('meta_fields'):
                            content = '{"' + content + '}'
                        
                        data = json.loads(content)
                        profile_name = file.stem
                        self.profiles[profile_name] = data.get('meta_fields', [])
                        
                        # Derive segment rules from profile data
                        self._derive_segment_rules(profile_name, data.get('meta_fields', []))
                        
                except Exception as e:
                    logger.error(f"Error loading profile {file}: {e}")
        
        logger.info(f"  Loaded {len(self.profiles)} profiles")
        
        # Load intents
        intents_path = self.base_path / 'intents'
        if intents_path.exists():
            for file in intents_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        self.intents[name] = data
                except Exception as e:
                    logger.error(f"Error loading intent {file}: {e}")
        
        logger.info(f"  Loaded {len(self.intents)} intents")
        
        # Load responses
        responses_path = self.base_path / 'responses'
        if responses_path.exists():
            for file in responses_path.glob('*.json'):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        name = data.get('name', file.stem)
                        self.responses[name] = data
                except Exception as e:
                    logger.error(f"Error loading response {file}: {e}")
        
        logger.info(f"  Loaded {len(self.responses)} responses")
    
    def _derive_segment_rules(self, segment_name: str, meta_fields: List[Dict]):
        """Derive segment matching rules from profile metadata"""
        # Build a rule set for this segment based on its meta fields
        rules = {}
        for field in meta_fields:
            key = field.get('key') or field.get('name')
            value = field.get('value')
            if key and value:
                rules[key] = value
        
        if rules:
            self.segment_rules[segment_name] = rules
            logger.debug(f"Segment rules for {segment_name}: {rules}")
    
    def does_profile_match_segment(self, test_profile_name: str, segment_name: str) -> bool:
        """Check if a test profile matches a segment based on meta fields"""
        # Get the test profile's meta fields
        test_meta_fields = self.profiles.get(test_profile_name, [])
        test_meta_dict = {}
        for field in test_meta_fields:
            key = field.get('key') or field.get('name')
            value = field.get('value')
            if key and value:
                test_meta_dict[key] = value
        
        # Get the segment's required fields
        segment_rules = self.segment_rules.get(segment_name, {})
        
        # Check if all segment requirements are met
        for key, required_value in segment_rules.items():
            if test_meta_dict.get(key) != required_value:
                return False
        
        return True
    
    def get_intent_response_name(self, intent_name: str) -> Optional[str]:
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
        
        return None
    
    def is_clarification_intent(self, intent_name: str) -> bool:
        """Check if an intent is a ClarificationIntent"""
        intent = self.intents.get(intent_name, {})
        return intent.get('webhook_name', '') == 'ClarificationIntent'
    
    def resolve_response_for_profile(self, response_name: str, test_profile_name: str) -> Tuple[Dict, str]:
        """
        Resolve the actual response for a profile based on segment matching rules.
        Uses most-specific-first logic to match CAPI behavior.
        Returns (response_data, response_type)
        """
        if response_name not in self.responses:
            return {}, "N/A"
        
        response_data = self.responses[response_name]
        default_response = response_data.get('default_response', {})
        segment_responses = response_data.get('segment_responses', [])
        
        # Find all matching segments for this profile
        matching_segments = []
        for seg_resp in segment_responses:
            segment_name = seg_resp.get('segment_name')
            if segment_name and self.does_profile_match_segment(test_profile_name, segment_name):
                matching_segments.append((seg_resp, segment_name))
        
        if matching_segments:
            # Use FIRST matching segment (order in response file matters)
            # CAPI returns the first segment response that matches the profile
            first_match = matching_segments[0][0]  # Get the seg_resp from the tuple
            first_segment_name = matching_segments[0][1]
            
            return first_match.get('response', {}), f"Segment-specific ({first_segment_name})"
        
        # Otherwise, use default
        return default_response, "Default"
    
    def get_example_trigger(self, intent_name: str) -> Optional[str]:
        """Get an example trigger for an intent from intent_data files.
        Returns None if no valid intent_data file exists."""
        # Try different naming patterns for intent_data files
        intent_name_lower = intent_name.lower()
        possible_files = [
            self.base_path / 'intent_data' / f'{intent_name_lower}_train.json',
            self.base_path / 'intent_data' / f'{intent_name_lower}_test.json',
            self.base_path / 'intent_data' / f'{intent_name_lower}_seed.json',
            self.base_path / 'intent_data' / f'intent_data_{intent_name}.json'
        ]
        
        intent_data_file = None
        for possible_file in possible_files:
            if possible_file.exists():
                intent_data_file = possible_file
                break
        
        if intent_data_file and intent_data_file.exists():
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
                
                # The data contains an array of trigger objects
                if isinstance(data, list) and len(data) > 0:
                    # Find the first active trigger
                    for item in data:
                        if item.get('active', True) and item.get('type') == 'TRIGGER':
                            trigger = item.get('trigger_sentence', '')
                            if trigger:
                                # Clean up entity placeholders
                                import re
                                trigger = re.sub(r'{@\w+\s+([^}]+)}', r'\1', trigger)
                                return trigger
                    
                    # If no active trigger found, use the first one
                    if data[0].get('trigger_sentence'):
                        trigger = data[0]['trigger_sentence']
                        import re
                        trigger = re.sub(r'{@\w+\s+([^}]+)}', r'\1', trigger)
                        return trigger
            except Exception as e:
                logger.warning(f"Error reading intent_data for {intent_name}: {e}")
        
        # No valid intent_data file - return None to indicate invalid test
        return None
    
    def extract_response_text(self, response_data: Dict) -> Dict:
        """Extract text and buttons from response data structure"""
        if not response_data:
            return {"text": "N/A", "buttons": []}
        
        message_contents = response_data.get('message_contents', [])
        texts = []
        buttons = []
        
        for content in message_contents:
            if content.get('type') == 'TEXT':
                text = content.get('payload', {}).get('text', '')
                if text:
                    # Clean up but don't truncate
                    text = text.replace('\n', ' ').strip()
                    texts.append(text)
            elif content.get('type') == 'BUTTON':
                label = content.get('payload', {}).get('label', '')
                if label:
                    buttons.append(label)
        
        # Also check for quick_replies
        quick_replies = response_data.get('quick_replies', [])
        if quick_replies:
            qr_labels = [qr.get('label', '') for qr in quick_replies]
            buttons.extend(qr_labels)
        
        text_content = " ".join(texts) if texts else "N/A"
        return {"text": text_content, "buttons": buttons}
    
    def _generate_hoot_rows(self, segment_name: str, intent_name: str, example_trigger: str, 
                           response_text: str, response_buttons: List[str], response_data: Dict,
                           test_case_summary_id: int, test_case_detail_id: int, step_id: int) -> List[Dict]:
        """Generate hoot format rows for a single test case"""
        rows = []
        current_detail_id = test_case_detail_id
        current_step_id = step_id
        
        # Default meta tags for segment
        meta_tags = f'[{{"key":"semantic_group:","value":"default"}},{{"key":"semantic_group_secondary:","value":"default"}}]'
        
        # Test case name
        test_case_name = f"{segment_name.upper()}_{intent_name}_Response"
        
        # Row 1: start-session
        rows.append({
            'test_plan_name': segment_name.upper(),
            'run_time': '',
            'run_schedule': 'null',
            'testing_phase': 'Baseline',
            'endpoint_id': '85',
            'endpoint_type': 'Kasisto',
            'test_case_summary_id': test_case_summary_id,
            'test_case_name': test_case_name,
            'test_case_type': 'BASELINE',
            'active': 'TRUE',
            'test_case_detail_id': current_detail_id,
            'step_id': current_step_id,
            'action': 'start-session',
            'object': 'event',
            'value': 'start-session',
            'meta_tags': meta_tags
        })
        current_detail_id += 1
        current_step_id += 1
        
        # Row 2: user-input
        rows.append({
            'test_plan_name': segment_name.upper(),
            'run_time': '',
            'run_schedule': 'null',
            'testing_phase': 'Baseline',
            'endpoint_id': '85',
            'endpoint_type': 'Kasisto',
            'test_case_summary_id': test_case_summary_id,
            'test_case_name': test_case_name,
            'test_case_type': 'BASELINE',
            'active': 'TRUE',
            'test_case_detail_id': current_detail_id,
            'step_id': current_step_id,
            'action': 'user-input',
            'object': 'text',
            'value': example_trigger,
            'meta_tags': meta_tags
        })
        current_detail_id += 1
        current_step_id += 1
        
        # Row 3+: object-semantics for text response
        if response_text and response_text != "N/A":
            # Find the correct JSON path for the text
            text_path = self._find_text_json_path(response_data)
            rows.append({
                'test_plan_name': segment_name.upper(),
                'run_time': '',
                'run_schedule': 'null',
                'testing_phase': 'Baseline',
                'endpoint_id': '85',
                'endpoint_type': 'Kasisto',
                'test_case_summary_id': test_case_summary_id,
                'test_case_name': test_case_name,
                'test_case_type': 'BASELINE',
                'active': 'TRUE',
                'test_case_detail_id': current_detail_id,
                'step_id': current_step_id,
                'action': 'object-semantics',
                'object': text_path,
                'value': response_text,
                'meta_tags': meta_tags
            })
            current_detail_id += 1
            current_step_id += 1
        
        # Rows 4+: object-semantics for each button/quick reply
        if response_buttons:
            button_paths = self._find_button_json_paths(response_data, len(response_buttons))
            for i, (button_text, button_path) in enumerate(zip(response_buttons, button_paths)):
                rows.append({
                    'test_plan_name': segment_name.upper(),
                    'run_time': '',
                    'run_schedule': 'null',
                    'testing_phase': 'Baseline',
                    'endpoint_id': '85',
                    'endpoint_type': 'Kasisto',
                    'test_case_summary_id': test_case_summary_id,
                    'test_case_name': test_case_name,
                    'test_case_type': 'BASELINE',
                    'active': 'TRUE',
                    'test_case_detail_id': current_detail_id,
                    'step_id': current_step_id,
                    'action': 'object-semantics',
                    'object': button_path,
                    'value': button_text,
                    'meta_tags': meta_tags
                })
                current_detail_id += 1
                current_step_id += 1
        
        return rows
    
    def _find_text_json_path(self, response_data: Dict) -> str:
        """Find the correct JSON path for text content in response"""
        if not response_data:
            return "message_contents[0].payload.text"
        
        message_contents = response_data.get('message_contents', [])
        for i, content in enumerate(message_contents):
            if content.get('type') == 'TEXT':
                return f"message_contents[{i}].payload.text"
        
        # Default fallback
        return "message_contents[0].payload.text"
    
    def _find_button_json_paths(self, response_data: Dict, button_count: int) -> List[str]:
        """Find the correct JSON paths for buttons/quick replies"""
        paths = []
        
        if not response_data:
            # Default paths for buttons
            for i in range(button_count):
                paths.append(f"quick_replies[{i}].label")
            return paths
        
        # Check for quick_replies first
        quick_replies = response_data.get('quick_replies', [])
        if quick_replies:
            for i in range(min(button_count, len(quick_replies))):
                paths.append(f"quick_replies[{i}].label")
        
        # Check for BUTTON type in message_contents
        message_contents = response_data.get('message_contents', [])
        button_index = 0
        for i, content in enumerate(message_contents):
            if content.get('type') == 'BUTTON' and len(paths) < button_count:
                paths.append(f"message_contents[{i}].payload.label")
                button_index += 1
        
        # Fill remaining with default paths
        while len(paths) < button_count:
            paths.append(f"quick_replies[{len(paths)}].label")
        
        return paths
    
    def generate_matrix_csv(self, output_file: str, sample_only: bool = False, format_type: str = "standard"):
        """Generate the segment-intent matrix CSV with correct response resolution
        
        Args:
            output_file: Output CSV file path
            sample_only: If True, generate only a subset for testing
            format_type: Either 'standard' or 'hoot' format
        """
        csv_data = []
        invalid_tests = []
        
        # Initialize counters for hoot format
        if format_type == "hoot":
            test_case_summary_id = 3575  # Starting ID from example
            test_case_detail_id = 7364   # Starting ID from example
            step_id_counter = 0
        
        # Sort for consistent output
        segment_names = sorted(self.segments.keys())
        intent_names = sorted(self.intents.keys())
        
        if sample_only:
            # Limit to subset for sample
            segment_names = segment_names[:5]
            intent_names = intent_names[:20]
            logger.info(f"Generating sample with {len(segment_names)} segments x {len(intent_names)} intents")
        else:
            logger.info(f"Generating full matrix with {len(segment_names)} segments x {len(intent_names)} intents")
        
        # Log segment matching rules for debugging
        logger.info("\nSegment matching rules:")
        for seg, rules in sorted(self.segment_rules.items()):
            logger.info(f"  {seg}: {rules}")
        
        for segment_name in segment_names:
            segment = self.segments[segment_name]
            disabled_actions = set(segment.get('disabled_actions', []))
            
            for intent_name in intent_names:
                intent = self.intents[intent_name]
                
                # Use validator to check if intent is enabled (includes global segment check)
                validation_result = self.validator.validate_test_case(intent_name, segment_name)
                is_enabled = validation_result['valid']
                is_globally_disabled = validation_result.get('reason') == 'intent_disabled_globally'
                
                # Check if intent is active
                is_intent_active = intent.get('active', True)
                
                # Get example trigger
                example_trigger = self.get_example_trigger(intent_name)
                
                # Check if we have valid intent data
                has_valid_intent_data = example_trigger is not None
                
                # Get response using correct resolution logic
                response_text = "N/A"
                response_buttons = []
                response_type = "N/A"
                
                if is_enabled and is_intent_active and has_valid_intent_data:
                    response_name = self.get_intent_response_name(intent_name)
                    if response_name:
                        # Use profile-aware response resolution
                        response_data, response_type = self.resolve_response_for_profile(response_name, segment_name)
                        if response_data:
                            extracted = self.extract_response_text(response_data)
                            response_text = extracted["text"]
                            response_buttons = extracted["buttons"]
                else:
                    if is_globally_disabled:
                        response_text = "Intent disabled globally"
                        response_type = "Globally Disabled"
                    elif not has_valid_intent_data:
                        response_text = "No intent data file"
                        response_type = "No Intent Data"
                        example_trigger = "N/A"
                    elif not is_intent_active:
                        response_text = "Intent is inactive"
                        response_type = "Inactive"
                    else:
                        response_text = "Intent disabled for this segment"
                        response_type = "Disabled"
                
                # Check if this is a valid test case
                is_valid_test = (
                    response_text not in ["N/A", "Intent disabled for this segment", "Intent is inactive", "No intent data file", "Intent disabled globally"] and
                    segment.get('active', True) and
                    is_enabled and
                    is_intent_active and
                    has_valid_intent_data
                )
                
                # Create row data based on format type
                if format_type == "hoot" and is_valid_test:
                    # Generate hoot format rows for this test case
                    hoot_rows = self._generate_hoot_rows(
                        segment_name, intent_name, example_trigger, 
                        response_text, response_buttons, response_data,
                        test_case_summary_id, test_case_detail_id, step_id_counter
                    )
                    csv_data.extend(hoot_rows)
                    
                    # Update counters
                    test_case_summary_id += 1
                    test_case_detail_id += len(hoot_rows)
                    step_id_counter = 0  # Reset for next test case
                    
                elif format_type != "hoot":
                    # Standard format
                    row_data = {
                        'segment': segment_name,
                        'segment_description': segment.get('description', ''),
                        'segment_active': 'Yes' if segment.get('active', True) else 'No',
                        'intent': intent_name,
                        'intent_display_name': intent.get('display_name', intent_name),
                        'intent_active': 'Yes' if is_intent_active else 'No',
                        'enabled_for_segment': 'Yes' if is_enabled else 'No',
                        'example_trigger': example_trigger,
                        'response_type': response_type,
                        'expected_response': response_text,
                        'expected_buttons': '|'.join(response_buttons) if response_buttons else ''
                    }
                    
                    if is_valid_test:
                        csv_data.append(row_data)
                
                # Track invalid tests for standard format only
                if not is_valid_test and format_type != "hoot":
                    invalid_reason = []
                    if response_text == "Intent disabled globally":
                        invalid_reason.append("Intent disabled globally - switched off system-wide")
                    elif response_text == "N/A":
                        invalid_reason.append("No response defined")
                    elif response_text == "Intent disabled for this segment":
                        invalid_reason.append("Intent disabled")
                    elif response_text == "Intent is inactive":
                        invalid_reason.append("Intent is inactive")
                    elif response_text == "No intent data file":
                        invalid_reason.append("No intent data file")
                    
                    if not segment.get('active', True):
                        invalid_reason.append("Segment inactive")
                    if not is_enabled and not is_globally_disabled:
                        invalid_reason.append("Intent not enabled for segment")
                    if not is_intent_active:
                        invalid_reason.append("Intent marked as inactive")
                    if not has_valid_intent_data:
                        invalid_reason.append("No valid intent data (example triggers)")
                    
                    row_data['invalid_reason'] = '; '.join(invalid_reason)
                    invalid_tests.append(row_data)
        
        # Write CSV with format-specific headers
        if format_type == "hoot":
            fieldnames = [
                'test_plan_name', 'run_time', 'run_schedule', 'testing_phase', 'endpoint_id',
                'endpoint_type', 'test_case_summary_id', 'test_case_name', 'test_case_type',
                'active', 'test_case_detail_id', 'step_id', 'action', 'object', 'value', 'meta_tags'
            ]
        else:
            fieldnames = [
                'segment', 'segment_description', 'segment_active', 'intent', 'intent_display_name',
                'intent_active', 'enabled_for_segment', 'example_trigger', 'response_type',
                'expected_response', 'expected_buttons'
            ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        logger.info(f"✅ Generated {output_file} with {len(csv_data)} valid test rows")
        
        # Write invalid tests to separate files
        if invalid_tests:
            self._write_invalid_tests(invalid_tests, output_file)
        
        # Print summary
        self._print_summary(csv_data, len(invalid_tests), format_type)
    
    def _write_invalid_tests(self, invalid_tests: List[Dict], output_file: str):
        """Write invalid tests to separate CSV and markdown files."""
        from pathlib import Path
        from datetime import datetime
        
        base_name = Path(output_file).stem
        
        # Write invalid tests CSV
        invalid_csv = f"{base_name}_invalid_tests.csv"
        invalid_fieldnames = [
            'segment', 'segment_description', 'segment_active', 'intent', 'intent_display_name',
            'intent_active', 'enabled_for_segment', 'example_trigger', 'response_type', 'expected_response', 
            'expected_buttons', 'invalid_reason'
        ]
        
        with open(invalid_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=invalid_fieldnames)
            writer.writeheader()
            writer.writerows(invalid_tests)
        
        logger.info(f"✅ Generated invalid tests report: {invalid_csv}")
    
    def _print_summary(self, csv_data: List[Dict], invalid_count: int, format_type: str = "standard"):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        valid_rows = len(csv_data)
        
        if format_type == "hoot":
            # For hoot format, count test cases (every 3+ rows is one test case)
            test_case_count = len(set(row.get('test_case_summary_id', 0) for row in csv_data))
            print(f"\nHoot format rows generated: {valid_rows}")
            print(f"Test cases represented: {test_case_count}")
            print(f"Average rows per test case: {valid_rows/test_case_count:.1f}" if test_case_count > 0 else "N/A")
            
            # Count action types
            action_types = {}
            for row in csv_data:
                action = row.get('action', 'unknown')
                action_types[action] = action_types.get(action, 0) + 1
            
            print("\nAction type distribution:")
            for action, count in sorted(action_types.items()):
                print(f"  {action}: {count} ({count/valid_rows*100:.1f}%)")
        else:
            # Standard format statistics
            total_combinations = valid_rows + invalid_count
            enabled_count = sum(1 for row in csv_data if row.get('enabled_for_segment') == 'Yes')
            disabled_count = valid_rows - enabled_count
            
            print(f"\nTotal combinations generated: {total_combinations}")
            print(f"Valid test cases: {valid_rows} ({valid_rows/total_combinations*100:.1f}%)")
            print(f"Invalid/excluded test cases: {invalid_count} ({invalid_count/total_combinations*100:.1f}%)")
            print(f"\nOf valid test cases:")
            if valid_rows > 0:
                print(f"  Enabled combinations: {enabled_count} ({enabled_count/valid_rows*100:.1f}%)")
                print(f"  Disabled combinations: {disabled_count} ({disabled_count/valid_rows*100:.1f}%)")
            else:
                print(f"  Enabled combinations: {enabled_count} (N/A%)")
                print(f"  Disabled combinations: {disabled_count} (N/A%)")
            
            # Count response types
            response_types = {}
            for row in csv_data:
                rt = row.get('response_type', 'N/A')
                response_types[rt] = response_types.get(rt, 0) + 1
            
            print("\nResponse type distribution:")
            for rt, count in sorted(response_types.items()):
                print(f"  {rt}: {count} ({count/valid_rows*100:.1f}%)")


def main():
    import sys
    
    # Parse command line arguments
    format_type = "standard"
    if len(sys.argv) > 1 and sys.argv[1] == "--hoot":
        format_type = "hoot"
    
    # Base path for data files
    BASE_PATH = "/Users/jaskew/workspace/Skynet/claude/hoot"
    
    # Create generator
    generator = SegmentMatchingMatrixGenerator(BASE_PATH)
    
    # Load all data
    generator.load_all_data()
    
    if format_type == "hoot":
        # Generate hoot format files
        logger.info("\nGenerating hoot format sample CSV...")
        generator.generate_matrix_csv("hoot_tests_sample.csv", sample_only=True, format_type="hoot")
        
        logger.info("\nGenerating hoot format full CSV...")
        generator.generate_matrix_csv("hoot_tests_full.csv", sample_only=False, format_type="hoot")
        
        print("\n✅ Generated hoot format files:")
        print("  - hoot_tests_sample.csv (subset for review)")
        print("  - hoot_tests_full.csv (complete matrix in hoot format)")
    else:
        # Generate standard format files
        logger.info("\nGenerating sample CSV with segment matching...")
        generator.generate_matrix_csv("segment_intent_matrix_with_matching_sample.csv", sample_only=True)
        
        logger.info("\nGenerating full CSV with segment matching...")
        generator.generate_matrix_csv("segment_intent_matrix_with_matching_full.csv", sample_only=False)
        
        print("\n✅ Generated files with correct segment matching logic:")
        print("  - segment_intent_matrix_with_matching_sample.csv (subset for review)")
        print("  - segment_intent_matrix_with_matching_full.csv (complete matrix)")


if __name__ == "__main__":
    main()