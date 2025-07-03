#!/usr/bin/env python3
"""
Generate Segment-Intent-Response Matrix CSV (File-based version)
Creates a CSV with example triggers and expected responses by reading directly from files
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Set
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class FileBasedMatrixGenerator:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.segments = {}
        self.intents = {}
        self.responses = {}
        
    def load_all_data(self):
        """Load all data from files"""
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
    
    def get_intent_response_name(self, intent_name: str) -> Optional[str]:
        """Get the response name for an intent"""
        intent = self.intents.get(intent_name, {})
        
        # Check webhook_params first
        webhook_params = intent.get('webhook_params', {})
        if 'response_name' in webhook_params:
            return webhook_params['response_name']
        
        # Check responses array
        responses = intent.get('responses', [])
        if responses:
            return responses[0]
        
        # Try common pattern
        if f"{intent_name}_response" in self.responses:
            return f"{intent_name}_response"
        
        return None
    
    def get_example_trigger(self, intent_name: str) -> str:
        """Get an example trigger for an intent from intent_data files"""
        # Try to load from intent_data file
        intent_data_file = self.base_path / 'intent_data' / f'intent_data_{intent_name}.json'
        
        if intent_data_file.exists():
            try:
                with open(intent_data_file, 'r') as f:
                    data = json.load(f)
                
                # The file contains an array of trigger objects
                if isinstance(data, list) and len(data) > 0:
                    # Find the first active trigger
                    for item in data:
                        if item.get('active', True) and item.get('type') == 'TRIGGER':
                            trigger = item.get('trigger_sentence', '')
                            if trigger:
                                # Clean up entity placeholders
                                # Replace {@entity_type value} with just value
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
        
        # Fallback: check intent display_sentence
        intent = self.intents.get(intent_name, {})
        if 'display_sentence' in intent:
            return intent['display_sentence']
        
        # Last resort: generate from intent name
        clean_name = intent_name.replace('bt_', '').replace('kcb_', '').replace('_', ' ')
        return f"Help with {clean_name}"
    
    def extract_response_text(self, response_data: Dict) -> Dict:
        """Extract text and buttons separately from response data structure"""
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
    
    def generate_matrix_csv(self, output_file: str, sample_only: bool = False):
        """Generate the segment-intent matrix CSV"""
        csv_data = []
        invalid_tests = []  # Track invalid/disabled tests
        
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
        
        for segment_name in segment_names:
            segment = self.segments[segment_name]
            disabled_actions = set(segment.get('disabled_actions', []))
            
            for intent_name in intent_names:
                intent = self.intents[intent_name]
                
                # Check if intent is enabled for this segment
                is_enabled = intent_name not in disabled_actions
                
                # Get example trigger
                example_trigger = self.get_example_trigger(intent_name)
                
                # Get response
                response_text = "N/A"
                response_buttons = []
                response_type = "N/A"
                
                if is_enabled:
                    response_name = self.get_intent_response_name(intent_name)
                    if response_name and response_name in self.responses:
                        response_data = self.responses[response_name]
                        
                        # Check for segment-specific response
                        segment_specific = None
                        for seg_resp in response_data.get('segment_responses', []):
                            if seg_resp.get('segment_name') == segment_name:
                                segment_specific = seg_resp.get('response', {})
                                break
                        
                        if segment_specific:
                            extracted = self.extract_response_text(segment_specific)
                            response_text = extracted["text"]
                            response_buttons = extracted["buttons"]
                            response_type = "Segment-specific"
                        else:
                            # Use default response
                            default_resp = response_data.get('default_response', {})
                            extracted = self.extract_response_text(default_resp)
                            response_text = extracted["text"]
                            response_buttons = extracted["buttons"]
                            response_type = "Default"
                else:
                    response_text = "Intent disabled for this segment"
                    response_type = "Disabled"
                
                # Create row data
                row_data = {
                    'segment': segment_name,
                    'segment_description': segment.get('description', ''),
                    'segment_active': 'Yes' if segment.get('active', True) else 'No',
                    'intent': intent_name,
                    'intent_display_name': intent.get('display_name', intent_name),
                    'enabled_for_segment': 'Yes' if is_enabled else 'No',
                    'example_trigger': example_trigger,
                    'response_type': response_type,
                    'expected_response': response_text,
                    'expected_buttons': '|'.join(response_buttons) if response_buttons else ''
                }
                
                # Check if this is a valid test case
                is_valid_test = (
                    response_text not in ["N/A", "Intent disabled for this segment"] and
                    segment.get('active', True) and
                    is_enabled
                )
                
                if is_valid_test:
                    csv_data.append(row_data)
                else:
                    # Track invalid test with reason
                    invalid_reason = []
                    if response_text == "N/A":
                        invalid_reason.append("No response defined")
                    if response_text == "Intent disabled for this segment":
                        invalid_reason.append("Intent disabled")
                    if not segment.get('active', True):
                        invalid_reason.append("Segment inactive")
                    if not is_enabled:
                        invalid_reason.append("Intent not enabled for segment")
                    
                    row_data['invalid_reason'] = '; '.join(invalid_reason)
                    invalid_tests.append(row_data)
        
        # Write CSV
        fieldnames = [
            'segment',
            'segment_description',
            'segment_active',
            'intent',
            'intent_display_name',
            'enabled_for_segment',
            'example_trigger',
            'response_type',
            'expected_response',
            'expected_buttons'
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
        self._print_summary(csv_data, len(invalid_tests))
    
    def _write_invalid_tests(self, invalid_tests: List[Dict], output_file: str):
        """Write invalid tests to separate CSV and markdown files."""
        from pathlib import Path
        from datetime import datetime
        
        base_name = Path(output_file).stem
        
        # Write invalid tests CSV
        invalid_csv = f"{base_name}_invalid_tests.csv"
        invalid_fieldnames = [
            'segment', 'segment_description', 'segment_active', 'intent', 'intent_display_name',
            'enabled_for_segment', 'example_trigger', 'response_type', 'expected_response', 
            'expected_buttons', 'invalid_reason'
        ]
        
        with open(invalid_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=invalid_fieldnames)
            writer.writeheader()
            writer.writerows(invalid_tests)
        
        # Write invalid tests markdown report
        invalid_md = f"{base_name}_invalid_tests_report.md"
        with open(invalid_md, 'w', encoding='utf-8') as mdfile:
            mdfile.write(f"# Invalid Test Cases Report\n\n")
            mdfile.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            mdfile.write(f"**Total Invalid Tests:** {len(invalid_tests)}\n\n")
            
            # Group by reason
            reason_groups = {}
            for test in invalid_tests:
                reason = test['invalid_reason']
                if reason not in reason_groups:
                    reason_groups[reason] = []
                reason_groups[reason].append(test)
            
            mdfile.write("## Summary by Reason\n\n")
            for reason, tests in sorted(reason_groups.items(), key=lambda x: len(x[1]), reverse=True):
                mdfile.write(f"- **{reason}**: {len(tests)} tests\n")
            
            mdfile.write("\n## Detailed Breakdown\n\n")
            for reason, tests in sorted(reason_groups.items(), key=lambda x: len(x[1]), reverse=True):
                mdfile.write(f"### {reason} ({len(tests)} tests)\n\n")
                mdfile.write("| Segment | Intent | Description |\n")
                mdfile.write("|---------|--------|-----------|\n")
                
                for test in sorted(tests, key=lambda x: (x['segment'], x['intent']))[:20]:  # Limit to 20 for readability
                    segment = test['segment']
                    intent = test['intent_display_name'] or test['intent']
                    desc = test['segment_description'][:50] + "..." if len(test['segment_description']) > 50 else test['segment_description']
                    mdfile.write(f"| {segment} | {intent} | {desc} |\n")
                
                if len(tests) > 20:
                    mdfile.write(f"\n*... and {len(tests) - 20} more tests*\n")
                mdfile.write("\n")
        
        logger.info(f"✅ Generated invalid tests report: {invalid_csv} and {invalid_md}")
    
    def _print_summary(self, csv_data: List[Dict], invalid_count: int):
        """Print summary statistics"""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        valid_rows = len(csv_data)
        total_combinations = valid_rows + invalid_count
        enabled_count = sum(1 for row in csv_data if row['enabled_for_segment'] == 'Yes')
        disabled_count = valid_rows - enabled_count
        
        print(f"\nTotal combinations generated: {total_combinations}")
        print(f"Valid test cases: {valid_rows} ({valid_rows/total_combinations*100:.1f}%)")
        print(f"Invalid/excluded test cases: {invalid_count} ({invalid_count/total_combinations*100:.1f}%)")
        print(f"\nOf valid test cases:")
        print(f"  Enabled combinations: {enabled_count} ({enabled_count/valid_rows*100:.1f}%)")
        print(f"  Disabled combinations: {disabled_count} ({disabled_count/valid_rows*100:.1f}%)")
        
        # Count response types
        response_types = {}
        for row in csv_data:
            rt = row['response_type']
            response_types[rt] = response_types.get(rt, 0) + 1
        
        print("\nResponse type distribution:")
        for rt, count in sorted(response_types.items()):
            print(f"  {rt}: {count} ({count/valid_rows*100:.1f}%)")
        
        # Segments with most customization
        segment_custom_counts = {}
        for row in csv_data:
            if row['response_type'] == 'Segment-specific':
                seg = row['segment']
                segment_custom_counts[seg] = segment_custom_counts.get(seg, 0) + 1
        
        if segment_custom_counts:
            print("\nSegments with most customized responses:")
            for seg, count in sorted(segment_custom_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {seg}: {count} customized responses")


def main():
    # Base path for data files
    BASE_PATH = "/Users/jaskew/workspace/Skynet/desktop/claude/test"
    
    # Create generator
    generator = FileBasedMatrixGenerator(BASE_PATH)
    
    # Load all data
    generator.load_all_data()
    
    # Generate sample CSV first
    logger.info("\nGenerating sample CSV...")
    generator.generate_matrix_csv("segment_intent_matrix_sample.csv", sample_only=True)
    
    # Generate full CSV
    logger.info("\nGenerating full CSV...")
    generator.generate_matrix_csv("segment_intent_matrix_full.csv", sample_only=False)
    
    print("\n✅ Generated files:")
    print("  - segment_intent_matrix_sample.csv (subset for review)")
    print("  - segment_intent_matrix_full.csv (complete matrix)")


if __name__ == "__main__":
    main()
