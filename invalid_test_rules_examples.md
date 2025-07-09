# Invalid Test Rules - Specific Examples

## 0. Global Segment Rule (HIGHEST PRIORITY)

### Example: Intent Disabled Globally
```
File: responses/IntentMessageDisabledbtexperimentalfeature.json
Content:
{
  "segment_responses": [
    {
      "segment_name": "global",
      "response": {...}
    }
  ]
}

Intent: bt_experimental_feature
Test segments attempted: bt_account_advised_investment, bt_channel_mobile_investor, etc.
Check: 'global' in disabled_segments
Result: ALL tests for bt_experimental_feature marked INVALID
Reason: "Intent disabled globally - switched off system-wide"
Impact: Zero tests generated for this intent across all segments
```

## 1. Response Content Issues

### Example: "N/A" Response
```
Intent: bt_some_new_feature
Segment: bt_account_advised_investment
Issue: No response file exists for bt_some_new_feature_response
Result: response_text = "N/A"
Test Status: INVALID - excluded from test generation
```

### Example: "Intent disabled for this segment"
```
Intent: bt_deposit_funds
Segment: bt_account_pension
Issue: Intent explicitly disabled due to pension restrictions
Result: response_text = "Intent disabled for this segment"
Test Status: INVALID - marked with reason "Intent disabled"
```

### Example: "Intent is inactive"
```
Intent: bt_old_feature (with active: false in intent JSON)
Segment: bt_channel_public
Issue: Intent marked as inactive in bt_old_feature.json
Result: response_text = "Intent is inactive"
Test Status: INVALID - marked with reason "Intent is inactive"
```

### Example: "No intent data file"
```
Intent: bt_experimental_feature
Segment: bt_user_adviser
Issue: No bt_experimental_feature_train.json, _test.json, or _seed.json exists
Result: response_text = "No intent data file", example_trigger = "N/A"
Test Status: INVALID - marked with reason "No intent data file"
```

## 2. Missing Data

### Example: No Example Triggers
```
Intent: bt_balance
File checked: intent_data/bt_balance_train.json
Content: {"data": []} (empty array)
Result: get_example_trigger() returns None
Test Status: INVALID - no trigger sentence to test with
```

### Example: Corrupted Intent Definition
```
Intent: bt_transfer_funds
File: intents/bt_transfer_funds.json
Content: {"name": "bt_transfer_funds"} (missing webhook_params)
Result: get_intent_response_name() returns None
Test Status: INVALID - cannot determine response
```

## 3. Disabled/Inactive Status

### Example: Intent Marked Inactive
```json
// intents/bt_legacy_feature.json
{
  "name": "bt_legacy_feature",
  "active": false,
  "webhook_params": {...}
}
Result: is_intent_active = False
Test Status: INVALID - "Intent marked as inactive"
```

### Example: Segment Marked Inactive
```json
// profiles/bt_test_segment.json
{
  "name": "bt_test_segment",
  "active": false,
  "meta_fields": [...]
}
Result: segment.get('active', True) = False
Test Status: INVALID - "Segment inactive"
```

### Example: Intent in Disabled Actions
```json
// profiles/bt_channel_mobile_investor.json
{
  "disabled_actions": ["bt_complex_feature", "bt_admin_function"],
  "meta_fields": [...]
}
Intent: bt_complex_feature
Result: is_enabled = False (intent in disabled_actions)
Test Status: INVALID - "Intent not enabled for segment"
```

### Example: Explicit Disabled File
```
File: responses/IntentMessageDisabledbtdepositfunds.json
Segment responses: [{"segment_name": "bt_account_pension"}]
Intent: bt_deposit_funds
Segment: bt_account_pension
Result: Explicitly disabled via IntentMessageDisabled file
Test Status: INVALID - "explicitly_disabled"
```

## 4. Segment-Intent Incompatibility

### Example: Pension Account Restriction
```python
Intent: bt_deposit_funds
Segment: bt_account_advised_pension
Check: if "pension" in segment_name and "deposit_funds" in intent_name
Result: _check_segment_compatibility() returns False
Test Status: INVALID - deposits not allowed for pension accounts
```

