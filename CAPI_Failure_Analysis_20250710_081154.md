# CAPI Test Failure Analysis Report

**Generated**: 2025-07-10 08:11:54  
**Total Tests Executed**: 42  
**Total Failures**: 11  
**Success Rate**: 73.8%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 0 (0.0%) - High similarity but not exact match
- **Content Mismatch**: 0 (0.0%) - Moderate similarity, content differs
- **Failed Response**: 9 (21.4%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Failed Response Cases (9 items)
*These tests failed to extract a valid response from the API.*

#### 1. bt_tax_and_annual_statements
**Trigger**: "Tax and annual statements"  
**Error**: Turn 1 response mismatch - Expected: 'As part of BT’s simplification we have closed the super fund Retirement Wrap. This means BT Panorama...', Got: 'Annual and tax statements are generated automatically by BT. These are released after the end of eac...'
**Session ID**: node0gi6iw1mp9tmgokq1t7n66u7f1751752090091295672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 2. Actions_Menu
**Trigger**: "Where is the actions menu?"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'To better help you with your query could you log in into your account and please ask me again?'
**Session ID**: node01wbeq3cobtovgih91e0l6gbr41761752090091296672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 3. bt_term_deposit
**Trigger**: "term deposit"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'To better help you with your query, please sign in to your account, then ask again.'
**Session ID**: node01ooyq4i1od5nj1jnxt3ag26mda1771752090091297672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 4. bt_register
**Trigger**: "Can you help me register?"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'If your account was set up using your existing Westpac profile you can sign in using your Westpac Li...'
**Session ID**: node0zhaiyn78c54wyvuv5acuts751781752090091298672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 5. bt_view_closed_accounts
**Trigger**: "View closed accounts"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'You can access your account for 2 years after the account has been closed. If this period has passed...'
**Session ID**: node0rmc6lu4uw8wutnaadbhf8uko1791752090091299672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 6. bt_wrap_employer_cont
**Trigger**: "Will regular super contributions from employers continue as normal on Panorama?"  
**Error**: Turn 1 response mismatch - Expected: 'The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365
The USI/SPIN is 90 194 410...', Got: 'We are contacting clients who are still receiving contributions under the old USI. Clients need to g...'
**Session ID**: node01izjwa655skir1k4dd43qxt66t1801752090091300672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 7. bt_funds_not_received
**Trigger**: "Why cant i see my employer contributions?"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01o72rq2csutt21iw5hk67ddwur1811752090091301672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 8. bt_how_logout
**Trigger**: "How to logout?"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'To better help you with your query could you log in into your account and please ask me again?'
**Session ID**: node01e56kddcwy72ha90f7c4lg0v1821752090091302672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 9. bt_approval_notify
**Trigger**: "How is the client notified to approve application?"  
**Error**: Turn 1 response mismatch - Expected: 'Please select which applies to your log in difficulties.', Got: 'If your account was set up using your existing Westpac profile you can sign in using your Westpac Li...'
**Session ID**: node01uubhk9l27d8n7qp9scisg0001831752090091303672b3096-f11c-4e0a-a094-4109a3611fe4

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 0 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 9 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_tax_and_annual_statements`: INTENT_MISMATCH: 2, FAILED_RESPONSE: 1
- `Actions_Menu`: FAILED_RESPONSE: 1
- `bt_term_deposit`: FAILED_RESPONSE: 1
- `bt_register`: FAILED_RESPONSE: 1
- `bt_view_closed_accounts`: FAILED_RESPONSE: 1
- `bt_wrap_employer_cont`: FAILED_RESPONSE: 1
- `bt_funds_not_received`: FAILED_RESPONSE: 1
- `bt_how_logout`: FAILED_RESPONSE: 1
- `bt_approval_notify`: FAILED_RESPONSE: 1


### Success Patterns
**Consistently Passing Intents**: 31 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-07-10 08:11:54
**Analysis Scope**: All 42 test cases from segment `bt_account__advised_super`
