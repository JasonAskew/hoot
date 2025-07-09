# CAPI Test Failure Analysis Report

**Generated**: 2025-07-10 08:39:48  
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

#### 1. bt_platforms_sft (Similarity: 1.00)
**Trigger**: "Tax and annual statements"  
**Issue**: Significant content differences

**Expected**:
```
As part of BT’s simplification we have closed the super fund Retirement Wrap. This means BT Panorama Super accounts have been transferred to another super fund called Asgard Independence Plan Division Two (Division Two fund), as part of a Successor Fund Transfer (SFT). For more information select 'G...
```

**Actual**:
```
As part of BT’s simplification we have closed the super fund Retirement Wrap. This means BT Panorama Super accounts have been transferred to another super fund called Asgard Independence Plan Division Two (Division Two fund), as part of a Successor Fund Transfer (SFT). For more information select 'G...
```

---

#### 2. bt_login_failure (Similarity: 1.00)
**Trigger**: "Where is the actions menu?"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

#### 3. bt_login_failure (Similarity: 1.00)
**Trigger**: "term deposit"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

#### 4. bt_login_failure (Similarity: 1.00)
**Trigger**: "Can you help me register?"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

#### 5. bt_login_failure (Similarity: 1.00)
**Trigger**: "View closed accounts"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

#### 6. bt_login_failure (Similarity: 1.00)
**Trigger**: "How to logout?"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

#### 7. bt_login_failure (Similarity: 1.00)
**Trigger**: "How is the client notified to approve application?"  
**Issue**: Significant content differences

**Expected**:
```
Please select which applies to your log in difficulties.
```

**Actual**:
```
Please select which applies to your log in difficulties.
```

---

### Failed Response Cases (1 items)
*These tests failed to extract a valid response from the API.*

#### 1. bt_funds_not_received
**Trigger**: "Why cant i see my employer contributions?"  
**Error**: Turn 1 response mismatch - Expected: 'To better help you with your query could you log in into your account and please ask me again?', Got: 'For now, I can't help with that. But I'm always learning.'
**Session ID**: node0158tivka9smpe1g87irzqzxrx72261752090091346672b3096-f11c-4e0a-a094-4109a3611fe4

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 7 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 1 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_login_failure`: PARTIAL_PASS: 6
- `bt_tax_and_annual_statements`: INTENT_MISMATCH: 2
- `bt_platforms_sft`: PARTIAL_PASS: 1
- `bt_funds_not_received`: FAILED_RESPONSE: 1


### Success Patterns
**Consistently Passing Intents**: 32 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-07-10 08:39:48
**Analysis Scope**: All 42 test cases from segment `bt_account__advised_super`
