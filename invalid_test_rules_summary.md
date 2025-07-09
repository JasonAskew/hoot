# Summary: Rules for Identifying Invalid Tests

## Quick Reference

Tests are marked as **INVALID** when any of these conditions are met:

### 0. Global Segment Rule (HIGHEST PRIORITY)
- Intent has "global" in its disabled segments list
- This means the intent is switched off system-wide
- NO tests will be generated for ANY segment

### 1. Response Content Issues
- Response text is "N/A"
- Response text is "Intent disabled for this segment"
- Response text is "Intent is inactive"
- Response text is "No intent data file"
- No response name can be resolved for the intent

### 2. Missing Data
- No example triggers available (missing intent_data files)
- No valid trigger_sentence in intent data
- Intent definition missing or corrupted
- Response definition missing

### 3. Disabled/Inactive Status
- Intent marked as `active: false` in intent JSON
- Segment marked as `active: false` in profile JSON
- Intent in segment's `disabled_actions` list
- Intent has a corresponding `IntentMessageDisabled*.json` file

### 4. Segment-Intent Incompatibility

#### Pension Accounts
- `deposit_funds` intents are invalid for pension segments

#### Public/Unauthenticated Channels
Invalid intents for "public" or "bt_account_super" segments:
- deposit_funds
- withdrawal
- balance
- transactions
- account_details
- personal_tax
- statements

#### Investment vs Super Restrictions
Super-only intents invalid for investment accounts:
- rollover
- pension
- super_early
- centrelink
- minimum_pension
- pension_payment

### 5. Conversation Flow Specific Rules
- No valid segments exist for the intent
- Clarification response missing
- No quick replies in clarification response
- Quick reply options have no matching rules
- Expected response for quick reply not found

### 6. Intent Navigation Specific Rules
- Source or target intent matches excluded patterns:
  - feedback
  - survey
  - thumbs
  - rating
  - csat
  - nps
  - binary
- Navigation payload is not INTENT type
- Target intent not found in system

### 7. Test Filtering Rules
- Segment not in `top_segments.txt` (when filtering)
- Intent not in `top_intents.txt` (when filtering)
- Duplicate test (same key already processed)

## How Invalid Tests Are Handled

1. **During Generation**: Tests failing validation are not written to the main test file
2. **Invalid Test Tracking**: Failed tests are written to `*_invalid_tests.csv` with reasons
3. **During Execution**: Tests marked invalid are skipped
4. **In Reports**: Invalid tests are tracked separately with failure reasons

## Key Implementation Files

- `segment_intent_validator.py` - Core validation logic
- `generate_matrix_with_segment_matching.py` - Matrix test validation
- `conversation_flow_test_generator.py` - Conversation flow validation
- `intent_navigation_test_generator.py` - Navigation test validation
- `filter_tests_subset.py` - Test filtering rules