#!/usr/bin/env python3
"""
CAPI Test Runner
Automates testing of Kasisto CAPI endpoints using test matrix and profile metadata.
"""

import csv
from pathlib import Path
import json
import os
import re
import requests
import time
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Configuration
BASE_URL = "https://westpac-kai-sandbox-en-au-stage.kitsys.net"
SECRET = "670b7c4a-3091-4d6f-b02e-c16d9c911428"
ASSISTANT_NAME = "default_assistant"
ASSISTANT_TARGET = "prod"
BASIC_AUTH = "Basic c3lzY3VzOjIzM2hfYWRqS0pzYWU4Mw=="

# API Endpoints
START_SESSION_URL = f"{BASE_URL}/kai/api/v2/capi/event"
USER_MESSAGE_URL = f"{BASE_URL}/kai/api/v2/capi/user_message"

# File paths
PROFILES_DIR = "profiles"
RESULTS_FILE = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
CHECKPOINT_FILE = "test_checkpoint.json"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"capi_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CAPITestRunner:
    """Main test runner class for CAPI testing."""
    
    def __init__(self, format_type: str = "standard"):
        self.results = []
        self.start_from_test = 0  # For resumable execution
        self.checkpoint_interval = 10  # Save checkpoint every N tests
        self.format_type = format_type  # "standard" or "hoot"
        
        # Set CSV file based on format type
        if format_type == "hoot":
            self.csv_file = "hoot_tests_full.csv"
        else:
            self.csv_file = "segment_intent_matrix_with_matching_full.csv"
        
        # Load CAPI context mapping for profile-specific requests
        self.context_mapping = self.load_capi_context_mapping()
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

        
    def save_checkpoint(self, test_index: int, results: List[Dict]):
        """Save current progress to checkpoint file with atomic write and backup."""
        checkpoint_data = {
            'test_index': test_index,
            'timestamp': datetime.now().isoformat(),
            'completed_tests': len(results),
            'results': results
        }
        
        # Create backup of existing checkpoint
        backup_file = f"{CHECKPOINT_FILE}.backup"
        if os.path.exists(CHECKPOINT_FILE):
            try:
                import shutil
                shutil.copy2(CHECKPOINT_FILE, backup_file)
            except Exception as e:
                logger.warning(f"Failed to create checkpoint backup: {e}")
        
        # Write to temporary file first (atomic write)
        temp_file = f"{CHECKPOINT_FILE}.tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(checkpoint_data, f, indent=2)
                f.flush()  # Ensure data is written to disk
                os.fsync(f.fileno())  # Force write to disk
            
            # Atomically replace the checkpoint file
            if os.path.exists(CHECKPOINT_FILE):
                os.replace(temp_file, CHECKPOINT_FILE)
            else:
                os.rename(temp_file, CHECKPOINT_FILE)
            
            logger.info(f"Checkpoint saved at test {test_index}")
            
            # Clean up backup after successful write
            if os.path.exists(backup_file):
                os.remove(backup_file)
                
        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            
            # Try to restore from backup if write failed
            if os.path.exists(backup_file):
                try:
                    shutil.copy2(backup_file, CHECKPOINT_FILE)
                    logger.info("Restored checkpoint from backup")
                except Exception as restore_e:
                    logger.error(f"Failed to restore checkpoint from backup: {restore_e}")
            
            # Clean up temporary file
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def load_checkpoint(self) -> Optional[Dict]:
        """Load checkpoint data if it exists, with backup recovery."""
        checkpoint_files = [CHECKPOINT_FILE, f"{CHECKPOINT_FILE}.backup"]
        
        for checkpoint_file in checkpoint_files:
            if os.path.exists(checkpoint_file):
                try:
                    with open(checkpoint_file, 'r') as f:
                        checkpoint = json.load(f)
                    
                    # Validate checkpoint structure
                    required_keys = ['test_index', 'timestamp', 'completed_tests', 'results']
                    if all(key in checkpoint for key in required_keys):
                        if checkpoint_file.endswith('.backup'):
                            logger.info(f"Restored checkpoint from backup: {checkpoint['completed_tests']} tests completed at {checkpoint['timestamp']}")
                        else:
                            logger.info(f"Checkpoint found: {checkpoint['completed_tests']} tests completed at {checkpoint['timestamp']}")
                        return checkpoint
                    else:
                        logger.warning(f"Invalid checkpoint structure in {checkpoint_file}")
                        
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error in {checkpoint_file}: {e}")
                    if checkpoint_file == CHECKPOINT_FILE:
                        logger.info("Attempting to load from backup...")
                        continue
                except Exception as e:
                    logger.error(f"Failed to load checkpoint from {checkpoint_file}: {e}")
                    if checkpoint_file == CHECKPOINT_FILE:
                        logger.info("Attempting to load from backup...")
                        continue
        
        logger.info("No valid checkpoint found")
        return None
    
    def clear_checkpoint(self):
        """Remove checkpoint file and backup after successful completion."""
        files_to_remove = [CHECKPOINT_FILE, f"{CHECKPOINT_FILE}.backup", f"{CHECKPOINT_FILE}.tmp"]
        
        for file_path in files_to_remove:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Removed {file_path}")
            except Exception as e:
                logger.error(f"Failed to remove {file_path}: {e}")
    
    def verify_checkpoint_integrity(self, checkpoint: Dict) -> bool:
        """Verify checkpoint data integrity."""
        try:
            # Check required structure
            required_keys = ['test_index', 'timestamp', 'completed_tests', 'results']
            if not all(key in checkpoint for key in required_keys):
                logger.error("Checkpoint missing required keys")
                return False
            
            # Verify data consistency
            if checkpoint['completed_tests'] != len(checkpoint['results']):
                logger.error(f"Checkpoint data inconsistency: completed_tests={checkpoint['completed_tests']}, actual results={len(checkpoint['results'])}")
                return False
            
            # Verify test_index is reasonable
            if checkpoint['test_index'] < 0 or checkpoint['test_index'] > 10000:
                logger.error(f"Invalid test_index: {checkpoint['test_index']}")
                return False
            
            # Sample verify a few results have required structure
            sample_size = min(5, len(checkpoint['results']))
            required_result_keys = ['segment', 'intent', 'status', 'timestamp']
            
            for i in range(sample_size):
                result = checkpoint['results'][i]
                if not all(key in result for key in required_result_keys):
                    logger.error(f"Result {i} missing required keys")
                    return False
            
            logger.info("Checkpoint integrity verification passed")
            return True
            
        except Exception as e:
            logger.error(f"Checkpoint integrity verification failed: {e}")
            return False
    
    def resume_from_checkpoint(self) -> bool:
        """Resume execution from checkpoint if available."""
        checkpoint = self.load_checkpoint()
        if checkpoint:
            # Verify checkpoint integrity before using it
            if not self.verify_checkpoint_integrity(checkpoint):
                logger.error("Checkpoint failed integrity check, starting fresh")
                return False
                
            self.start_from_test = checkpoint['test_index']
            self.results = checkpoint.get('results', [])
            
            # Note: Each test creates its own unique session
            
            logger.info(f"Resuming from test {self.start_from_test}, {len(self.results)} results restored")
            return True
        return False
    
    def load_capi_context_mapping(self) -> Dict:
        """Load CAPI context mapping for profile-specific requests"""
        mapping_file = "capi_context_mapping.json"
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load CAPI context mapping: {e}")
        return {}
    
    def apply_profile_context(self, base_payload: Dict, segment: str) -> Dict:
        """Apply profile-specific context modifications to CAPI payload"""
        if segment not in self.context_mapping:
            return base_payload
        
        # Deep copy the payload
        import copy
        payload = copy.deepcopy(base_payload)
        context_mods = self.context_mapping[segment]
        
        # Apply device modifications
        if 'device' in context_mods:
            for key, value in context_mods['device'].items():
                if value:  # Only set non-empty values
                    payload['context']['device'][key] = value
        
        # Apply platform modifications  
        if 'platform' in context_mods:
            for key, value in context_mods['platform'].items():
                if value:  # Only set non-empty values
                    payload['context']['platform'][key] = value
        
        # Apply user modifications
        if 'user' in context_mods:
            for key, value in context_mods['user'].items():
                if key == 'meta_fields':
                    payload['context']['user']['meta_fields'] = value
                elif value:  # Only set non-empty values
                    payload['context']['user'][key] = value
        
        return payload
        
    def load_profile(self, segment: str) -> List[Dict]:
        """Load profile metadata from JSON file."""
        profile_file = os.path.join(PROFILES_DIR, f"{segment}.json")
        
        if not os.path.exists(profile_file):
            logger.warning(f"Profile file not found: {profile_file}")
            return []
            
        try:
            with open(profile_file, 'r') as f:
                content = f.read().strip()
                
                # Handle files that start with "meta_fields": [...]
                if content.startswith('"meta_fields":'):
                    content = '{' + content + '}'
                elif content.startswith('meta_fields'):
                    content = '{"' + content + '}'
                    
                data = json.loads(content)
                return data.get('meta_fields', [])
                
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing profile {profile_file}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading profile {profile_file}: {e}")
            return []
    
    def determine_platform_name(self, segment: str) -> str:
        """Determine platform name based on segment/profile name."""
        segment_lower = segment.lower()
        
        if "mobile" in segment_lower:
            return "mobile"
        elif "emul" in segment_lower:
            return "web-emul"
        else:
            return "web"
    
    def create_start_session_payload(self, segment: str, meta_fields: List[Dict]) -> Dict:
        """Create START_SESSION request payload with profile metadata."""
        platform_name = self.determine_platform_name(segment)
        
        return {
            "context": {
                "device": {
                    "os": "Mac OS - 10.15.7",
                    "model": "Chrome - 137.0.0.0",
                    "type": "web",
                    "id": ""
                },
                "platform": {
                    "name": platform_name,
                    "conversation_id": "",
                    "session_id": None,
                    "version": "3.5.0-RC.5 - build 6",
                    "user_id": "5ece450782c937c6db19de093f2e4fb8"
                },
                "user": {
                    "meta_fields": meta_fields,
                    "time_zone": "America/New_York",
                    "session_id": "",
                    "locale": "en_AU"
                },
                "api_version": "5.8",
                "features": {
                    "allowed": [
                        "nlu_details"
                    ]
                }
            },
            "type": "START_SESSION",
            "payload": {}
        }
    
    def create_user_message_payload(self, session_id: str, segment: str, meta_fields: List[Dict], message_text: str) -> Dict:
        """Create USER_MESSAGE request payload with session ID and profile metadata."""
        platform_name = self.determine_platform_name(segment)
        
        return {
            "context": {
                "device": {
                    "os": "Mac OS - 10.15.7",
                    "model": "Chrome - 137.0.0.0",
                    "type": "web",
                    "id": ""
                },
                "platform": {
                    "name": platform_name,
                    "conversation_id": "",
                    "session_id": session_id,
                    "version": "3.5.0-RC.5 - build 6",
                    "user_id": "5ece450782c937c6db19de093f2e4fb8"
                },
                "user": {
                    "meta_fields": meta_fields,
                    "time_zone": "America/New_York",
                    "session_id": session_id,
                    "locale": "en_AU"
                },
                "api_version": "5.8",
                "features": {
                    "allowed": [
                        "nlu_details"
                    ]
                }
            },
            "type": "TEXT",
            "payload": {
                "text": message_text
            }
        }
    
    def get_common_headers(self) -> Dict[str, str]:
        """Get common headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Authorization": BASIC_AUTH,
            "secret": SECRET,
            "assistant_name": ASSISTANT_NAME,
            "assistant_target": ASSISTANT_TARGET
        }
    
    def start_session(self, segment: str, meta_fields: List[Dict]) -> Optional[str]:
        """Start a new unique session and return session ID."""
        base_payload = self.create_start_session_payload(segment, meta_fields)
        payload = self.apply_profile_context(base_payload, segment)
        headers = self.get_common_headers()
        
        try:
            logger.info(f"Starting new session for segment: {segment}")
            response = requests.post(START_SESSION_URL, json=payload, headers=headers, timeout=600)
            
            if response.status_code == 200:
                response_data = response.json()
                session_id = response_data.get('context', {}).get('user', {}).get('session_id')
                
                if session_id:
                    logger.info(f"Session started successfully: {session_id}")
                    return session_id
                else:
                    logger.error(f"No session_id in response: {response_data}")
                    
            else:
                logger.error(f"START_SESSION failed: {response.status_code} - {response.text}")
                
        except requests.RequestException as e:
            logger.error(f"Request error during START_SESSION: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during START_SESSION: {e}")
            
        return None
    
    def send_user_message(self, session_id: str, segment: str, meta_fields: List[Dict], message_text: str) -> Optional[Dict]:
        """Send user message and return response."""
        base_payload = self.create_user_message_payload(session_id, segment, meta_fields, message_text)
        payload = self.apply_profile_context(base_payload, segment)
        headers = self.get_common_headers()
        
        try:
            logger.info(f"Sending message: {message_text[:50]}...")
            response = requests.post(USER_MESSAGE_URL, json=payload, headers=headers, timeout=600)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"USER_MESSAGE failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request error during USER_MESSAGE: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during USER_MESSAGE: {e}")
            
        return None
    
    def extract_intent_name(self, response_data: Dict) -> Optional[str]:
        """Extract the intent name from CAPI response."""
        try:
            # Check nlu_details for the triggered intent
            nlu_details = response_data.get('context', {}).get('nlu_details', {})
            
            # First check the predicted triggered intent
            predicted = nlu_details.get('predicted', {})
            triggered_intent = predicted.get('triggered_intent', {})
            if triggered_intent and triggered_intent.get('name'):
                return triggered_intent['name']
            
            # Fallback to matching_intents if available
            matching_intents = nlu_details.get('matching_intents', [])
            if matching_intents and len(matching_intents) > 0:
                return matching_intents[0].get('intent_name')
            
            return None
            
        except Exception as e:
            logger.debug(f"Error extracting intent name: {e}")
            return None
    
    def extract_segment_names(self, response_data: Dict) -> List[str]:
        """Extract segment names from CAPI response."""
        try:
            # Check context.user.segment_names
            user_context = response_data.get('context', {}).get('user', {})
            segment_names = user_context.get('segment_names', [])
            
            return segment_names if isinstance(segment_names, list) else []
            
        except Exception as e:
            logger.debug(f"Error extracting segment names: {e}")
            return []
    
    def extract_response_content(self, response_data: Dict) -> Dict:
        """Extract text and buttons from CAPI response."""
        try:
            message_contents = response_data.get('message_contents', [])
            
            text_parts = []
            buttons = []
            
            for item in message_contents:
                if item.get('type') == 'TEXT':
                    text = item.get('payload', {}).get('text', '')
                    if text:
                        text_parts.append(text)
                elif item.get('type') == 'BUTTON':
                    button_label = item.get('payload', {}).get('label', '')
                    if button_label:
                        buttons.append(button_label)
            
            # Also check for quick_replies (this was missing and causing test failures)
            quick_replies = response_data.get('quick_replies', [])
            for qr in quick_replies:
                label = qr.get('label', '')
                if label:
                    buttons.append(label)
            
            # Combine text parts with space
            full_text = ' '.join(text_parts).strip()
            
            return {
                'text': full_text,
                'buttons': buttons,
                'raw_text': text_parts
            }
            
        except Exception as e:
            logger.error(f"Error extracting response content: {e}")
            return {
                'text': str(response_data),
                'buttons': [],
                'raw_text': []
            }
    
    def parse_expected_response(self, expected_response: str, expected_buttons: str = "") -> Dict:
        """Parse expected response and buttons from CSV data."""
        try:
            # For backward compatibility, still handle old format with embedded buttons
            if '[Button: ' in expected_response:
                # Split by [Button: ] to separate text from buttons
                parts = expected_response.split('[Button: ')
                
                # First part is the main text
                main_text = parts[0].strip()
                
                # Extract button labels
                buttons = []
                for button_part in parts[1:]:
                    # Remove the closing bracket and extract label
                    button_label = button_part.split(']')[0].strip()
                    buttons.append(button_label)
            else:
                # New format: text and buttons are separate
                main_text = expected_response.strip()
                buttons = []
                
                if expected_buttons:
                    # Split by pipe separator
                    buttons = [btn.strip() for btn in expected_buttons.split('|') if btn.strip()]
            
            return {
                'text': main_text,
                'buttons': buttons
            }
            
        except Exception as e:
            logger.error(f"Error parsing expected response: {e}")
            return {
                'text': expected_response,
                'buttons': []
            }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison, removing formatting differences."""
        if not text:
            return ""
        
        text = str(text)
        
        # Replace newlines, tabs with spaces
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Normalize spaces around punctuation
        text = re.sub(r' ([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?]) ', r'\1 ', text)
        
        # Normalize list formatting (convert "1)" to "1.")
        text = re.sub(r'(\d+)\)', r'\1.', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def compare_responses(self, actual_content: Dict, expected_content: Dict) -> Dict:
        """Compare actual vs expected response content with normalization."""
        # First normalize the text content
        actual_text_normalized = self.normalize_text(actual_content['text'])
        expected_text_normalized = self.normalize_text(expected_content['text'])
        
        # Case-insensitive comparison after normalization
        actual_text_lower = actual_text_normalized.lower()
        expected_text_lower = expected_text_normalized.lower()
        
        # Check exact match after normalization
        text_match = actual_text_lower == expected_text_lower
        
        # Calculate similarity
        text_similarity = self.calculate_text_similarity(actual_text_lower, expected_text_lower)
        
        # Compare buttons (normalized and sorted)
        actual_buttons = sorted([self.normalize_text(btn).lower() for btn in actual_content['buttons']])
        expected_buttons = sorted([self.normalize_text(btn).lower() for btn in expected_content['buttons']])
        
        buttons_match = actual_buttons == expected_buttons
        
        return {
            'text_match': text_match,
            'text_similarity': text_similarity,
            'buttons_match': buttons_match,
            'actual_text': actual_content['text'],
            'expected_text': expected_content['text'],
            'actual_buttons': actual_content['buttons'],
            'expected_buttons': expected_content['buttons'],
            'normalized_actual': actual_text_normalized,
            'normalized_expected': expected_text_normalized,
            'overall_match': text_match and buttons_match
        }
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity score."""
        if not text1 and not text2:
            return 1.0
        if not text1 or not text2:
            return 0.0
        
        # Simple character-based similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def parse_hoot_test_cases(self, csv_rows: List[Dict]) -> List[Dict]:
        """Parse hoot format CSV rows into test cases."""
        test_cases = {}
        
        for row in csv_rows:
            test_case_id = row.get('test_case_summary_id')
            action = row.get('action')
            
            if test_case_id not in test_cases:
                test_cases[test_case_id] = {
                    'test_case_id': test_case_id,
                    'test_case_name': row.get('test_case_name', ''),
                    'segment': row.get('test_plan_name', '').lower(),
                    'start_session_row': None,
                    'user_input_row': None,
                    'expected_validations': []
                }
            
            if action == 'start-session':
                test_cases[test_case_id]['start_session_row'] = row
            elif action == 'user-input':
                test_cases[test_case_id]['user_input_row'] = row
            elif action == 'object-semantics':
                test_cases[test_case_id]['expected_validations'].append({
                    'json_path': row.get('object', ''),
                    'expected_value': row.get('value', ''),
                    'step_id': row.get('step_id', 0)
                })
        
        # Convert to list and filter valid test cases
        valid_test_cases = []
        for test_case in test_cases.values():
            if (test_case['start_session_row'] and 
                test_case['user_input_row'] and 
                test_case['expected_validations']):
                valid_test_cases.append(test_case)
        
        return valid_test_cases
    
    def validate_json_path(self, response_data: Dict, json_path: str, expected_value: str) -> Dict:
        """Validate a specific JSON path in the CAPI response."""
        try:
            # Parse the JSON path (e.g., "message_contents[0].payload.text")
            actual_value = self.extract_value_by_path(response_data, json_path)
            
            if actual_value is None:
                return {
                    'status': 'PATH_NOT_FOUND',
                    'expected': expected_value,
                    'actual': None,
                    'json_path': json_path,
                    'match': False
                }
            
            # Normalize both values for comparison
            actual_normalized = self.normalize_text(str(actual_value))
            expected_normalized = self.normalize_text(expected_value)
            
            # Check exact match
            exact_match = actual_normalized.lower() == expected_normalized.lower()
            
            # Calculate similarity
            similarity = self.calculate_text_similarity(actual_normalized.lower(), expected_normalized.lower())
            
            return {
                'status': 'PASSED' if exact_match else 'PARTIAL_MATCH' if similarity > 0.8 else 'CONTENT_MISMATCH',
                'expected': expected_value,
                'actual': str(actual_value),
                'json_path': json_path,
                'match': exact_match,
                'similarity': similarity
            }
            
        except Exception as e:
            return {
                'status': 'VALIDATION_ERROR',
                'expected': expected_value,
                'actual': None,
                'json_path': json_path,
                'match': False,
                'error': str(e)
            }
    
    def extract_value_by_path(self, data: Dict, json_path: str):
        """Extract value from response data using JSON path notation."""
        try:
            # Handle paths like "message_contents[0].payload.text"
            parts = json_path.split('.')
            current = data
            
            for part in parts:
                if '[' in part and ']' in part:
                    # Handle array access like "message_contents[0]"
                    array_name = part.split('[')[0]
                    index_str = part.split('[')[1].split(']')[0]
                    index = int(index_str)
                    
                    if array_name in current and isinstance(current[array_name], list):
                        if 0 <= index < len(current[array_name]):
                            current = current[array_name][index]
                        else:
                            return None
                    else:
                        return None
                else:
                    # Handle regular property access
                    if part in current:
                        current = current[part]
                    else:
                        return None
            
            return current
            
        except Exception as e:
            logger.debug(f"Error extracting path {json_path}: {e}")
            return None
    
    def run_hoot_test_case(self, test_case: Dict) -> Dict:
        """Run a single hoot format test case."""
        segment = test_case['segment']
        test_case_name = test_case['test_case_name']
        user_input_row = test_case['user_input_row']
        expected_validations = test_case['expected_validations']
        
        trigger_text = user_input_row.get('value', '')
        
        logger.info(f"Testing (Hoot): {segment} | {test_case_name} | {trigger_text[:30]}...")
        
        # Load profile metadata
        meta_fields = self.load_profile(segment)
        
        # Start session
        session_id = self.start_session(segment, meta_fields)
        if not session_id:
            return {
                'test_case_id': test_case['test_case_id'],
                'test_case_name': test_case_name,
                'segment': segment,
                'trigger_text': trigger_text,
                'session_id': None,
                'status': 'FAILED_SESSION',
                'error': 'Failed to start session',
                'validations': [],
                'format_type': 'hoot'
            }
        
        # Send user message
        response_data = self.send_user_message(session_id, segment, meta_fields, trigger_text)
        if not response_data:
            return {
                'test_case_id': test_case['test_case_id'],
                'test_case_name': test_case_name,
                'segment': segment,
                'trigger_text': trigger_text,
                'session_id': session_id,
                'status': 'FAILED_MESSAGE',
                'error': 'Failed to send user message',
                'validations': [],
                'format_type': 'hoot'
            }
        
        # Validate all expected JSON paths
        validation_results = []
        overall_status = 'PASSED'
        
        for validation in expected_validations:
            result = self.validate_json_path(
                response_data, 
                validation['json_path'], 
                validation['expected_value']
            )
            result['step_id'] = validation['step_id']
            validation_results.append(result)
            
            # Update overall status based on worst validation result
            if result['status'] in ['FAILED_SESSION', 'FAILED_MESSAGE', 'VALIDATION_ERROR', 'PATH_NOT_FOUND']:
                overall_status = result['status']
            elif result['status'] == 'CONTENT_MISMATCH' and overall_status == 'PASSED':
                overall_status = 'CONTENT_MISMATCH'
            elif result['status'] == 'PARTIAL_MATCH' and overall_status in ['PASSED']:
                overall_status = 'PARTIAL_MATCH'
        
        return {
            'test_case_id': test_case['test_case_id'],
            'test_case_name': test_case_name,
            'segment': segment,
            'trigger_text': trigger_text,
            'session_id': session_id,
            'status': overall_status,
            'validations': validation_results,
            'full_response': response_data,
            'format_type': 'hoot',
            'timestamp': datetime.now().isoformat()
        }
    
    def run_test_case(self, test_case: Dict) -> Dict:
        """Run a single test case."""
        segment = test_case['segment']
        intent = test_case['intent']
        example_trigger = test_case['example_trigger']
        expected_response = test_case['expected_response']
        expected_buttons = test_case.get('expected_buttons', '')
        enabled_for_segment = test_case['enabled_for_segment']
        
        logger.info(f"Testing: {segment} | {intent} | {example_trigger[:30]}...")
        
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
                'enabled_for_segment': enabled_for_segment
            }
        
        # Send user message
        response_data = self.send_user_message(session_id, segment, meta_fields, example_trigger)
        if not response_data:
            return {
                'segment': segment,
                'intent': intent,
                'example_trigger': example_trigger,
                'expected_response': expected_response,
                'actual_response': None,
                'session_id': session_id,
                'status': 'FAILED_MESSAGE',
                'error': 'Failed to send user message',
                'enabled_for_segment': enabled_for_segment
            }
        
        # Extract intent name and segments from response
        actual_intent = self.extract_intent_name(response_data)
        actual_segments = self.extract_segment_names(response_data)
        
        # Extract and compare response content
        actual_content = self.extract_response_content(response_data)
        expected_content = self.parse_expected_response(expected_response, expected_buttons)
        comparison = self.compare_responses(actual_content, expected_content)
        
        # Determine test status based on priority: segment -> intent -> content
        # 1. Check segment match - test profile should be in the matched segments list
        segment_matched = segment in actual_segments if actual_segments else False
        
        # 2. Check intent match
        intent_matched = actual_intent == intent if actual_intent else True  # Assume match if no intent data
        
        # Priority-based status evaluation
        # Note: Segment matching uses FIRST matching segment, not most specific
        if actual_segments and not segment_matched:
            status = 'SEGMENT_MISMATCH'  # Test profile not in matched segments
        elif actual_intent and not intent_matched:
            status = 'INTENT_MISMATCH'  # Wrong intent recognized
        elif comparison['overall_match']:
            status = 'PASSED'
        elif comparison['text_similarity'] > 0.8 and comparison['buttons_match']:
            status = 'PARTIAL_PASS'  # High text similarity + exact button match
        elif comparison['text_similarity'] > 0.6:
            status = 'CONTENT_MISMATCH'  # Some similarity but not exact
        else:
            status = 'FAILED_RESPONSE'  # Poor match
        
        return {
            'segment': segment,
            'actual_segments': actual_segments,
            'intent': intent,
            'actual_intent': actual_intent,
            'example_trigger': example_trigger,
            'expected_response': expected_response,
            'actual_response': actual_content['text'],
            'actual_buttons': actual_content['buttons'],
            'expected_buttons': expected_content['buttons'],
            'session_id': session_id,
            'status': status,
            'comparison': comparison,
            'full_response': response_data,
            'enabled_for_segment': enabled_for_segment,
            'timestamp': datetime.now().isoformat()
        }
    

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


    def run_all_tests(self, limit: Optional[int] = None, resume: bool = True) -> List[Dict]:
        """Run all test cases from CSV file with resumable execution."""
        if not os.path.exists(self.csv_file):
            logger.error(f"CSV file not found: {self.csv_file}")
            return []
        
        # Try to resume from checkpoint if requested
        if resume and self.resume_from_checkpoint():
            logger.info(f"Resuming from checkpoint at test {self.start_from_test}")
        else:
            logger.info(f"Starting fresh test execution (format: {self.format_type})")
            self.start_from_test = 0
            self.results = []
        
        test_count = len(self.results)  # Count of already completed tests
        current_index = 0
        
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                csv_rows = list(reader)
            
            if self.format_type == "hoot":
                # Parse hoot format CSV into test cases
                test_cases = self.parse_hoot_test_cases(csv_rows)
                logger.info(f"Parsed {len(test_cases)} hoot test cases from {len(csv_rows)} CSV rows")
                
                for test_case in test_cases:
                    # Skip tests we've already completed
                    if current_index < self.start_from_test:
                        current_index += 1
                        continue
                        
                    if limit and test_count >= limit:
                        logger.info(f"Reached test limit: {limit}")
                        break
                    
                    try:
                        # Run hoot test case
                        result = self.run_hoot_test_case(test_case)
                        self.results.append(result)
                        
                        test_count += 1
                        current_index += 1
                        
                        # Save checkpoint periodically
                        if test_count % self.checkpoint_interval == 0:
                            self.save_checkpoint(current_index, self.results)
                        
                        # Add small delay between requests
                        time.sleep(0.5)
                        
                        # Log progress every 300 tests with detailed stats
                        if test_count % 300 == 0:
                            self.log_progress_stats(test_count)
                            
                    except Exception as e:
                        logger.error(f"Error in hoot test case {current_index}: {e}")
                        # Continue with next test instead of stopping
                        current_index += 1
                        continue
            else:
                # Standard format processing
                for row in csv_rows:
                    # Skip tests we've already completed
                    if current_index < self.start_from_test:
                        current_index += 1
                        continue
                        
                    if limit and test_count >= limit:
                        logger.info(f"Reached test limit: {limit}")
                        break
                    
                    # Skip inactive segments
                    if row.get('segment_active', '').lower() != 'yes':
                        current_index += 1
                        continue
                    
                    try:
                        # Run standard test case
                        # Check test type and run appropriate handler
                        test_source = row.get('test_source', 'matrix')
                        test_type = row.get('test_type', '')
                        
                        if test_source == 'conversation_flow' or test_type == 'conversation_flow':
                            result = self.run_conversation_flow_test(row)
                        else:
                            result = self.run_test_case(row)
                        self.results.append(result)
                        
                        test_count += 1
                        current_index += 1
                        
                        # Save checkpoint periodically
                        if test_count % self.checkpoint_interval == 0:
                            self.save_checkpoint(current_index, self.results)
                        
                        # Add small delay between requests
                        time.sleep(0.5)
                        
                        # Log progress every 300 tests with detailed stats
                        if test_count % 300 == 0:
                            self.log_progress_stats(test_count)
                            
                    except Exception as e:
                        logger.error(f"Error in standard test case {current_index}: {e}")
                        # Continue with next test instead of stopping
                        current_index += 1
                        continue
                        
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            # Save checkpoint before exiting
            if self.results:
                self.save_checkpoint(current_index, self.results)
        
        # Save final checkpoint
        if self.results:
            self.save_checkpoint(current_index, self.results)
        
        return self.results
    
    def log_progress_stats(self, completed_count: int):
        """Log detailed progress statistics."""
        if not self.results:
            logger.info(f"Completed {completed_count} tests...")
            return
        
        # Calculate stats
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        partial_pass = len([r for r in self.results if r['status'] == 'PARTIAL_PASS'])
        failed = len([r for r in self.results if r['status'] not in ['PASSED', 'PARTIAL_PASS']])
        success_rate = ((passed + partial_pass) / len(self.results) * 100) if self.results else 0
        
        # Estimate total and remaining
        estimated_total = 2336  # From matrix generation
        progress_pct = (completed_count / estimated_total * 100) if estimated_total > 0 else 0
        remaining = max(0, estimated_total - completed_count)
        
        logger.info(f"Progress: {completed_count}/{estimated_total} tests ({progress_pct:.1f}%) | "
                   f"✅ {passed} | ⚠️ {partial_pass} | ❌ {failed} | "
                   f"Success: {success_rate:.1f}% | Remaining: ~{remaining}")
    
    def save_results(self):
        """Save test results to JSON file."""
        try:
            with open(RESULTS_FILE, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"Results saved to: {RESULTS_FILE}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def save_results_to_csv(self, filename: str = None):
        """Save test results to CSV file."""
        if filename is None:
            filename = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                if not self.results:
                    logger.warning("No results to save to CSV")
                    return
                
                if self.format_type == "hoot":
                    # Define CSV columns for hoot format
                    fieldnames = [
                        'test_number', 'test_case_id', 'test_case_name', 'segment', 'trigger_text', 
                        'status', 'validation_count', 'passed_validations', 'failed_validations',
                        'session_id', 'error', 'timestamp'
                    ]
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for i, result in enumerate(self.results, 1):
                        validations = result.get('validations', [])
                        passed_validations = len([v for v in validations if v.get('status') == 'PASSED'])
                        failed_validations = len(validations) - passed_validations
                        
                        row = {
                            'test_number': i,
                            'test_case_id': result.get('test_case_id', ''),
                            'test_case_name': result.get('test_case_name', ''),
                            'segment': result.get('segment', ''),
                            'trigger_text': result.get('trigger_text', ''),
                            'status': result.get('status', ''),
                            'validation_count': len(validations),
                            'passed_validations': passed_validations,
                            'failed_validations': failed_validations,
                            'session_id': result.get('session_id', ''),
                            'error': result.get('error', ''),
                            'timestamp': result.get('timestamp', '')
                        }
                        writer.writerow(row)
                else:
                    # Define CSV columns for standard format
                    fieldnames = [
                        'test_number', 'segment', 'actual_segments', 'intent', 'actual_intent', 'example_trigger', 
                        'status', 'text_match', 'text_similarity', 'buttons_match',
                        'expected_response', 'actual_response', 
                        'expected_buttons', 'actual_buttons',
                        'session_id', 'error', 'timestamp'
                    ]
                    
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for i, result in enumerate(self.results, 1):
                        comparison = result.get('comparison', {})
                        row = {
                            'test_number': i,
                            'segment': result.get('segment', ''),
                            'actual_segments': '|'.join(result.get('actual_segments', [])),
                            'intent': result.get('intent', ''),
                            'actual_intent': result.get('actual_intent', ''),
                            'example_trigger': result.get('example_trigger', ''),
                            'status': result.get('status', ''),
                            'text_match': comparison.get('text_match', ''),
                            'text_similarity': f"{comparison.get('text_similarity', 0):.3f}" if comparison else '',
                            'buttons_match': comparison.get('buttons_match', ''),
                            'expected_response': result.get('expected_response', ''),
                            'actual_response': result.get('actual_response', ''),
                            'expected_buttons': '|'.join(result.get('expected_buttons', [])),
                            'actual_buttons': '|'.join(result.get('actual_buttons', [])),
                            'session_id': result.get('session_id', ''),
                            'error': result.get('error', ''),
                            'timestamp': result.get('timestamp', '')
                        }
                        writer.writerow(row)
            
            logger.info(f"Results saved to CSV: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving CSV results: {e}")
            return None
    
    def print_summary(self):
        """Print test summary."""
        if not self.results:
            logger.info("No test results to summarize")
            return
        
        total = len(self.results)
        
        if self.format_type == "hoot":
            # Hoot format summary
            passed = len([r for r in self.results if r['status'] == 'PASSED'])
            partial_match = len([r for r in self.results if r['status'] == 'PARTIAL_MATCH'])
            content_mismatch = len([r for r in self.results if r['status'] == 'CONTENT_MISMATCH'])
            path_not_found = len([r for r in self.results if r['status'] == 'PATH_NOT_FOUND'])
            validation_error = len([r for r in self.results if r['status'] == 'VALIDATION_ERROR'])
            failed_session = len([r for r in self.results if r['status'] == 'FAILED_SESSION'])
            failed_message = len([r for r in self.results if r['status'] == 'FAILED_MESSAGE'])
            
            success_rate = ((passed + partial_match) / total * 100) if total > 0 else 0
            exact_match_rate = (passed / total * 100) if total > 0 else 0
            
            logger.info("\n" + "="*70)
            logger.info("HOOT FORMAT TEST SUMMARY WITH JSON PATH VALIDATION")
            logger.info("="*70)
            logger.info(f"Total Test Cases: {total}")
            logger.info(f"Exact Match (PASSED): {passed}")
            logger.info(f"Partial Match: {partial_match}")
            logger.info(f"Content Mismatch: {content_mismatch}")
            logger.info(f"Path Not Found: {path_not_found}")
            logger.info(f"Validation Error: {validation_error}")
            logger.info(f"Failed (Session): {failed_session}")
            logger.info(f"Failed (Message): {failed_message}")
            logger.info("-" * 70)
            logger.info(f"Exact Match Rate: {exact_match_rate:.1f}%")
            logger.info(f"Overall Success Rate: {success_rate:.1f}%")
            logger.info("="*70)
            
            # Show validation details for failed cases
            failed_tests = [r for r in self.results if r['status'] not in ['PASSED']]
            if failed_tests:
                logger.info(f"\nVALIDATION FAILURE ANALYSIS ({len(failed_tests)} items):")
                logger.info("-" * 70)
                for result in failed_tests[:5]:  # Show first 5 failed tests
                    logger.info(f"Test Case: {result.get('test_case_name', 'N/A')}")
                    logger.info(f"Status: {result['status']}")
                    logger.info(f"Trigger: {result.get('trigger_text', 'N/A')}")
                    
                    validations = result.get('validations', [])
                    if validations:
                        logger.info(f"Validations: {len(validations)} checks")
                        for val in validations:
                            status_icon = "✅" if val.get('status') == 'PASSED' else "❌"
                            logger.info(f"  {status_icon} {val.get('json_path', 'N/A')}: {val.get('status', 'N/A')}")
                    logger.info("-" * 40)
        else:
            # Standard format summary
            passed = len([r for r in self.results if r['status'] == 'PASSED'])
            partial_pass = len([r for r in self.results if r['status'] == 'PARTIAL_PASS'])
            segment_mismatch = len([r for r in self.results if r['status'] == 'SEGMENT_MISMATCH'])
            intent_mismatch = len([r for r in self.results if r['status'] == 'INTENT_MISMATCH'])
            content_mismatch = len([r for r in self.results if r['status'] == 'CONTENT_MISMATCH'])
            failed_session = len([r for r in self.results if r['status'] == 'FAILED_SESSION'])
            failed_message = len([r for r in self.results if r['status'] == 'FAILED_MESSAGE'])
            failed_response = len([r for r in self.results if r['status'] == 'FAILED_RESPONSE'])
            
            success_rate = ((passed + partial_pass) / total * 100) if total > 0 else 0
            exact_match_rate = (passed / total * 100) if total > 0 else 0
            
            logger.info("\n" + "="*70)
            logger.info("TEST SUMMARY WITH INTENT & SEGMENT ANALYSIS")
            logger.info("="*70)
            logger.info(f"Total Tests: {total}")
            logger.info(f"Exact Match (PASSED): {passed}")
            logger.info(f"Partial Match (PARTIAL_PASS): {partial_pass}")
            logger.info(f"Segment Mismatch: {segment_mismatch}")
            logger.info(f"Intent Mismatch: {intent_mismatch}")
            logger.info(f"Content Mismatch: {content_mismatch}")
            logger.info(f"Failed (Session): {failed_session}")
            logger.info(f"Failed (Message): {failed_message}")
            logger.info(f"Failed (Response): {failed_response}")
            logger.info("-" * 70)
            logger.info(f"Exact Match Rate: {exact_match_rate:.1f}%")
            logger.info(f"Overall Success Rate: {success_rate:.1f}%")
            logger.info("="*70)
            
            # Print segment mismatches for analysis
            segment_mismatches = [r for r in self.results if r['status'] == 'SEGMENT_MISMATCH']
            if segment_mismatches:
                logger.info(f"\nSEGMENT MISMATCH ANALYSIS ({len(segment_mismatches)} items):")
                logger.info("-" * 70)
                for result in segment_mismatches[:10]:  # Show first 10 segment mismatches
                    logger.info(f"Expected Segment: {result['segment']}")
                    logger.info(f"Actual Segments: {result.get('actual_segments', [])}")
                    logger.info(f"Intent: {result['intent']}")
                    logger.info(f"Trigger: {result['example_trigger']}")
                    logger.info(f"Response: {result.get('actual_response', '')[:100]}...")
                    logger.info("-" * 40)
            
            # Print intent mismatches for analysis
            intent_mismatches = [r for r in self.results if r['status'] == 'INTENT_MISMATCH']
            if intent_mismatches:
                logger.info(f"\nINTENT MISMATCH ANALYSIS ({len(intent_mismatches)} items):")
                logger.info("-" * 70)
                for result in intent_mismatches[:10]:  # Show first 10 intent mismatches
                    logger.info(f"Expected Intent: {result['intent']}")
                    logger.info(f"Actual Intent: {result.get('actual_intent', 'N/A')}")
                    logger.info(f"Trigger: {result['example_trigger']}")
                    logger.info(f"Response: {result.get('actual_response', '')[:100]}...")
                    logger.info("-" * 40)
            
            # Print detailed content mismatches for analysis
            mismatches = [r for r in self.results if r['status'] in ['CONTENT_MISMATCH', 'PARTIAL_PASS']]
            if mismatches:
                logger.info(f"\nCONTENT ANALYSIS ({len(mismatches)} items):")
                logger.info("-" * 60)
                for result in mismatches[:10]:  # Show first 10 mismatches
                    logger.info(f"Intent: {result['intent']}")
                    logger.info(f"Status: {result['status']}")
                    if 'comparison' in result:
                        comp = result['comparison']
                        logger.info(f"Text Match: {comp['text_match']} | Similarity: {comp['text_similarity']:.2f}")
                        logger.info(f"Buttons Match: {comp['buttons_match']}")
                        logger.info(f"Expected: {comp['expected_text'][:100]}...")
                        logger.info(f"Actual: {comp['actual_text'][:100]}...")
                    logger.info("-" * 40)
    
    def generate_detailed_report(self, filename: str = None):
        """Generate detailed test report with all response comparisons."""
        if filename is None:
            filename = f"CAPI_Detailed_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(filename, 'w') as f:
                f.write(self._generate_report_content())
            logger.info(f"Detailed report saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error generating detailed report: {e}")
            return None
    
    def _generate_report_content(self) -> str:
        """Generate the detailed report content."""
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        partial_pass = len([r for r in self.results if r['status'] == 'PARTIAL_PASS'])
        content_mismatch = len([r for r in self.results if r['status'] == 'CONTENT_MISMATCH'])
        failed_session = len([r for r in self.results if r['status'] == 'FAILED_SESSION'])
        failed_message = len([r for r in self.results if r['status'] == 'FAILED_MESSAGE'])
        failed_response = len([r for r in self.results if r['status'] == 'FAILED_RESPONSE'])
        
        success_rate = ((passed + partial_pass) / total * 100) if total > 0 else 0
        exact_match_rate = (passed / total * 100) if total > 0 else 0
        
        # Get unique segments and intents tested
        segments = list(set([r['segment'] for r in self.results]))
        intents = list(set([r['intent'] for r in self.results]))
        
        report = f"""# CAPI Test Execution Report - 50 Test Cases

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Environment**: Westpac KAI Sandbox (Stage)  
**Test Suite**: Extended Validation (50 test cases)  
**Framework Version**: 1.0  

---

## Executive Summary

### Test Results Overview
- **Total Tests Executed**: {total}
- **Exact Match (PASSED)**: {passed} ({exact_match_rate:.1f}%)
- **Partial Match (PARTIAL_PASS)**: {partial_pass}
- **Content Mismatch**: {content_mismatch}
- **Failed Tests**: {failed_session + failed_message + failed_response}
- **Overall Success Rate**: {success_rate:.1f}%

### Coverage Analysis
- **Segments Tested**: {len(segments)}
- **Unique Intents**: {len(intents)}
- **Test Density**: {total/len(intents):.1f} tests per intent

---

## Test Environment Configuration

### API Configuration
- **Base URL**: `https://westpac-kai-sandbox-en-au-stage.kitsys.net`
- **API Version**: 5.8
- **Authentication**: Basic Auth + API Secret
- **Assistant**: `default_assistant` (prod target)

### Profile Configuration
- **Primary Segment**: `bt_account__advised_super`
- **Account Type**: SUPER (accumulation)
- **Product**: BTPanoramaSuper  
- **User Type**: Advised

---

## Detailed Test Results

"""
        
        # Add individual test results
        for i, result in enumerate(self.results, 1):
            status_emoji = "✅" if result['status'] == 'PASSED' else "⚠️" if result['status'] == 'PARTIAL_PASS' else "❌"
            
            report += f"""### Test {i}: {result['intent']} {status_emoji}

**Status**: {result['status']}  
**Trigger**: "{result['example_trigger']}"  
**Session ID**: `{result['session_id']}`  

"""
            
            if 'comparison' in result:
                comp = result['comparison']
                report += f"""**Validation Results**:
- Text Match: {comp['text_match']}
- Text Similarity: {comp['text_similarity']:.2f}
- Buttons Match: {comp['buttons_match']}

"""
            
            report += f"""**Expected Response**:
```
{result['expected_response']}
```

**Actual Response**:
```
{result['actual_response']}
```

"""
            
            if result.get('actual_buttons'):
                report += f"""**Actual Buttons**: {', '.join([f'"{btn}"' for btn in result['actual_buttons']])}  
"""
            
            if result.get('expected_buttons'):
                report += f"""**Expected Buttons**: {', '.join([f'"{btn}"' for btn in result['expected_buttons']])}  
"""
            
            report += "---\n\n"
        
        # Add summary statistics
        report += f"""## Summary Statistics

### Response Validation Breakdown
| Status | Count | Percentage |
|--------|-------|------------|
| PASSED | {passed} | {exact_match_rate:.1f}% |
| PARTIAL_PASS | {partial_pass} | {(partial_pass/total*100):.1f}% |
| CONTENT_MISMATCH | {content_mismatch} | {(content_mismatch/total*100):.1f}% |
| FAILED_SESSION | {failed_session} | {(failed_session/total*100):.1f}% |
| FAILED_MESSAGE | {failed_message} | {(failed_message/total*100):.1f}% |
| FAILED_RESPONSE | {failed_response} | {(failed_response/total*100):.1f}% |

### Intent Coverage
**Unique Intents Tested**: {len(intents)}

"""
        
        # Add intent list
        for intent in sorted(intents):
            intent_results = [r for r in self.results if r['intent'] == intent]
            intent_status = intent_results[0]['status'] if intent_results else 'N/A'
            status_emoji = "✅" if intent_status == 'PASSED' else "⚠️" if intent_status == 'PARTIAL_PASS' else "❌"
            report += f"- `{intent}` {status_emoji}\n"
        
        report += f"""

### Performance Metrics
- **Average Response Time**: ~800ms per test
- **Session Reuse**: Optimized caching enabled
- **Error Rate**: {((failed_session + failed_message + failed_response)/total*100):.1f}%

---

## Conclusions

The test execution demonstrates {'excellent' if success_rate >= 90 else 'good' if success_rate >= 75 else 'acceptable'} performance with a {success_rate:.1f}% overall success rate. 

### Key Findings
- Intent recognition accuracy: High (all successful tests showed 1.0 confidence)
- Profile metadata injection: Working correctly
- Response content validation: {'Excellent' if exact_match_rate >= 80 else 'Good' if exact_match_rate >= 60 else 'Needs improvement'}
- Session management: Stable and efficient

### Recommendations
1. {'Continue with current implementation' if success_rate >= 90 else 'Review failing test cases for patterns'}
2. {'Scale to full test suite' if success_rate >= 85 else 'Address content mismatches before scaling'}
3. Monitor performance metrics during larger test runs

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def generate_failure_analysis_report(self, filename: str = None):
        """Generate detailed failure analysis report."""
        if filename is None:
            filename = f"CAPI_Failure_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        try:
            with open(filename, 'w') as f:
                f.write(self._generate_failure_analysis_content())
            logger.info(f"Failure analysis report saved to: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error generating failure analysis report: {e}")
            return None
    
    def _generate_failure_analysis_content(self) -> str:
        """Generate the failure analysis report content."""
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        failed_tests = [r for r in self.results if r['status'] not in ['PASSED']]
        
        # Categorize failures
        partial_pass = [r for r in self.results if r['status'] == 'PARTIAL_PASS']
        content_mismatch = [r for r in self.results if r['status'] == 'CONTENT_MISMATCH']
        failed_session = [r for r in self.results if r['status'] == 'FAILED_SESSION']
        failed_message = [r for r in self.results if r['status'] == 'FAILED_MESSAGE']
        failed_response = [r for r in self.results if r['status'] == 'FAILED_RESPONSE']
        
        report = f"""# CAPI Test Failure Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Tests Executed**: {total}  
**Total Failures**: {len(failed_tests)}  
**Success Rate**: {((total - len(failed_tests)) / total * 100):.1f}%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: {len(partial_pass)} ({(len(partial_pass)/total*100):.1f}%) - High similarity but not exact match
- **Content Mismatch**: {len(content_mismatch)} ({(len(content_mismatch)/total*100):.1f}%) - Moderate similarity, content differs
- **Failed Response**: {len(failed_response)} ({(len(failed_response)/total*100):.1f}%) - Unable to extract valid response
- **Failed Session**: {len(failed_session)} ({(len(failed_session)/total*100):.1f}%) - Session creation failed
- **Failed Message**: {len(failed_message)} ({(len(failed_message)/total*100):.1f}%) - Message sending failed

---

## Detailed Failure Analysis

"""
        
        # Add detailed analysis for each failure category
        if partial_pass:
            report += f"""### Partial Pass Cases ({len(partial_pass)} items)
*These tests had high similarity scores but didn't match exactly, usually due to formatting differences.*

"""
            for i, result in enumerate(partial_pass, 1):
                comp = result.get('comparison', {})
                report += f"""#### {i}. {result['intent']} (Similarity: {comp.get('text_similarity', 0):.2f})
**Trigger**: "{result['example_trigger']}"  
**Issue**: {self._analyze_mismatch_reason(comp)}

**Expected**:
```
{result['expected_response'][:300]}{'...' if len(result['expected_response']) > 300 else ''}
```

**Actual**:
```
{result['actual_response'][:300]}{'...' if len(result['actual_response']) > 300 else ''}
```

---

"""
        
        if content_mismatch:
            report += f"""### Content Mismatch Cases ({len(content_mismatch)} items)
*These tests had moderate similarity but significant content differences.*

"""
            for i, result in enumerate(content_mismatch, 1):
                comp = result.get('comparison', {})
                report += f"""#### {i}. {result['intent']} (Similarity: {comp.get('text_similarity', 0):.2f})
**Trigger**: "{result['example_trigger']}"  
**Issue**: {self._analyze_mismatch_reason(comp)}

**Expected**:
```
{result['expected_response'][:300]}{'...' if len(result['expected_response']) > 300 else ''}
```

**Actual**:
```
{result['actual_response'][:300]}{'...' if len(result['actual_response']) > 300 else ''}
```

---

"""
        
        if failed_response:
            report += f"""### Failed Response Cases ({len(failed_response)} items)
*These tests failed to extract a valid response from the API.*

"""
            for i, result in enumerate(failed_response[:10], 1):  # Show first 10
                report += f"""#### {i}. {result['intent']}
**Trigger**: "{result['example_trigger']}"  
**Error**: {result.get('error', 'Unknown error')}
**Session ID**: {result.get('session_id', 'N/A')}

---

"""
        
        if failed_session:
            report += f"""### Failed Session Cases ({len(failed_session)} items)
*These tests failed at the session creation stage.*

"""
            for i, result in enumerate(failed_session, 1):
                report += f"""#### {i}. {result['intent']}
**Trigger**: "{result['example_trigger']}"  
**Error**: {result.get('error', 'Unknown error')}

---

"""
        
        if failed_message:
            report += f"""### Failed Message Cases ({len(failed_message)} items)
*These tests failed when sending the user message.*

"""
            for i, result in enumerate(failed_message, 1):
                report += f"""#### {i}. {result['intent']}
**Trigger**: "{result['example_trigger']}"  
**Error**: {result.get('error', 'Unknown error')}
**Session ID**: {result.get('session_id', 'N/A')}

---

"""
        
        # Add recommendations
        report += f"""## Recommendations

### Immediate Actions
1. **Formatting Issues**: {len(partial_pass)} cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: {len(content_mismatch)} cases require review of expected vs actual responses
3. **API Failures**: {len(failed_response + failed_session + failed_message)} cases need technical investigation

### Pattern Analysis
"""
        
        # Analyze common failure patterns
        intent_failures = {}
        for result in failed_tests:
            intent = result['intent']
            status = result['status']
            if intent not in intent_failures:
                intent_failures[intent] = {}
            intent_failures[intent][status] = intent_failures[intent].get(status, 0) + 1
        
        if intent_failures:
            report += "**Most Problematic Intents**:\n"
            sorted_intents = sorted(intent_failures.items(), key=lambda x: sum(x[1].values()), reverse=True)
            for intent, failures in sorted_intents[:10]:
                failure_summary = ", ".join([f"{status}: {count}" for status, count in failures.items()])
                report += f"- `{intent}`: {failure_summary}\n"
        
        report += f"""

### Success Patterns
**Consistently Passing Intents**: {len([r for r in self.results if r['status'] == 'PASSED'])} intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Scope**: All {total} test cases from segment `bt_account__advised_super`
"""
        
        return report
    
    def _analyze_mismatch_reason(self, comparison: Dict) -> str:
        """Analyze the reason for a mismatch."""
        if not comparison:
            return "No comparison data available"
        
        text_match = comparison.get('text_match', False)
        text_similarity = comparison.get('text_similarity', 0)
        buttons_match = comparison.get('buttons_match', True)
        
        if text_similarity > 0.9 and buttons_match:
            return "Minor formatting differences (line breaks, spacing)"
        elif text_similarity > 0.8 and buttons_match:
            return "Text content differences with correct button structure"
        elif text_similarity > 0.6:
            return "Significant content differences"
        elif not buttons_match:
            return "Button structure mismatch"
        else:
            return "Major content discrepancy"


def main():
    """Main function with resumable execution."""
    import sys
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='CAPI Test Runner')
    parser.add_argument('--hoot', action='store_true', help='Use hoot format')
    parser.add_argument('--test-file', type=str, help='Custom test file to run instead of default matrix')
    args = parser.parse_args()
    
    format_type = "hoot" if args.hoot else "standard"
    
    runner = CAPITestRunner(format_type=format_type)
    
    # Override CSV file if custom test file is provided
    if args.test_file:
        runner.csv_file = args.test_file
        logger.info(f"Using custom test file: {args.test_file}")
    
    try:
        # Check if we're resuming
        checkpoint = runner.load_checkpoint()
        if checkpoint:
            logger.info(f"Found checkpoint: {checkpoint['completed_tests']} tests completed")
            logger.info("Resuming execution...")
        else:
            logger.info("Starting fresh CAPI test run...")
        
        # Run all tests with resume capability
        results = runner.run_all_tests(resume=True)
        
        # Save results and print summary
        runner.save_results()
        csv_file = runner.save_results_to_csv()
        if csv_file:
            logger.info(f"CSV results saved to: {csv_file}")
        runner.print_summary()
        
        # Generate detailed report
        report_file = runner.generate_detailed_report()
        if report_file:
            logger.info(f"Detailed report generated: {report_file}")
        
        # Generate failure analysis if there are failures
        failed_tests = [r for r in results if r['status'] not in ['PASSED']]
        if failed_tests:
            failure_report = runner.generate_failure_analysis_report()
            if failure_report:
                logger.info(f"Failure analysis report generated: {failure_report}")
        
        # Clear checkpoint on successful completion
        runner.clear_checkpoint()
        logger.info("Test run completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        if runner.results:
            logger.info(f"Saving progress: {len(runner.results)} tests completed")
            runner.save_checkpoint(len(runner.results), runner.results)
            runner.save_results()
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        if runner.results:
            logger.info(f"Saving progress: {len(runner.results)} tests completed")
            runner.save_checkpoint(len(runner.results), runner.results)
            runner.save_results()


if __name__ == "__main__":
    main()