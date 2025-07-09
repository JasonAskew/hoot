# CAPI Test Failure Analysis Report

**Generated**: 2025-06-23 11:39:21  
**Total Tests Executed**: 2336  
**Total Failures**: 79  
**Success Rate**: 96.6%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 0 (0.0%) - High similarity but not exact match
- **Content Mismatch**: 7 (0.3%) - Moderate similarity, content differs
- **Failed Response**: 50 (2.1%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Content Mismatch Cases (7 items)
*These tests had moderate similarity but significant content differences.*

#### 1. 47_TxnHistoryLength_S (Similarity: 0.67)
**Trigger**: "Tell me how long you keep transaction history."  
**Issue**: Significant content differences

**Expected**:
```
To view transaction history, select a client's account and then select 'Transactions'. To view transactions older than 3 years, sign in to the full Panorama website.
```

**Actual**:
```
To view transaction history, select 'Go to page'. To view transactions older than 3 years, sign in to the full Panorama website.
```

---

#### 2. bt_all_transactions (Similarity: 1.00)
**Trigger**: "can i transfer money"  
**Issue**: Significant content differences

**Expected**:
```
What type of transaction are you looking to make today?
```

**Actual**:
```
What type of transaction are you looking to make today?
```

---

#### 3. bt_change_insurance (Similarity: 1.00)
**Trigger**: "How can I reduce or cancel my insurance cover?"  
**Issue**: Significant content differences

**Expected**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

**Actual**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

---

#### 4. bt_all_transactions (Similarity: 1.00)
**Trigger**: "can i transfer money"  
**Issue**: Significant content differences

**Expected**:
```
What type of transaction are you looking to make today?
```

**Actual**:
```
What type of transaction are you looking to make today?
```

---

#### 5. bt_change_insurance (Similarity: 1.00)
**Trigger**: "How can I reduce or cancel my insurance cover?"  
**Issue**: Significant content differences

**Expected**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

**Actual**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

---

#### 6. bt_all_transactions (Similarity: 1.00)
**Trigger**: "can i transfer money"  
**Issue**: Significant content differences

**Expected**:
```
What type of transaction are you looking to make today?
```

**Actual**:
```
What type of transaction are you looking to make today?
```

---

#### 7. bt_change_insurance (Similarity: 1.00)
**Trigger**: "How can I reduce or cancel my insurance cover?"  
**Issue**: Significant content differences

**Expected**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

**Actual**:
```
For any insurance related enquiry, please call 1300 553 764, 8:30am to 6:30pm (Sydney time) Monday to Friday. Is there anything else I can help you with?
```

---

### Failed Response Cases (50 items)
*These tests failed to extract a valid response from the API.*

#### 1. 44_CloseAcc_S
**Trigger**: "when my account gets deactivated"  
**Error**: Unknown error
**Session ID**: node0uwgttythv6vi8pnowqco9myb70941750629248376b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 2. 79_EstatementError_S
**Trigger**: "my cc statement not appear in my account on the internet banking"  
**Error**: Unknown error
**Session ID**: node02dwpd73f4wzxxaod4eu7klxd70981750629248380b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 3. bt_account_number
**Trigger**: "i need my member number"  
**Error**: Unknown error
**Session ID**: node0u5sc6galhgpl7nevmixow2nc71041750629248386b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 4. bt_balance
**Trigger**: "how is my investment accounts doing?"  
**Error**: Unknown error
**Session ID**: node01wt50jcqbgnb310p9edcyi3pc171061750629248388b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 5. bt_link_account
**Trigger**: "where do we go to link a bank account on behalf of a client?"  
**Error**: Unknown error
**Session ID**: node0wp0giha24a4m1fktkyz43v2v771211750629248403b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 6. bt_trading_fees
**Trigger**: "What are the mutual fund trading fees of my account with id QPO8Jo8vdDHMepg41PBwckXm4KdK1yUdmXOwK"  
**Error**: Unknown error
**Session ID**: node01maubhxd3zj3veja9wjnfzmz71261750629248408b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 7. 44_CloseAcc_S
**Trigger**: "when my account gets deactivated"  
**Error**: Unknown error
**Session ID**: node0nmzl18jmgtkd1i806plaq1pqc71331750629248415b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 8. 47_TxnHistoryLength_S
**Trigger**: "Tell me how long you keep transaction history."  
**Error**: Unknown error
**Session ID**: node0ur8ypl2l9ohm1d64myboqlts71341750629248416b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 9. bt_account_number
**Trigger**: "i need my member number"  
**Error**: Unknown error
**Session ID**: node0np7ibndqn8akyac4wtudvniu71421750629248424b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 10. bt_balance
**Trigger**: "how is my investment accounts doing?"  
**Error**: Unknown error
**Session ID**: node0i0y4gegtp7krlkr6rnfr5wfn71441750629248426b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 0 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 7 cases require review of expected vs actual responses
3. **API Failures**: 50 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_client_details`: INTENT_MISMATCH: 22
- `44_CloseAcc_S`: FAILED_RESPONSE: 3
- `47_TxnHistoryLength_S`: CONTENT_MISMATCH: 1, FAILED_RESPONSE: 2
- `bt_account_number`: FAILED_RESPONSE: 3
- `bt_all_transactions`: CONTENT_MISMATCH: 3
- `bt_balance`: FAILED_RESPONSE: 3
- `bt_change_insurance`: CONTENT_MISMATCH: 3
- `bt_link_account`: FAILED_RESPONSE: 3
- `79_EstatementError_S`: FAILED_RESPONSE: 2
- `bt_trading_fees`: FAILED_RESPONSE: 2


### Success Patterns
**Consistently Passing Intents**: 2257 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-06-23 11:39:21
**Analysis Scope**: All 2336 test cases from segment `bt_account__advised_super`
