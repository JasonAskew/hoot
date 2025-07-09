#!/usr/bin/env python3
"""
Single CAPI Test Runner with Full Request/Response Logging
Saves JSON payloads to files for easier viewing
"""

import json
import requests
import os
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

# Output directory for JSON files
OUTPUT_DIR = "capi_payloads"

def pretty_print_json(data, title):
    """Pretty print JSON data with a title."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print('='*80)
    print(json.dumps(data, indent=2))
    print('='*80)

def save_json_to_file(data, filename):
    """Save JSON data to a file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved to: {filepath}")
    return filepath

def load_profile(segment: str):
    """Load profile metadata from JSON file."""
    profile_file = os.path.join("profiles", f"{segment}.json")
    
    if not os.path.exists(profile_file):
        print(f"Profile file not found: {profile_file}")
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
            
    except Exception as e:
        print(f"Error loading profile {profile_file}: {e}")
        return []

def create_start_session_payload(segment: str, meta_fields: list):
    """Create START_SESSION request payload."""
    platform_name = "mobile" if "mobile" in segment.lower() else "web"
    
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

def create_user_message_payload(session_id: str, segment: str, meta_fields: list, message_text: str):
    """Create USER_MESSAGE request payload."""
    platform_name = "mobile" if "mobile" in segment.lower() else "web"
    
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

def get_common_headers():
    """Get common headers for API requests."""
    return {
        "Content-Type": "application/json",
        "Authorization": BASIC_AUTH,
        "secret": SECRET,
        "assistant_name": ASSISTANT_NAME,
        "assistant_target": ASSISTANT_TARGET
    }

def run_single_test():
    """Run a single test case with full logging."""
    # Test parameters
    segment = "bt_account__advised_super"
    intent = "advised_super_add_funds_intent"
    trigger_text = "How do I add money to my BT super?"
    
    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'#'*80}")
    print(f"# CAPI SINGLE TEST EXECUTION")
    print(f"# Segment: {segment}")
    print(f"# Intent: {intent}")
    print(f"# Trigger: {trigger_text}")
    print(f"# Timestamp: {timestamp}")
    print(f"{'#'*80}")
    
    # Create summary file
    summary = {
        "test_info": {
            "segment": segment,
            "intent": intent,
            "trigger_text": trigger_text,
            "timestamp": timestamp
        },
        "payloads": {}
    }
    
    # Load profile metadata
    meta_fields = load_profile(segment)
    print(f"\nLoaded {len(meta_fields)} meta fields from profile")
    
    # Step 1: Start Session
    print(f"\n{'='*80}")
    print("STEP 1: START SESSION")
    print('='*80)
    
    start_payload = create_start_session_payload(segment, meta_fields)
    headers = get_common_headers()
    
    pretty_print_json(start_payload, "START SESSION REQUEST PAYLOAD")
    save_json_to_file(start_payload, f"01_start_session_request_{timestamp}.json")
    summary["payloads"]["start_session_request"] = start_payload
    
    print("\nSending START_SESSION request...")
    start_response = requests.post(START_SESSION_URL, json=start_payload, headers=headers, timeout=30)
    
    print(f"Response Status Code: {start_response.status_code}")
    
    if start_response.status_code == 200:
        start_data = start_response.json()
        pretty_print_json(start_data, "START SESSION RESPONSE")
        save_json_to_file(start_data, f"02_start_session_response_{timestamp}.json")
        summary["payloads"]["start_session_response"] = start_data
        
        # Extract session ID
        session_id = start_data.get('context', {}).get('user', {}).get('session_id')
        print(f"\nExtracted Session ID: {session_id}")
        summary["session_id"] = session_id
        
        if session_id:
            # Step 2: Send User Message
            print(f"\n{'='*80}")
            print("STEP 2: USER MESSAGE")
            print('='*80)
            
            message_payload = create_user_message_payload(session_id, segment, meta_fields, trigger_text)
            
            pretty_print_json(message_payload, "USER MESSAGE REQUEST PAYLOAD")
            save_json_to_file(message_payload, f"03_user_message_request_{timestamp}.json")
            summary["payloads"]["user_message_request"] = message_payload
            
            print("\nSending USER_MESSAGE request...")
            message_response = requests.post(USER_MESSAGE_URL, json=message_payload, headers=headers, timeout=30)
            
            print(f"Response Status Code: {message_response.status_code}")
            
            if message_response.status_code == 200:
                message_data = message_response.json()
                pretty_print_json(message_data, "USER MESSAGE RESPONSE")
                save_json_to_file(message_data, f"04_user_message_response_{timestamp}.json")
                summary["payloads"]["user_message_response"] = message_data
                
                # Extract key information
                print(f"\n{'='*80}")
                print("EXTRACTED RESPONSE INFORMATION")
                print('='*80)
                
                # Extract intent
                nlu_details = message_data.get('context', {}).get('nlu_details', {})
                predicted = nlu_details.get('predicted', {})
                triggered_intent = predicted.get('triggered_intent', {})
                actual_intent = triggered_intent.get('name', 'N/A')
                confidence = triggered_intent.get('confidence', 0)
                
                print(f"Detected Intent: {actual_intent}")
                print(f"Confidence: {confidence}")
                
                summary["results"] = {
                    "detected_intent": actual_intent,
                    "confidence": confidence,
                    "expected_intent": intent,
                    "match": actual_intent == intent
                }
                
                # Extract response text
                message_contents = message_data.get('message_contents', [])
                response_texts = []
                for item in message_contents:
                    if item.get('type') == 'TEXT':
                        text = item.get('payload', {}).get('text', '')
                        if text:
                            response_texts.append(text)
                
                if response_texts:
                    print(f"\nResponse Text:")
                    for text in response_texts:
                        print(f"  {text}")
                    summary["results"]["response_texts"] = response_texts
                
                # Extract buttons/quick replies
                quick_replies = message_data.get('quick_replies', [])
                if quick_replies:
                    print(f"\nQuick Reply Buttons:")
                    button_labels = []
                    for qr in quick_replies:
                        label = qr.get('label', 'N/A')
                        print(f"  - {label}")
                        button_labels.append(label)
                    summary["results"]["quick_replies"] = button_labels
                
            else:
                print(f"USER_MESSAGE request failed: {message_response.text}")
                summary["error"] = f"USER_MESSAGE failed: {message_response.status_code}"
        else:
            print("Failed to extract session ID from START_SESSION response")
            summary["error"] = "No session ID in response"
    else:
        print(f"START_SESSION request failed: {start_response.text}")
        summary["error"] = f"START_SESSION failed: {start_response.status_code}"
    
    # Save summary file
    save_json_to_file(summary, f"00_test_summary_{timestamp}.json")
    
    print(f"\n{'#'*80}")
    print(f"# TEST EXECUTION COMPLETE")
    print(f"# All JSON payloads saved to: {OUTPUT_DIR}/")
    print(f"{'#'*80}\n")

if __name__ == "__main__":
    run_single_test()