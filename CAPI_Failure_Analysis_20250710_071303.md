# CAPI Test Failure Analysis Report

**Generated**: 2025-07-10 07:13:03  
**Total Tests Executed**: 42  
**Total Failures**: 11  
**Success Rate**: 73.8%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 0 (0.0%) - High similarity but not exact match
- **Content Mismatch**: 0 (0.0%) - Moderate similarity, content differs
- **Failed Response**: 8 (19.0%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Failed Response Cases (8 items)
*These tests failed to extract a valid response from the API.*

#### 1. bt_tax_and_annual_statements
**Trigger**: "Tax and annual statements"  
**Error**: Response mismatch - Expected: 'bt_tax_and_annual_statements', Got: 'Annual and tax statements are generated automatically by BT. These are released after the end of eac...'
**Session ID**: node01ma7ad4fryt50mr41hp6tup6l901752090091210672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 2. Actions_Menu
**Trigger**: "Where is the actions menu?"  
**Error**: Response mismatch - Expected: 'Actions_Menu', Got: 'To better help you with your query could you log in into your account and please ask me again?'
**Session ID**: node0elwetck3ojv31c1zwhm61j929911752090091211672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 3. bt_term_deposit
**Trigger**: "term deposit"  
**Error**: Response mismatch - Expected: 'bt_term_deposit', Got: 'To better help you with your query, please sign in to your account, then ask again.'
**Session ID**: node01w2kpc75w4adw8tbhveyav43y921752090091212672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 4. bt_register
**Trigger**: "Can you help me register?"  
**Error**: Response mismatch - Expected: 'bt_register_response', Got: 'If your account was set up using your existing Westpac profile you can sign in using your Westpac Li...'
**Session ID**: node0aj46wo1s165v4zr3hihes2ql931752090091213672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 5. bt_view_closed_accounts
**Trigger**: "View closed accounts"  
**Error**: Response mismatch - Expected: 'bt_view_closed_accounts', Got: 'You can access your account for 2 years after the account has been closed. If this period has passed...'
**Session ID**: node0u2fhdjlkpvim10quz7wd7qy0c941752090091214672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 6. bt_wrap_employer_cont
**Trigger**: "Will regular super contributions from employers continue as normal on Panorama?"  
**Error**: Response mismatch - Expected: 'bt_wrap_employer_cont_response', Got: 'We are contacting clients who are still receiving contributions under the old USI. Clients need to g...'
**Session ID**: node0ess6v79mszk88rrh5bh3lw47951752090091215672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 7. bt_how_logout
**Trigger**: "How to logout?"  
**Error**: Response mismatch - Expected: 'bt_how_logout', Got: 'To better help you with your query could you log in into your account and please ask me again?'
**Session ID**: node0jel0hpba3f5xltci88dtrmsu971752090091217672b3096-f11c-4e0a-a094-4109a3611fe4

---

#### 8. bt_approval_notify
**Trigger**: "How is the client notified to approve application?"  
**Error**: Response mismatch - Expected: 'bt_approval_notify_response', Got: 'If your account was set up using your existing Westpac profile you can sign in using your Westpac Li...'
**Session ID**: node0s2joqp1d7mtrm084pg0kyv82981752090091218672b3096-f11c-4e0a-a094-4109a3611fe4

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 0 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 8 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_tax_and_annual_statements`: INTENT_MISMATCH: 2, FAILED_RESPONSE: 1
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

**Report Generated**: 2025-07-10 07:13:03
**Analysis Scope**: All 42 test cases from segment `bt_account__advised_super`
