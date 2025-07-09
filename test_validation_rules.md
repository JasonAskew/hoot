# Test Validation Rules Documentation

This document describes all the rules implemented to identify and filter invalid tests in the HOOT test generation framework.

## Overview

The test validation system uses multiple layers of rules to ensure only valid test cases are generated and executed. These rules prevent tests from being created for:
- Disabled intents
- Incompatible segment-intent combinations  
- Missing or incomplete test data
- Inactive segments or intents

## 1. Global Segment Rule (HIGHEST PRIORITY)

### Global Segment Master Switch
- **Rule**: If an intent is disabled for the `global` segment, it cannot be tested for ANY segment
- **Priority**: This check happens FIRST, before any other validation
- **Reason**: The global segment matches on every request, so disabling an intent globally effectively switches it off system-wide
- **Implementation**: Checks if 'global' is in the disabled_segments list for an intent
- **Result**: Test marked as "Intent disabled globally - switched off system-wide"

## 2. Segment-Intent Compatibility Rules (segment_intent_validator.py)

### Pension Account Restrictions
- **Rule**: Intents containing "deposit_funds" are disabled for pension accounts
- **Reason**: Deposits are not allowed into pension accounts
- **Implementation**: Checks if "pension" is in segment name and "deposit_funds" is in intent name

### Public/Unauthenticated Channel Restrictions
- **Rule**: Secure functions are disabled for public and unauthenticated segments
- **Applies to segments containing**: "public" or "bt_account_super"
- **Restricted intents include**:
  - deposit_funds
  - withdrawal
  - balance
  - transactions
  - account_details
  - personal_tax
  - statements
- **Reason**: These functions require authenticated user access

### Investment vs Super Account Restrictions
- **Rule**: Super-specific intents are disabled for investment accounts
- **Super-only intents include**:
  - rollover
  - pension
  - super_early
  - centrelink
  - minimum_pension
  - pension_payment
- **Reason**: These features only apply to superannuation accounts

### Explicitly Disabled Intents
- **Rule**: Intents with disabled response files are marked invalid
- **Detection**: Looks for IntentMessageDisabled*.json files
- **Example**: IntentMessageDisabledbtdepositfunds.json disables bt_deposit_funds for specific segments

## 2. Test Generation Validation Rules (generate_matrix_with_segment_matching.py)

### Valid Test Criteria
A test is considered valid only if ALL of the following conditions are met:

1. **Valid Response Content**
   - Response text is NOT "N/A"
   - Response text is NOT "Intent disabled for this segment"
   - Response text is NOT "Intent is inactive"  
   - Response text is NOT "No intent data file"

2. **Active Segment**
   - segment.active must be True
   - Segments can be marked inactive in their profile JSON

3. **Enabled Intent for Segment**
   - Intent must not be in segment's disabled_actions list
   - Checked via is_enabled flag

4. **Active Intent**
   - intent.active must be True
   - Intents can be marked inactive in their JSON definition

5. **Valid Intent Data**
   - Intent must have example triggers available
   - Checks for intent_data files (train/test/seed)
   - At least one valid trigger_sentence must exist

### Invalid Test Tracking
When a test fails validation, the reason is tracked:
- "No response defined" - No valid response found
- "Intent disabled" - Intent explicitly disabled for segment
- "Intent is inactive" - Intent marked as inactive
- "No intent data file" - Missing training data
- "Segment inactive" - Segment marked as inactive
- "Intent not enabled for segment" - Failed compatibility check
- "No valid intent data (example triggers)" - No triggers found

## 3. Conversation Flow Validation (conversation_flow_test_generator.py)

### Valid Segments Check
- Uses SegmentIntentValidator to get valid segments for an intent
- Skips test generation if no valid segments found
- Logs warning: "No valid segments found for {intent_name}, skipping test generation"

### Clarification Response Validation
- Verifies clarification response exists in responses
- Checks for quick_replies in clarification response
- Validates matching rules exist for quick reply options

### Rule Matching Validation
- Ensures each quick reply option has a corresponding rule
- Logs warning if no matching rule found for slot value
- Skips test case if expected response not found

## 4. Test Filtering Rules (filter_tests_subset.py)

### Segment Filtering
- Only includes tests where segment is in top_segments.txt
- Applied to all test types (matrix, conversation_flow, intent_navigation)

### Intent Filtering
For different test types:

**Matrix and Conversation Flow Tests**:
- Intent must be in top_intents.txt

**Intent Navigation Tests**:
- Either source_intent OR target_intent must be in top_intents.txt
- Allows navigation tests that connect to/from important intents

### Deduplication
- Creates unique test keys to prevent duplicates
- Key format varies by test type:
  - Matrix/Conversation: `{test_source}_{intent}_{segment}_{test_type}_{turn_2_input}`
  - Navigation: `nav_{source_intent}_{target_intent}_{segment}`

## 5. Response Resolution Rules

### Segment-Specific Response Priority
1. Check for segment-specific response variant
2. Fall back to default response if no segment variant exists
3. Mark as "N/A" if no response found

### Response Type Classification
- "Segment-specific ({segment_name})" - Using segment variant
- "Default" - Using default response
- "Disabled" - Intent disabled for segment
- "Inactive" - Intent marked inactive
- "No Intent Data" - Missing training data

## 6. Special Cases and Edge Rules

### Default Segment Mapping
- "default" segment maps to ["bt_account_super", "global"]
- Used for basic/unauthenticated access patterns

### Mobile Channel Considerations
- bt_channel_mobile_investor has specific response variants
- Some features have limited mobile functionality

### Adviser Portal Rules
- bt_user_adviser segment has enhanced permissions
- Can access client-management features
- Different response content for adviser context

## Usage in Test Pipeline

1. **Generation Phase**: Apply all validation rules to prevent invalid test creation
2. **Filtering Phase**: Further reduce tests based on specific criteria
3. **Execution Phase**: Skip tests marked as invalid or expected failures
4. **Reporting Phase**: Track invalid test reasons for analysis

## Maintenance Notes

- Validation rules should be updated when new segment types are added
- Intent compatibility rules may need adjustment for new features
- Disabled intent files should be kept in sync with platform configuration
- Test data files must be maintained for all active intents