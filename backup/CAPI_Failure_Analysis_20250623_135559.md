# CAPI Test Failure Analysis Report

**Generated**: 2025-06-23 13:55:59  
**Total Tests Executed**: 2336  
**Total Failures**: 45  
**Success Rate**: 98.1%  

---

## Executive Summary

### Failure Breakdown
- **Partial Pass**: 0 (0.0%) - High similarity but not exact match
- **Content Mismatch**: 0 (0.0%) - Moderate similarity, content differs
- **Failed Response**: 23 (1.0%) - Unable to extract valid response
- **Failed Session**: 0 (0.0%) - Session creation failed
- **Failed Message**: 0 (0.0%) - Message sending failed

---

## Detailed Failure Analysis

### Failed Response Cases (23 items)
*These tests failed to extract a valid response from the API.*

#### 1. 79_EstatementError_S
**Trigger**: "my cc statement not appear in my account on the internet banking"  
**Error**: Unknown error
**Session ID**: node03j5877nv5j9dkgowko3yhjjw125871750629253868b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 2. bt_balance
**Trigger**: "how is my investment accounts doing?"  
**Error**: Unknown error
**Session ID**: node01trfigxegcmiw3c4ksveyhv4125951750629253876b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 3. bt_trading_fees
**Trigger**: "What are the mutual fund trading fees of my account with id QPO8Jo8vdDHMepg41PBwckXm4KdK1yUdmXOwK"  
**Error**: Unknown error
**Session ID**: node010g62naqnwiao1ddk6lmxfsdme126151750629253896b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 4. bt_balance
**Trigger**: "how is my investment accounts doing?"  
**Error**: Unknown error
**Session ID**: node017d9hw0does941a1pq7hzr15jg126331750629253914b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 5. 79_EstatementError_S
**Trigger**: "my cc statement not appear in my account on the internet banking"  
**Error**: Unknown error
**Session ID**: node01x9jcbb5srhsj1svhss1gohba9126601750629253941b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 6. bt_balance
**Trigger**: "how is my investment accounts doing?"  
**Error**: Unknown error
**Session ID**: node01dqaaj88u0pbe14krc55e4pxee126681750629253949b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 7. bt_trading_fees
**Trigger**: "What are the mutual fund trading fees of my account with id QPO8Jo8vdDHMepg41PBwckXm4KdK1yUdmXOwK"  
**Error**: Unknown error
**Session ID**: node01gwcr0yhx7d6pkeov31b3xd9o126881750629253969b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 8. bt_amend_advice_fee
**Trigger**: "Can you show me how to make changes to the advice fee?"  
**Error**: Unknown error
**Session ID**: node07xptk96qqko71potj9z2fj26f128251750629254106b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 9. bt_auto_invest
**Trigger**: "Can I have money in my account automatically invested into my portfolio?"  
**Error**: Unknown error
**Session ID**: node01rjqvf8ldi5ir1q4tabc88wyrw128271750629254108b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

#### 10. bt_cancel_trade
**Trigger**: "How can we reverse this trade?"  
**Error**: Unknown error
**Session ID**: node01pgs5mhxvbom1d3a5191grf1o128321750629254113b4afa67f-f4fc-473b-a7f7-233aa58118ae

---

## Recommendations

### Immediate Actions
1. **Formatting Issues**: 0 cases with minor formatting differences could be resolved with improved text normalization
2. **Content Differences**: 0 cases require review of expected vs actual responses
3. **API Failures**: 23 cases need technical investigation

### Pattern Analysis
**Most Problematic Intents**:
- `bt_client_details`: INTENT_MISMATCH: 22
- `bt_balance`: FAILED_RESPONSE: 3
- `79_EstatementError_S`: FAILED_RESPONSE: 2
- `bt_trading_fees`: FAILED_RESPONSE: 2
- `bt_amend_advice_fee`: FAILED_RESPONSE: 1
- `bt_auto_invest`: FAILED_RESPONSE: 1
- `bt_cancel_trade`: FAILED_RESPONSE: 1
- `bt_centrelink_schedule`: FAILED_RESPONSE: 1
- `bt_change_pension_payment`: FAILED_RESPONSE: 1
- `bt_commence_pension`: FAILED_RESPONSE: 1


### Success Patterns
**Consistently Passing Intents**: 2291 intents passed all validation checks.

**High Similarity Rates**: Most partial passes show >90% similarity, indicating the core logic works correctly.

---

**Report Generated**: 2025-06-23 13:55:59
**Analysis Scope**: All 2336 test cases from segment `bt_account__advised_super`
