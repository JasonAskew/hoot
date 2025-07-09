# CAPI Test Failure Analysis Report

**Generated**: 2025-07-09 16:57:22  
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
**Session ID**: node012181l3u6yi1x16sgdclju4yip84731752015118733ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 2. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node01q99ocd0y1v08f0wlikiza75m84801752015118740ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 3. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node09cmrqoban9e1mtjhg25xnkyw84891752015118749ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 4. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Unknown error
**Session ID**: node01f19xhj3fqkkcw3gab6txtbou85001752015118760ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 5. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0x4f0ga09abuk1gferjj4ryg1x85031752015118763ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 6. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node018fhr9c119hzh97pkty13t7bd85041752015118764ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 7. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node013mf8av5wqyagotezl6t3cgux85051752015118765ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 8. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node01u1x4m3komjmp7n4ijpla2nhs85061752015118766ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 9. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node01bfuu26au7ez01sigqh3f2nk1785071752015118767ee2e84d1-25bc-40a6-9e61-553b30701878

---

#### 10. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Unknown error
**Session ID**: node0188ilwjmrdq7e1aajls89jmri185081752015118768ee2e84d1-25bc-40a6-9e61-553b30701878

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

**Report Generated**: 2025-07-09 16:57:22
**Analysis Scope**: All 53 test cases from segment `bt_account__advised_super`
