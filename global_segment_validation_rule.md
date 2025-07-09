# Global Segment Validation Rule

## Overview

The global segment acts as a master switch for intents. If an intent is disabled for the `global` segment, it is effectively switched off system-wide and cannot be tested for ANY segment.

## Implementation Details

### 1. Priority Check
The global segment check is performed FIRST before any other validation:

```python
def is_intent_enabled_for_segment(self, intent_name: str, segment_name: str) -> bool:
    # CRITICAL: First check if intent is disabled globally
    if intent_name in self.disabled_intents:
        disabled_segments = self.disabled_intents[intent_name]
        if 'global' in disabled_segments:
            # Intent is globally disabled - cannot be tested for ANY segment
            return False
```

### 2. Test Generation Impact
When an intent is globally disabled:
- No tests are generated for that intent across ALL segments
- Response text: "Intent disabled globally"
- Response type: "Globally Disabled"
- Invalid reason: "Intent disabled globally - switched off system-wide"

### 3. Example Scenario

#### Global Segment Definition
```json
// segments/global.json
{
  "categorization": {
    "tags": []
  },
  "state": "SAVED",
  "name": "global",
  "disabled_actions": [
    "bt_deposit_funds",
    "bt_deposit_funds_investor",
    "bt_asset_transfer",
    "bt_asset_transfer_investor",
    "bt_request_for_withdrawal",
    "bt_request_for_withdrawal_investor",
    "91_Capabilities_S_P",
    "bt_available_balance"
  ]
}
```

#### Result
- Intents in disabled_actions: bt_deposit_funds, bt_asset_transfer, bt_request_for_withdrawal, etc.
- ALL segments: bt_account_advised_investment, bt_channel_mobile_investor, bt_channel_public, bt_user_adviser, etc.
- Status: INVALID - Intent disabled globally
- No tests generated for ANY segment

For example:
- bt_request_for_withdrawal is in global disabled_actions
- Therefore, ALL bt_request_for_withdrawal tests are invalid, regardless of segment
- This explains why all 10 bt_request_for_withdrawal tests failed with "For now, I can't help with that"

### 4. Validation Flow

```
1. Check global segment disabled status
   ├─ If disabled globally → Return False immediately
   └─ If not disabled globally → Continue with other checks
       ├─ Check segment-specific disabled status
       ├─ Check segment compatibility rules
       └─ Check other validation criteria
```

### 5. Impact on Test Results

#### Without Global Check
```csv
intent,segment,status,reason
bt_experimental_feature,bt_account_advised_investment,INVALID,Intent disabled
bt_experimental_feature,bt_channel_mobile_investor,INVALID,Intent disabled
bt_experimental_feature,bt_channel_public,INVALID,Intent disabled
bt_experimental_feature,bt_user_adviser,INVALID,Intent disabled
```

#### With Global Check
```csv
intent,segment,status,reason
bt_experimental_feature,ALL,INVALID,Intent disabled globally - switched off system-wide
```

### 6. Benefits

1. **Efficiency**: Prevents generating tests for intents that won't work anywhere
2. **Clarity**: Makes it clear when an intent is completely disabled vs partially disabled
3. **Accuracy**: Reflects actual bot behavior where global segment takes precedence
4. **Maintenance**: Easier to identify which intents are completely switched off

### 7. How to Enable a Globally Disabled Intent

To re-enable an intent that's globally disabled:
1. Remove the IntentMessageDisabled file for that intent, OR
2. Remove the "global" segment from the segment_responses array
3. Regenerate test suites
4. The intent will now be tested based on segment-specific rules

### 8. Detection in Code

The validator provides specific feedback for globally disabled intents:

```python
result = validator.validate_test_case("bt_experimental_feature", "bt_channel_public")
# Returns:
{
    'valid': False,
    'intent': 'bt_experimental_feature',
    'segment': 'bt_channel_public',
    'expected_behavior': 'globally_disabled',
    'reason': 'intent_disabled_globally',
    'message': 'Intent bt_experimental_feature is disabled for the global segment - effectively switched off system-wide'
}
```

## Testing the Rule

To verify the global segment rule is working:

1. Create an IntentMessageDisabled file with global segment
2. Run test generation
3. Verify no tests are generated for that intent
4. Check invalid_tests.csv for "Intent disabled globally" reason
5. Remove global segment from disabled file
6. Regenerate and verify tests are now created