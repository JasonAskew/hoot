# CAPI Test Failure Analysis Report

**Generated**: 2025-07-10 09:14:16  
**Total Tests Executed**: 42  
**Total Failures**: 10  
**Success Rate**: 76.2%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 7 (16.7%) - High similarity but not exact match
- **Content Mismatch**: 0 (0.0%) - Moderate similarity, content differs
- **Failed Response**: 1 (2.4%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Partial Pass Cases (7 items)
*These tests had high similarity scores but didn't match exactly, usually due to formatting differences.*

#### 1. bt_tax_and_annual_statements (Similarity: 1.00)
**Trigger**: "Tax and annual statements"  
**Issue**: Significant content differences

**Expected**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days. To locate the Annual audit report, Select the act...
```

**Actual**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days. To locate the Annual audit report, Select the act...
```

---

#### 2. Actions_Menu (Similarity: 1.00)
**Trigger**: "Where is the actions menu?"  
**Issue**: Minor formatting differences (line breaks, spacing)

**Expected**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual**:
```
To better help you with your query could you log in into your account and please ask me again?
```

---

#### 3. bt_term_deposit (Similarity: 1.00)
**Trigger**: "term deposit"  
**Issue**: Significant content differences

**Expected**:
```
To better help you with your query, please sign in to your account, then ask again.
```

**Actual**:
```
To better help you with your query, please sign in to your account, then ask again.
```

---

#### 4. bt_register (Similarity: 1.00)
**Trigger**: "Can you help me register?"  
**Issue**: Significant content differences

**Expected**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 charac...
```

**Actual**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 charac...
```

---

#### 5. bt_view_closed_accounts (Similarity: 1.00)
**Trigger**: "View closed accounts"  
**Issue**: Minor formatting differences (line breaks, spacing)

**Expected**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

---

#### 6. bt_how_logout (Similarity: 1.00)
**Trigger**: "How to logout?"  
**Issue**: Minor formatting differences (line breaks, spacing)

**Expected**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual**:
```
To better help you with your query could you log in into your account and please ask me again?
```

---

#### 7. bt_approval_notify (Similarity: 1.00)
**Trigger**: "How is the client notified to approve application?"  
**Issue**: Significant content differences

**Expected**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 charac...
```

**Actual**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 charac...
```

---

### Failed Response Cases (1 items)
*These tests failed to extract a valid response from the API.*

#### 1. bt_funds_not_received
**Trigger**: "Why cant i see my employer contributions?"  
**Error**: Turn 1 response mismatch - Expected: 'To better help you with your query could you log in into your account and please ask me again?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node01tquu35loza9lpxpvy1efghm82711752090091391672b3096-f11c-4e0a-a094-4109a3611fe4

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 7 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 1 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_tax_and_annual_statements`: INTENT_MISMATCH: 2, PARTIAL_PASS: 1
- `Actions_Menu`: PARTIAL_PASS: 1
- `bt_term_deposit`: PARTIAL_PASS: 1
- `bt_register`: PARTIAL_PASS: 1
- `bt_view_closed_accounts`: PARTIAL_PASS: 1
- `bt_funds_not_received`: FAILED_RESPONSE: 1
- `bt_how_logout`: PARTIAL_PASS: 1
- `bt_approval_notify`: PARTIAL_PASS: 1


### Success Patterns
**Consistently Passing Intents**: 32 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-07-10 09:14:16
**Analysis Scope**: All 42 test cases from segment `bt_account__advised_super`