### Example: Public Channel Restriction
```python
Intent: bt_balance
Segment: bt_channel_public
Check: "public" in segment_name and "balance" in restricted_intents
Result: _check_segment_compatibility() returns False
Test Status: INVALID - balance requires authentication
```

### Example: Investment vs Super Restriction
```python
Intent: bt_minimum_pension_changes
Segment: bt_account_advised_investment
Check: "investment" in segment_name and "minimum_pension" in super_only_intents
Result: _check_segment_compatibility() returns False
Test Status: INVALID - pension features not applicable to investment accounts
```

## 5. Conversation Flow Specific Rules

### Example: No Valid Segments
```python
Intent: bt_internal_admin_tool
Valid segments check: validator.get_valid_segments_for_intent("bt_internal_admin_tool")
Result: [] (empty list)
Warning: "No valid segments found for bt_internal_admin_tool, skipping test generation"
Test Status: NOT GENERATED
```

### Example: Missing Clarification Response
```python
Intent: bt_request_for_withdrawal
Expected clarification: bt_request_for_withdrawal_clarify_withdraw_amount_type
File check: responses/bt_request_for_withdrawal_clarify_withdraw_amount_type.json
Result: File not found
Test Status: INVALID - cannot generate conversation flow
```

### Example: No Matching Rule for Quick Reply
```python
Intent: bt_request_for_withdrawal
Quick reply option: "partial withdrawal"
Slot: withdraw_amount_type
Rules check: No rule where slot="withdraw_amount_type" and value="partial withdrawal"
Warning: "No matching rule found for withdraw_amount_type=partial withdrawal"
Test Status: INVALID - incomplete conversation flow
```

## 6. Intent Navigation Specific Rules

### Example: Excluded Pattern Match
```python
Source intent: 69_LiveAgent_S
Quick reply payload: "kcb_feedback_binary"
Check: "feedback" matches excluded pattern r'feedback'
Result: should_exclude_intent("kcb_feedback_binary") returns True
Test Status: NOT GENERATED - feedback intents excluded
```

### Example: Non-Intent Navigation
```python
Response: bt_find_forms_response
Quick reply: {"type": "URL", "payload": "https://forms.bt.com", "label": "Forms"}
Check: qr.get('type') != 'INTENT'
Result: Not an intent navigation
Test Status: NOT GENERATED - URL navigation, not intent
```

### Example: Missing Target Intent
```python
Source intent: bt_balance
Quick reply: {"type": "INTENT", "payload": "bt_old_removed_intent"}
Target check: "bt_old_removed_intent" not in self.intents
Warning: "Target intent bt_old_removed_intent not found"
Test Status: INVALID - target intent doesn't exist
```

## 7. Test Filtering Rules

### Example: Segment Not in Filter List
```
Test: bt_balance for segment bt_internal_testing
Filter file: top_segments.txt contains:
- bt_account_advised_investment
- bt_channel_mobile_investor
- bt_channel_public
- bt_user_adviser
Check: "bt_internal_testing" not in top_segments
Result: Test excluded from targeted subset
```

### Example: Intent Not in Filter List
```
Test: bt_rarely_used_feature for segment bt_channel_public
Filter file: top_intents.txt contains:
- bt_balance
- bt_deposit_funds
- bt_request_for_withdrawal
Check: "bt_rarely_used_feature" not in top_intents
Result: Test excluded from targeted subset
```

### Example: Duplicate Test Detection
```
Test 1: Key = "conversation_flow_bt_request_for_withdrawal_bt_user_adviser_conversation_flow_partial withdrawal"
Test 2: Same key (duplicate entry in source data)
Check: test_key already in seen_tests set
Result: Second test skipped as duplicate
```

## Real-World Impact

### bt_request_for_withdrawal Failures
```
All 10 tests failed with:
Expected: "What proportion do you want to withdraw?"
Actual: "For now, I can't help with that. But I'm always learning."
Reason: Intent appears to be disabled/unimplemented in bot platform
Impact: 18.9% of test suite failing
```

### #NAME? Intent Mismatch
```
Trigger: "#NAME?"
Expected intent: bt_tax_and_annual_statements
Actual intent: bt_change_name
Reason: NLU incorrectly mapping Excel error text to name change intent
Impact: 3 test failures
```