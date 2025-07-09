# bt_request_for_withdrawal Test Failure Analysis

## Issue Summary
All bt_request_for_withdrawal tests are failing with the response: "For now, I can't help with that. But I'm always learning."

## Root Cause Analysis

### 1. Test Execution Flow
- Tests are correctly sending triggers like "Am I able to make a payment over $200,000" and "How do I make a withdrawal"
- The intent is being correctly recognized (bt_request_for_withdrawal appears in actual_intent field)
- However, instead of the expected clarification response, the bot returns a fallback message

### 2. Expected vs Actual Behavior
**Expected:**
- Response: "What proportion do you want to withdraw?"
- Quick Replies: ["Partial withdrawal", "Full withdrawal"]

**Actual:**
- Response: "For now, I can't help with that. But I'm always learning."
- No quick replies

### 3. Response Source
The fallback response comes from one of these files:
- `MessageUnImplementedIntent.json`
- `IntentMessageDisabled.json`
- `Message-Un-Implemented-Intent.json`

### 4. Configuration Analysis
The intent configuration appears correct:
- Intent file: Properly configured as ClarificationIntent
- Clarification response: bt_request_for_withdrawal_clarify_withdraw_amount_type exists with correct content
- Rules: Properly configured for "partial withdrawal" and "full withdrawal" routing

## Likely Causes

### 1. Intent Implementation Status
The fallback response suggests the intent may be:
- Not fully implemented in the bot platform
- Disabled for certain segments
- In a development/testing state

### 2. Segment-Specific Configuration
The tests are running with these segments:
- bt_account_advised_investment
- bt_channel_mobile_investor
- bt_channel_public
- bt_user_adviser

The intent might not be enabled for these specific segments in the bot configuration.

### 3. API/Platform Issue
Since the intent is recognized but returns a generic fallback, this appears to be a platform-level configuration issue rather than a test framework issue.

## Recommendations

### 1. Immediate Actions
- Contact the bot development team to verify if bt_request_for_withdrawal is fully implemented
- Check if the intent is enabled for all test segments
- Verify if there are any feature flags or configuration settings blocking this intent

### 2. Test Framework Improvements
The test framework is working correctly:
- It properly detects the mismatch between expected and actual responses
- The error reporting accurately shows "FAILED_RESPONSE" status
- The "Unknown error" in reports should be updated to show more specific error information

### 3. Code Fix for Better Error Reporting
Update `capi_test_runner.py` to provide more descriptive error messages when status is FAILED_RESPONSE:

```python
# Around line 917 in run_test_case method
else:
    status = 'FAILED_RESPONSE'  # Poor match
    error_message = f"Response mismatch - Expected: '{expected_content['text'][:50]}...', Got: '{actual_content['text'][:50]}...'"

# Then include the error_message in the result dictionary
```

## Test Results Summary
- 10 bt_request_for_withdrawal tests failed (all with same issue)
- Failure rate: 100% for this intent
- Impact: 18.9% of total test suite (10 out of 53 tests)

## Next Steps
1. Verify with the bot team if bt_request_for_withdrawal is production-ready
2. Check segment enablement for this intent
3. If the intent is disabled, either:
   - Enable it for testing
   - Mark these tests as expected failures
   - Remove them from the test suite until the feature is ready