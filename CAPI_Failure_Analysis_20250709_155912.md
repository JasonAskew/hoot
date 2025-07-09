# CAPI Test Failure Analysis Report

**Generated**: 2025-07-09 15:59:12  
**Total Tests Executed**: 53  
**Total Failures**: 22  
**Success Rate**: 58.5%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 0 (0.0%) - High similarity but not exact match
- **Content Mismatch**: 0 (0.0%) - Moderate similarity, content differs
- **Failed Response**: 18 (34.0%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Failed Response Cases (18 items)
*These tests failed to extract a valid response from the API.*

#### 1. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node01iv2d4fz9sygqb6njwx8h75f383961752015118656ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 2. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node017f4inkco0nc8boi4yrzhfmn484031752015118663ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 3. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node013c4dlo7ge3ttpud85z2z9kyq84221752015118682ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 4. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node0qrgsp5vb9ral1mgm840s9e0df84331752015118693ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 5. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0gtxj6acbswvd1rd5r5fu2x4ie84361752015118696ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 6. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0z99bh24fcku12w25on08eb3h84371752015118697ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 7. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0c81d81378utuxl8aqbwukmm484381752015118698ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 8. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0kycatkjdompj1vypmj5k0a1yn84391752015118699ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 9. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node01gv7qivffzhm49s1g1kowbz0s84401752015118700ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 10. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node01k8nwxobqn4d5ynbbznex4bie84411752015118701ee2e84d1-25bc-40a6-9e61-553b30701878

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 0 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 18 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_request_for_withdrawal`: FAILED_RESPONSE: 10
- `bt_tax_and_annual_statements`: INTENT_MISMATCH: 3, FAILED_RESPONSE: 1
- `Actions_Menu`: FAILED_RESPONSE: 1
- `bt_term_deposit`: FAILED_RESPONSE: 1
- `bt_register`: FAILED_RESPONSE: 1
- `bt_view_closed_accounts`: FAILED_RESPONSE: 1
- `bt_wrap_employer_cont`: FAILED_RESPONSE: 1
- `bt_funds_not_received`: INTENT_MISMATCH: 1
- `bt_how_logout`: FAILED_RESPONSE: 1
- `bt_approval_notify`: FAILED_RESPONSE: 1


### Success Patterns
**Consistently Passing Intents**: 31 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-07-09 15:59:12
**Analysis Scope**: All 53 test cases from segment `bt_account__advised_super`
