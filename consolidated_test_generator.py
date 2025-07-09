#!/usr/bin/env python3
"""
Consolidated Test Generator
Combines all test types (matrix, conversation flow, intent navigation) into unified CSV files
Generates both CAPI and HOOT formats with datetime in filenames
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime
import logging

# Import the other generators
from generate_matrix_with_segment_matching import SegmentMatchingMatrixGenerator
from conversation_flow_test_generator import ConversationFlowTestGenerator
from intent_navigation_test_generator import IntentNavigationTestGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConsolidatedTestGenerator:
    """Generate consolidated test suites combining all test types"""
    
    def __init__(self, base_path: str = '.'):
        self.base_path = Path(base_path)
        self.matrix_generator = SegmentMatchingMatrixGenerator(str(self.base_path))
        self.conversation_generator = ConversationFlowTestGenerator(str(self.base_path))
        self.navigation_generator = IntentNavigationTestGenerator(str(self.base_path))
        
        # Generate timestamp for filenames
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
    def load_all_data(self):
        """Load all data from all generators"""
        logger.info("Loading data for all generators...")
        
        # Load data for each generator
        self.matrix_generator.load_all_data()
        self.conversation_generator.load_data()
        self.navigation_generator.load_data()
        
        logger.info("✅ All data loaded successfully")
        
    def generate_matrix_tests(self, format_type: str = "standard") -> List[Dict]:
        """Generate matrix tests using the existing generator"""
        logger.info(f"Generating matrix tests in {format_type} format...")
        
        # Create temporary file to capture matrix tests
        temp_file = f"temp_matrix_{self.timestamp}.csv"
        
        try:
            # Generate matrix tests
            self.matrix_generator.generate_matrix_csv(temp_file, sample_only=False, format_type=format_type)
            
            # Read the generated file
            tests = []
            with open(temp_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['test_source'] = 'matrix'
                    tests.append(row)
            
            logger.info(f"✅ Generated {len(tests)} matrix tests")
            return tests
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def generate_conversation_flow_tests(self, format_type: str = "standard") -> List[Dict]:
        """Generate conversation flow tests"""
        logger.info(f"Generating conversation flow tests in {format_type} format...")
        
        # Generate conversation flow tests
        test_suite = self.conversation_generator.generate_comprehensive_flow_tests()
        
        if format_type == "hoot":
            return self._convert_conversation_tests_to_hoot(test_suite['conversation_tests'])
        else:
            return self._convert_conversation_tests_to_capi(test_suite['conversation_tests'])
    
    def generate_intent_navigation_tests(self, format_type: str = "standard") -> List[Dict]:
        """Generate intent navigation tests"""
        logger.info(f"Generating intent navigation tests in {format_type} format...")
        
        # Generate navigation tests
        test_suite = self.navigation_generator.generate_comprehensive_navigation_tests()
        
        if format_type == "hoot":
            return self._convert_navigation_tests_to_hoot(test_suite['navigation_tests'])
        else:
            return self._convert_navigation_tests_to_capi(test_suite['navigation_tests'])
    
    def _convert_conversation_tests_to_capi(self, tests: List[Dict]) -> List[Dict]:
        """Convert conversation flow tests to CAPI format"""
        capi_tests = []
        
        for test in tests:
            # Create a row for each turn in the conversation
            base_row = {
                'test_source': 'conversation_flow',
                'test_type': test.get('test_type', 'conversation_flow'),
                'intent': test.get('intent', ''),
                'segment': test.get('segment', 'default'),
                'description': test.get('description', ''),
                'total_turns': len(test.get('turns', [])),
                'enabled_for_segment': 'Yes',  # These are pre-validated
                'intent_active': 'Yes',
                'segment_active': 'Yes'
            }
            
            # Add information from all turns
            turns = test.get('turns', [])
            if turns:
                first_turn = turns[0]
                base_row.update({
                    'example_trigger': first_turn.get('user_input', ''),
                    'expected_response': first_turn.get('expected_response_content', ''),  # Use actual content, not filename
                    'expected_buttons': '|'.join(first_turn.get('expected_quick_replies', [])),
                    'response_type': 'Conversation Flow'
                })
                
                # Add second turn information if exists
                if len(turns) > 1:
                    second_turn = turns[1]
                    base_row.update({
                        'turn_2_input': second_turn.get('user_input', ''),
                        'turn_2_expected_response': second_turn.get('expected_response_content', ''),  # Use actual content, not filename
                        'turn_2_expected_content': second_turn.get('expected_response_content', ''),
                        'slot_name': second_turn.get('slot_name', ''),
                        'user_input_label': second_turn.get('user_input_label', '')
                    })
            
            capi_tests.append(base_row)
        
        logger.info(f"✅ Converted {len(capi_tests)} conversation flow tests to CAPI format")
        return capi_tests
    
    def _convert_navigation_tests_to_capi(self, tests: List[Dict]) -> List[Dict]:
        """Convert intent navigation tests to CAPI format"""
        capi_tests = []
        
        for test in tests:
            # Skip non-navigation tests
            if test.get('test_type') != 'intent_navigation':
                continue
                
            base_row = {
                'test_source': 'intent_navigation',
                'test_type': test.get('test_type', 'intent_navigation'),
                'intent': test.get('source_intent', ''),
                'segment': test.get('segment', 'default'),
                'description': test.get('description', ''),
                'total_turns': len(test.get('turns', [])),
                'enabled_for_segment': 'Yes',  # These are pre-validated
                'intent_active': 'Yes',
                'segment_active': 'Yes',
                'source_intent': test.get('source_intent', ''),
                'target_intent': test.get('target_intent', ''),
                'navigation_type': test.get('navigation_type', ''),
                'source_response': test.get('source_response', ''),
                'target_response': test.get('target_response', ''),
                'response_type': 'Intent Navigation'
            }
            
            # Add information from turns
            turns = test.get('turns', [])
            if turns:
                first_turn = turns[0]
                # For intent navigation tests, use the actual content as expected_response
                first_turn_content = first_turn.get('expected_response_content', '')
                base_row.update({
                    'example_trigger': first_turn.get('user_input', ''),
                    'expected_response': first_turn_content if first_turn_content else first_turn.get('expected_response', ''),
                    'expected_buttons': '|'.join(first_turn.get('expected_navigation_options', [])),
                })
                
                # Add second turn information if exists
                if len(turns) > 1:
                    second_turn = turns[1]
                    # For intent navigation tests, use the actual content as expected_response
                    expected_response_content = second_turn.get('expected_response_content', '')
                    base_row.update({
                        'turn_2_input': second_turn.get('user_input', ''),
                        'turn_2_expected_response': expected_response_content if expected_response_content else second_turn.get('expected_response', ''),
                        'turn_2_expected_content': expected_response_content,
                        'user_action': second_turn.get('user_action', ''),
                        'expected_intent': second_turn.get('expected_intent', '')
                    })
            
            capi_tests.append(base_row)
        
        logger.info(f"✅ Converted {len(capi_tests)} intent navigation tests to CAPI format")
        return capi_tests
    
    def _convert_conversation_tests_to_hoot(self, tests: List[Dict]) -> List[Dict]:
        """Convert conversation flow tests to HOOT format"""
        hoot_tests = []
        
        # Initialize counters for hoot format
        test_case_summary_id = 5000  # Starting ID to avoid conflicts
        test_case_detail_id = 10000   # Starting ID to avoid conflicts
        
        for test in tests:
            segment_name = test.get('segment', 'default')
            intent_name = test.get('intent', '')
            turns = test.get('turns', [])
            
            if not turns:
                continue
                
            # Create test case name
            test_case_name = f"{segment_name.upper()}_{intent_name}_ConversationFlow"
            
            # Default meta tags for segment
            meta_tags = f'[{{"key":"semantic_group:","value":"default"}},{{"key":"semantic_group_secondary:","value":"default"}}]'
            
            current_step_id = 0
            
            # Row 1: start-session
            hoot_tests.append({
                'test_plan_name': segment_name.upper(),
                'run_time': '',
                'run_schedule': 'null',
                'testing_phase': 'Depth',
                'endpoint_id': '85',
                'endpoint_type': 'Kasisto',
                'test_case_summary_id': test_case_summary_id,
                'test_case_name': test_case_name,
                'test_case_type': 'DEPTH',
                'active': 'TRUE',
                'test_case_detail_id': test_case_detail_id,
                'step_id': current_step_id,
                'action': 'start-session',
                'object': 'event',
                'value': 'start-session',
                'meta_tags': meta_tags
            })
            test_case_detail_id += 1
            current_step_id += 1
            
            # Process each turn
            for turn in turns:
                user_input = turn.get('user_input', '')
                expected_response = turn.get('expected_response', '')
                expected_content = turn.get('expected_response_content', '')
                
                # Add user input
                hoot_tests.append({
                    'test_plan_name': segment_name.upper(),
                    'run_time': '',
                    'run_schedule': 'null',
                    'testing_phase': 'Depth',
                    'endpoint_id': '85',
                    'endpoint_type': 'Kasisto',
                    'test_case_summary_id': test_case_summary_id,
                    'test_case_name': test_case_name,
                    'test_case_type': 'DEPTH',
                    'active': 'TRUE',
                    'test_case_detail_id': test_case_detail_id,
                    'step_id': current_step_id,
                    'action': 'user-input',
                    'object': 'text',
                    'value': user_input,
                    'meta_tags': meta_tags
                })
                test_case_detail_id += 1
                current_step_id += 1
                
                # Add expected response validation
                if expected_content:
                    hoot_tests.append({
                        'test_plan_name': segment_name.upper(),
                        'run_time': '',
                        'run_schedule': 'null',
                        'testing_phase': 'Depth',
                        'endpoint_id': '85',
                        'endpoint_type': 'Kasisto',
                        'test_case_summary_id': test_case_summary_id,
                        'test_case_name': test_case_name,
                        'test_case_type': 'DEPTH',
                        'active': 'TRUE',
                        'test_case_detail_id': test_case_detail_id,
                        'step_id': current_step_id,
                        'action': 'object-semantics',
                        'object': 'message_contents[0].payload.text',
                        'value': expected_content,
                        'meta_tags': meta_tags
                    })
                    test_case_detail_id += 1
                    current_step_id += 1
                
                # Add quick reply validations
                expected_quick_replies = turn.get('expected_quick_replies', [])
                for i, qr in enumerate(expected_quick_replies):
                    hoot_tests.append({
                        'test_plan_name': segment_name.upper(),
                        'run_time': '',
                        'run_schedule': 'null',
                        'testing_phase': 'Depth',
                        'endpoint_id': '85',
                        'endpoint_type': 'Kasisto',
                        'test_case_summary_id': test_case_summary_id,
                        'test_case_name': test_case_name,
                        'test_case_type': 'DEPTH',
                        'active': 'TRUE',
                        'test_case_detail_id': test_case_detail_id,
                        'step_id': current_step_id,
                        'action': 'object-semantics',
                        'object': f'quick_replies[{i}].label',
                        'value': qr,
                        'meta_tags': meta_tags
                    })
                    test_case_detail_id += 1
                    current_step_id += 1
            
            test_case_summary_id += 1
        
        logger.info(f"✅ Converted {len(tests)} conversation flow tests to {len(hoot_tests)} HOOT format rows")
        return hoot_tests
    
    def _convert_navigation_tests_to_hoot(self, tests: List[Dict]) -> List[Dict]:
        """Convert intent navigation tests to HOOT format"""
        hoot_tests = []
        
        # Initialize counters for hoot format
        test_case_summary_id = 6000  # Starting ID to avoid conflicts
        test_case_detail_id = 12000   # Starting ID to avoid conflicts
        
        for test in tests:
            # Skip non-navigation tests
            if test.get('test_type') != 'intent_navigation':
                continue
                
            segment_name = test.get('segment', 'default')
            source_intent = test.get('source_intent', '')
            target_intent = test.get('target_intent', '')
            turns = test.get('turns', [])
            
            if not turns:
                continue
                
            # Create test case name
            test_case_name = f"{segment_name.upper()}_{source_intent}_to_{target_intent}_Navigation"
            
            # Default meta tags for segment
            meta_tags = f'[{{"key":"semantic_group:","value":"default"}},{{"key":"semantic_group_secondary:","value":"default"}}]'
            
            current_step_id = 0
            
            # Row 1: start-session
            hoot_tests.append({
                'test_plan_name': segment_name.upper(),
                'run_time': '',
                'run_schedule': 'null',
                'testing_phase': 'Depth',
                'endpoint_id': '85',
                'endpoint_type': 'Kasisto',
                'test_case_summary_id': test_case_summary_id,
                'test_case_name': test_case_name,
                'test_case_type': 'DEPTH',
                'active': 'TRUE',
                'test_case_detail_id': test_case_detail_id,
                'step_id': current_step_id,
                'action': 'start-session',
                'object': 'event',
                'value': 'start-session',
                'meta_tags': meta_tags
            })
            test_case_detail_id += 1
            current_step_id += 1
            
            # Process each turn
            for turn in turns:
                user_input = turn.get('user_input', '')
                expected_response = turn.get('expected_response', '')
                expected_content = turn.get('expected_response_content', '')
                
                # Add user input
                hoot_tests.append({
                    'test_plan_name': segment_name.upper(),
                    'run_time': '',
                    'run_schedule': 'null',
                    'testing_phase': 'Depth',
                    'endpoint_id': '85',
                    'endpoint_type': 'Kasisto',
                    'test_case_summary_id': test_case_summary_id,
                    'test_case_name': test_case_name,
                    'test_case_type': 'DEPTH',
                    'active': 'TRUE',
                    'test_case_detail_id': test_case_detail_id,
                    'step_id': current_step_id,
                    'action': 'user-input',
                    'object': 'text',
                    'value': user_input,
                    'meta_tags': meta_tags
                })
                test_case_detail_id += 1
                current_step_id += 1
                
                # Add expected response validation
                if expected_content:
                    hoot_tests.append({
                        'test_plan_name': segment_name.upper(),
                        'run_time': '',
                        'run_schedule': 'null',
                        'testing_phase': 'Depth',
                        'endpoint_id': '85',
                        'endpoint_type': 'Kasisto',
                        'test_case_summary_id': test_case_summary_id,
                        'test_case_name': test_case_name,
                        'test_case_type': 'DEPTH',
                        'active': 'TRUE',
                        'test_case_detail_id': test_case_detail_id,
                        'step_id': current_step_id,
                        'action': 'object-semantics',
                        'object': 'message_contents[0].payload.text',
                        'value': expected_content,
                        'meta_tags': meta_tags
                    })
                    test_case_detail_id += 1
                    current_step_id += 1
                
                # Add navigation options validation
                expected_navigation_options = turn.get('expected_navigation_options', [])
                for i, option in enumerate(expected_navigation_options):
                    hoot_tests.append({
                        'test_plan_name': segment_name.upper(),
                        'run_time': '',
                        'run_schedule': 'null',
                        'testing_phase': 'Depth',
                        'endpoint_id': '85',
                        'endpoint_type': 'Kasisto',
                        'test_case_summary_id': test_case_summary_id,
                        'test_case_name': test_case_name,
                        'test_case_type': 'DEPTH',
                        'active': 'TRUE',
                        'test_case_detail_id': test_case_detail_id,
                        'step_id': current_step_id,
                        'action': 'object-semantics',
                        'object': f'quick_replies[{i}].label',
                        'value': option,
                        'meta_tags': meta_tags
                    })
                    test_case_detail_id += 1
                    current_step_id += 1
            
            test_case_summary_id += 1
        
        logger.info(f"✅ Converted {len([t for t in tests if t.get('test_type') == 'intent_navigation'])} intent navigation tests to {len(hoot_tests)} HOOT format rows")
        return hoot_tests
    
    def generate_consolidated_test_suite(self, format_type: str = "standard"):
        """Generate consolidated test suite combining all test types"""
        logger.info(f"🚀 Starting consolidated test generation in {format_type} format...")
        
        # Load all data
        self.load_all_data()
        
        # Generate each type of test
        matrix_tests = self.generate_matrix_tests(format_type)
        conversation_tests = self.generate_conversation_flow_tests(format_type)
        navigation_tests = self.generate_intent_navigation_tests(format_type)
        
        # Combine all tests
        all_tests = matrix_tests + conversation_tests + navigation_tests
        
        # Add test case numbers to CAPI format tests
        if format_type != "hoot":
            test_case_number = 1
            for test in all_tests:
                test['test_case_number'] = test_case_number
                test_case_number += 1
            logger.info(f"✅ Added test case numbers to {len(all_tests)} tests")
        
        # Remove duplicates
        all_tests = self._remove_duplicate_tests(all_tests, format_type)
        
        # Generate filename with timestamp
        if format_type == "hoot":
            output_file = f"consolidated_tests_hoot_{self.timestamp}.csv"
            fieldnames = [
                'test_plan_name', 'run_time', 'run_schedule', 'testing_phase', 'endpoint_id',
                'endpoint_type', 'test_case_summary_id', 'test_case_name', 'test_case_type',
                'active', 'test_case_detail_id', 'step_id', 'action', 'object', 'value', 'meta_tags'
            ]
        else:
            output_file = f"consolidated_tests_capi_{self.timestamp}.csv"
            # Use comprehensive fieldnames for CAPI format
            fieldnames = [
                'test_case_number',  # Add test case number as first field
                'test_source', 'test_type', 'segment', 'segment_description', 'segment_active',
                'intent', 'intent_display_name', 'intent_active', 'enabled_for_segment',
                'example_trigger', 'response_type', 'expected_response', 'expected_buttons',
                'total_turns', 'description', 'turn_2_input', 'turn_2_expected_response',
                'turn_2_expected_content', 'slot_name', 'user_input_label', 'source_intent',
                'target_intent', 'navigation_type', 'source_response', 'target_response',
                'user_action', 'expected_intent'
            ]
        
        # Write consolidated CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_tests)
        
        # Generate statistics
        stats = self._generate_statistics(all_tests, format_type)
        
        # Generate summary report
        self._generate_summary_report(stats, output_file, format_type)
        
        logger.info(f"✅ Generated consolidated test suite: {output_file}")
        logger.info(f"📊 Total tests: {len(all_tests)}")
        
        return output_file, stats
    
    def _remove_duplicate_tests(self, tests: List[Dict], format_type: str) -> List[Dict]:
        """Remove duplicate tests based on key fields"""
        seen_tests = set()
        unique_tests = []
        
        for test in tests:
            # Create a unique key based on test type and key fields
            test_source = test.get('test_source', 'matrix')
            test_type = test.get('test_type', '')
            
            if format_type == "hoot":
                # For HOOT format, use test_case_name as the unique identifier
                test_key = test.get('test_case_name', '')
            else:
                # For CAPI format, create keys based on test source
                if test_source == 'matrix':
                    # For matrix tests: intent + segment
                    test_key = f"matrix_{test.get('intent', '')}_{test.get('segment', '')}"
                elif test_source == 'conversation_flow':
                    # For conversation flow: intent + segment + test_type + turn_2_input
                    test_key = f"conversation_{test.get('intent', '')}_{test.get('segment', '')}_{test_type}_{test.get('turn_2_input', '')}"
                elif test_source == 'intent_navigation':
                    # For navigation: source_intent + target_intent + segment
                    test_key = f"navigation_{test.get('source_intent', '')}_{test.get('target_intent', '')}_{test.get('segment', '')}"
                else:
                    # Fallback for any other test types
                    test_key = f"{test_source}_{test.get('intent', '')}_{test.get('segment', '')}"
            
            # Only add if we haven't seen this test before
            if test_key and test_key not in seen_tests:
                seen_tests.add(test_key)
                unique_tests.append(test)
        
        # Log deduplication results
        original_count = len(tests)
        unique_count = len(unique_tests)
        if original_count > unique_count:
            logger.info(f"🧹 Removed {original_count - unique_count} duplicate tests (from {original_count} to {unique_count})")
        
        return unique_tests
    
    def _generate_statistics(self, tests: List[Dict], format_type: str) -> Dict:
        """Generate statistics about the test suite"""
        stats = {
            'total_tests': len(tests),
            'format_type': format_type,
            'generated_at': datetime.now().isoformat(),
            'by_test_source': {},
            'by_test_type': {},
            'by_segment': {}
        }
        
        # Count by test source
        for test in tests:
            source = test.get('test_source', 'matrix')
            stats['by_test_source'][source] = stats['by_test_source'].get(source, 0) + 1
        
        # Count by test type
        for test in tests:
            test_type = test.get('test_type', 'matrix')
            stats['by_test_type'][test_type] = stats['by_test_type'].get(test_type, 0) + 1
        
        # Count by segment
        for test in tests:
            segment = test.get('segment', test.get('test_plan_name', 'unknown'))
            stats['by_segment'][segment] = stats['by_segment'].get(segment, 0) + 1
        
        return stats
    
    def _generate_summary_report(self, stats: Dict, output_file: str, format_type: str):
        """Generate a summary report"""
        report_file = f"test_generation_report_{self.timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write(f"# Consolidated Test Generation Report\n\n")
            f.write(f"**Generated:** {stats['generated_at']}\n")
            f.write(f"**Format:** {format_type.upper()}\n")
            f.write(f"**Output File:** {output_file}\n\n")
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Total Tests:** {stats['total_tests']}\n")
            f.write(f"- **Format Type:** {stats['format_type']}\n\n")
            
            f.write(f"## Test Distribution\n\n")
            f.write(f"### By Test Source\n\n")
            for source, count in sorted(stats['by_test_source'].items()):
                percentage = (count / stats['total_tests']) * 100
                f.write(f"- **{source}:** {count} ({percentage:.1f}%)\n")
            
            f.write(f"\n### By Test Type\n\n")
            for test_type, count in sorted(stats['by_test_type'].items()):
                percentage = (count / stats['total_tests']) * 100
                f.write(f"- **{test_type}:** {count} ({percentage:.1f}%)\n")
            
            f.write(f"\n### By Segment\n\n")
            for segment, count in sorted(stats['by_segment'].items()):
                percentage = (count / stats['total_tests']) * 100
                f.write(f"- **{segment}:** {count} ({percentage:.1f}%)\n")
            
            f.write(f"\n## Test Types Included\n\n")
            f.write(f"1. **Matrix Tests:** Standard intent/segment combinations\n")
            f.write(f"2. **Conversation Flow Tests:** Multi-turn conversation flows with clarification responses\n")
            f.write(f"3. **Intent Navigation Tests:** Intent-to-intent navigation through buttons and quick replies\n")
            
            if format_type == "hoot":
                f.write(f"\n## HOOT Format Details\n\n")
                f.write(f"- Uses 'DEPTH' testing phase for depth-based tests\n")
                f.write(f"- Includes multi-step validations for conversation flows\n")
                f.write(f"- Validates both text responses and interactive elements\n")
        
        logger.info(f"📄 Generated summary report: {report_file}")


def main():
    """Main function"""
    import sys
    
    # Parse command line arguments
    format_type = "standard"
    if len(sys.argv) > 1:
        if sys.argv[1] == "--hoot":
            format_type = "hoot"
        elif sys.argv[1] == "--capi":
            format_type = "standard"
    
    # Create consolidated generator
    generator = ConsolidatedTestGenerator()
    
    # Generate both formats
    logger.info("="*80)
    logger.info("🚀 CONSOLIDATED TEST GENERATION")
    logger.info("="*80)
    
    # Generate CAPI format
    logger.info("\n📋 Generating CAPI format tests...")
    capi_file, capi_stats = generator.generate_consolidated_test_suite("standard")
    
    # Generate HOOT format
    logger.info("\n📋 Generating HOOT format tests...")
    hoot_file, hoot_stats = generator.generate_consolidated_test_suite("hoot")
    
    # Final summary
    logger.info("\n" + "="*80)
    logger.info("✅ CONSOLIDATED TEST GENERATION COMPLETE")
    logger.info("="*80)
    logger.info(f"📄 CAPI Tests: {capi_file} ({capi_stats['total_tests']} tests)")
    logger.info(f"📄 HOOT Tests: {hoot_file} ({hoot_stats['total_tests']} tests)")
    logger.info(f"📊 Reports: test_generation_report_{generator.timestamp}.md")
    logger.info("="*80)


if __name__ == "__main__":
    main()