#!/usr/bin/env python3
"""
Segment Intent Validator
Checks if an intent is enabled for a given segment combination
"""

import json
import os
from typing import Dict, List, Set, Optional
from pathlib import Path

class SegmentIntentValidator:
    """Validates which intents are enabled for which segments"""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.intents_dir = self.base_path / "intents"
        self.responses_dir = self.base_path / "responses"
        self.segments_dir = self.base_path / "segments"
        self.disabled_intents = {}
        self.intent_configs = {}
        self.segment_configs = {}
        self.global_disabled_intents = set()
        self._load_disabled_responses()
        self._load_intent_configs()
        self._load_segment_configs()
    
    def _load_disabled_responses(self):
        """Load all disabled intent responses"""
        disabled_files = list(self.responses_dir.glob("IntentMessageDisabled*.json"))
        
        for file_path in disabled_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Extract intent name from filename
                filename = file_path.stem
                raw_intent = filename.replace("IntentMessageDisabled", "")
                
                # Convert btdepositfunds -> bt_deposit_funds
                if raw_intent.startswith("bt") and "_" not in raw_intent:
                    # Handle common patterns first
                    intent_name = raw_intent.replace("depositfunds", "deposit_funds")
                    intent_name = intent_name.replace("requestforwithdrawal", "request_for_withdrawal") 
                    intent_name = intent_name.replace("assettransfer", "asset_transfer")
                    
                    # Ensure bt_ prefix
                    if not intent_name.startswith("bt_"):
                        intent_name = intent_name.replace("bt", "bt_", 1)
                else:
                    intent_name = raw_intent
                
                print(f"Parsed disabled intent: {filename} -> {intent_name}")
                
                # Get disabled segments
                disabled_segments = set()
                
                # Check segment_responses for explicit disabled segments
                for segment_response in data.get('segment_responses', []):
                    segment_name = segment_response.get('segment_name')
                    if segment_name:
                        disabled_segments.add(segment_name)
                
                self.disabled_intents[intent_name] = disabled_segments
                
            except Exception as e:
                print(f"Error loading disabled intent {file_path}: {e}")
    
    def _load_intent_configs(self):
        """Load intent configurations to understand enabled segments"""
        for intent_file in self.intents_dir.glob("*.json"):
            try:
                with open(intent_file, 'r') as f:
                    data = json.load(f)
                
                intent_name = data.get('name', intent_file.stem)
                self.intent_configs[intent_name] = data
                
            except Exception as e:
                print(f"Error loading intent config {intent_file}: {e}")
    
    def _load_segment_configs(self):
        """Load segment configurations including global segment"""
        if self.segments_dir.exists():
            for segment_file in self.segments_dir.glob("*.json"):
                try:
                    with open(segment_file, 'r') as f:
                        data = json.load(f)
                    
                    segment_name = data.get('name', segment_file.stem)
                    self.segment_configs[segment_name] = data
                    
                    # Special handling for global segment
                    if segment_name == 'global':
                        disabled_actions = data.get('disabled_actions', [])
                        self.global_disabled_intents = set(disabled_actions)
                        print(f"Loaded global disabled intents: {disabled_actions}")
                    
                except Exception as e:
                    print(f"Error loading segment config {segment_file}: {e}")
        
        print(f"Loaded {len(self.segment_configs)} segment configurations")
    
    def is_intent_enabled_for_segment(self, intent_name: str, segment_name: str) -> bool:
        """Check if an intent is enabled for a specific segment"""
        
        # CRITICAL: First check if intent is disabled globally
        # If an intent is in the global segment's disabled_actions, it's effectively switched off system-wide
        if intent_name in self.global_disabled_intents:
            # Intent is globally disabled - cannot be tested for ANY segment
            return False
        
        # Handle "default" segment mapping
        actual_segments = self._resolve_segment_names(segment_name)
        
        # Check if intent is in the segment's disabled_actions
        if segment_name in self.segment_configs:
            segment_disabled_actions = self.segment_configs[segment_name].get('disabled_actions', [])
            if intent_name in segment_disabled_actions:
                return False
        
        # Check if intent is explicitly disabled for any of the actual segments (from IntentMessageDisabled files)
        if intent_name in self.disabled_intents:
            disabled_segments = self.disabled_intents[intent_name]
            for seg in actual_segments:
                if seg in disabled_segments:
                    return False
        
        # Special cases based on naming patterns
        for seg in actual_segments:
            if not self._check_segment_compatibility(intent_name, seg):
                return False
        
        return True
    
    def _resolve_segment_names(self, segment_name: str) -> List[str]:
        """Resolve segment name to actual segment list (handles 'default' case)"""
        if segment_name == "default":
            # Default maps to basic account segments (based on API response)
            return ["bt_account_super", "global"]
        else:
            return [segment_name]
    
    def _check_segment_compatibility(self, intent_name: str, segment_name: str) -> bool:
        """Check compatibility based on naming patterns and business logic"""
        
        # Pension-specific restrictions
        if "pension" in segment_name.lower():
            # Deposit funds not applicable to pension accounts
            if "deposit_funds" in intent_name:
                return False
        
        # Public/unauthenticated channel restrictions  
        if any(pattern in segment_name.lower() for pattern in ["public", "bt_account_super"]):
            # bt_account_super appears to be a basic/public segment requiring authentication
            # Many secure functions require proper login/profile
            restricted_intents = [
                "deposit_funds", "withdrawal", "balance", "transactions", 
                "account_details", "personal_tax", "statements"
            ]
            if any(restricted in intent_name for restricted in restricted_intents):
                return False
        
        # Investment vs Super account restrictions
        if "investment" in segment_name.lower():
            super_only_intents = [
                "rollover", "pension", "super_early", "centrelink", 
                "minimum_pension", "pension_payment"
            ]
            if any(super_intent in intent_name for super_intent in super_only_intents):
                return False
        
        return True
    
    def get_valid_segments_for_intent(self, intent_name: str) -> List[str]:
        """Get list of segments where this intent should be enabled"""
        valid_segments = []
        
        # Get all segment names from profiles directory
        profiles_dir = self.base_path / "profiles"
        for profile_file in profiles_dir.glob("*.json"):
            segment_name = profile_file.stem
            if self.is_intent_enabled_for_segment(intent_name, segment_name):
                valid_segments.append(segment_name)
        
        return valid_segments
    
    def get_valid_intents_for_segment(self, segment_name: str) -> List[str]:
        """Get list of intents that should be enabled for this segment"""
        valid_intents = []
        
        for intent_name in self.intent_configs.keys():
            if self.is_intent_enabled_for_segment(intent_name, segment_name):
                valid_intents.append(intent_name)
        
        return valid_intents
    
    def validate_test_case(self, intent_name: str, segment_name: str) -> Dict:
        """Validate if a test case should be created for this intent/segment combo"""
        result = {
            'intent': intent_name,
            'segment': segment_name
        }
        
        # Check if intent is globally disabled first
        if intent_name in self.global_disabled_intents:
            result['valid'] = False
            result['expected_behavior'] = 'globally_disabled'
            result['reason'] = 'intent_disabled_globally'
            result['message'] = f'Intent {intent_name} is in the global segment disabled_actions - effectively switched off system-wide'
            return result
        
        # Now check if enabled for specific segment
        is_valid = self.is_intent_enabled_for_segment(intent_name, segment_name)
        result['valid'] = is_valid
        
        if not is_valid:
            # Determine expected behavior
            if intent_name in self.disabled_intents:
                disabled_segments = self.disabled_intents[intent_name]
                if segment_name in disabled_segments:
                    result['expected_behavior'] = 'disabled_response'
                    result['reason'] = 'explicitly_disabled'
                else:
                    result['expected_behavior'] = 'fallback_response'
                    result['reason'] = 'not_applicable'
            else:
                result['expected_behavior'] = 'fallback_response'
                result['reason'] = 'segment_incompatible'
        
        return result

def main():
    """Test the validator"""
    validator = SegmentIntentValidator()
    
    # Test the problematic case
    result = validator.validate_test_case("bt_deposit_funds", "default")
    print("bt_deposit_funds + default segment:")
    print(json.dumps(result, indent=2))
    
    # Get valid segments for bt_deposit_funds
    valid_segments = validator.get_valid_segments_for_intent("bt_deposit_funds")
    print(f"\nValid segments for bt_deposit_funds: {valid_segments}")
    
    # Test with a specific enabled segment
    if valid_segments:
        result = validator.validate_test_case("bt_deposit_funds", valid_segments[0])
        print(f"\nbt_deposit_funds + {valid_segments[0]}:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()