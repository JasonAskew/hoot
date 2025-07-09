# CAPI Test Failure Analysis Report

**Generated**: 2025-07-10 07:04:58  
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
**Error**: Response mismatch - Expected: 'What proportion do you want to withdraw?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0xx4a2adrmibwtt0733a5a355121752090091132672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 2. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Response mismatch - Expected: 'What proportion do you want to withdraw?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node02v92u9t7qlmv14bfviam1j2g4191752090091139672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 3. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Response mismatch - Expected: 'What proportion do you want to withdraw?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0bkwbplubatjv1x6wi3wonnc9s281752090091148672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 4. bt_request_for_withdrawal
**Trigger**: "Am I able to make a payment over $200,000"  
**Error**: Response mismatch - Expected: 'What proportion do you want to withdraw?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01ue2caxy1uwcx3zcm8r8mgo8x391752090091159672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 5. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'One of our consultants will be able to assist you with this query. If you would like assistance, ple...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0ybe2ngr5fki1i4uuczhob6t3421752090091162672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 6. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'One of our consultants will be able to assist you with this query. If you would like assistance, ple...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0lk6cmkfnli8nd8p3udj2loa0431752090091163672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 7. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'One of our consultants will be able to assist you with this query. If you would like assistance, ple...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01av2dqdv6ips41wm57y4qz9yn0441752090091164672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 8. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' sectio...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01ss7nmvpmxtuu5wubcgb2z1ff451752090091165672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 9. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' sectio...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0yng8mxzxnijt796wt4hbmzwl461752090091166672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 10. bt_request_for_withdrawal
**Trigger**: "How do I make a withdrawal"  
**Error**: Turn 2 response mismatch - Expected: 'To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' sectio...', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01hy1td9ln04n81ax7syc5t45v2471752090091167672b3096-f11c-4e0a-a094-4109a3611fe4

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

**Report Generated**: 2025-07-10 07:04:58
**Analysis Scope**: All 53 test cases from segment `bt_account__advised_super`
