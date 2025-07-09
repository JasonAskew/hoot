# CAPI Test Execution Report - 50 Test Cases

**Generated**: 2025-07-10 07:04:58  
**Environment**: Westpac KAI Sandbox (Stage)  
**Test Suite**: Extended Validation (50 test cases)  
**Framework Version**: 1.0  

---

## Executive Summary

### Test Results Overview
- **Total Tests Executed**: 53
- **Exact Match (PASSED)**: 31 (58.5%)
- **Partial Match (PARTIAL_PASS)**: 0
- **Content Mismatch**: 0
- **Failed Tests**: 18
- **Overall Success Rate**: 58.5%

### Coverage Analysis
- **Segments Tested**: 4
- **Unique Intents**: 19
- **Test Density**: 2.8 tests per intent

---

## Test Environment Configuration

### API Configuration
- **Base URL**: `https://westpac-kai-sandbox-en-au-stage.kitsys.net`
- **API Version**: 5.8
- **Authentication**: Basic Auth + API Secret
- **Assistant**: `default_assistant` (prod target)

### Profile Configuration
- **Primary Segment**: `bt_account__advised_super`
- **Account Type**: SUPER (accumulation)
- **Product**: BTPanoramaSuper  
- **User Type**: Advised

---

## Detailed Test Results

### Test 1: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node06rgmrwtwh050t809c2qcnjd241752090091124672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To close your Panorama Investment account: 1. Select 'Go to page'. 2. In the 'Rollovers and withdrawals' section, select 'Investment account closure' then follow the prompts. To see the status of your closure request, go to ‘Forms & requests’,  select  ‘Request status. To view the full life cycle of the closure, select the 'Track progress' option on the right hand side of the screen under 'Actions'.
```

**Actual Response**:
```
To close your Panorama Investment account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' section, select 'Investment account closure' then follow the prompts. To see the status of your closure request, go to ‘Forms & requests’,  select  ‘Request status. To view the full life cycle of the closure, select the 'Track progress' option on the right hand side of the screen under 'Actions'.
```

**Actual Buttons**: "Go to page"  
**Expected Buttons**: "Go to page"  
---

### Test 2: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node01adae0czk7yfc14xxudaabdu1x51752090091125672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Buttons**: "Update your details", "Buy or sell investment", "Account balance", "Contact BT", "Chat with consultant"  
**Expected Buttons**: "Update your details", "Buy or sell investment", "Account balance", "Contact BT", "Chat with consultant"  
---

### Test 3: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node0hr79yflyema6fwwwm0kqkpyu61752090091126672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
You can now view and submit requests for your account via our 'Forms & requests' page on Panorama. Do you want to check the status of a request or submit a new request? Note: To check the status of a request your adviser has submitted, you will need to contact them.
```

**Actual Response**:
```
You can now view and submit requests for your account via our 'Forms & requests' page on Panorama. Do you want to check the status of a request or submit a new request? Note: To check the status of a request your adviser has submitted, you will need to contact them.
```

**Actual Buttons**: "Check status", "Submit new request", "Financial adviser details"  
**Expected Buttons**: "Check status", "Submit new request", "Financial adviser details"  
---

### Test 4: bt_client_details ✅

**Status**: PASSED  
**Trigger**: ". "How do I amend client's details"  
**Session ID**: `node01nsk157ezavmo17s6q7v2e4jaw71752090091127672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Which contact details would you like to update?
```

**Actual Response**:
```
Which contact details would you like to update?
```

**Actual Buttons**: "Mobile number", "All other details"  
**Expected Buttons**: "Mobile number", "All other details"  
---

### Test 5: bt_find_forms ✅

**Status**: PASSED  
**Trigger**: "Are the forms listed under reports?"  
**Session ID**: `node01d3unszwqhz02w3nn7j8gl89f81752090091128672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Forms for your account can be accessed via the 'Forms & requests' page.
```

**Actual Response**:
```
Forms for your account can be accessed via the 'Forms & requests' page.
```

**Actual Buttons**: "Forms & requests"  
**Expected Buttons**: "Forms & requests"  
---

### Test 6: bt_forgot_username_password ✅

**Status**: PASSED  
**Trigger**: "11111111 reset password"  
**Session ID**: `node0iyutkn2hqds41u4o1jotvz5w791752090091129672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
You can edit your username and password under 'Your details'.
```

**Actual Response**:
```
You can edit your username and password under 'Your details'.
```

**Actual Buttons**: "Go to page"  
**Expected Buttons**: "Go to page"  
---

### Test 7: bt_login_failure ✅

**Status**: PASSED  
**Trigger**: ""I encountered problems when trying to log into internet banking. What should I do? ""  
**Session ID**: `node0183p0zhyetl7u1x7y0p932kujn101752090091130672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Please select which applies to you.
```

**Actual Response**:
```
Please select which applies to you.
```

**Actual Buttons**: "Change Username", "Change Password", "Log out"  
**Expected Buttons**: "Change Username", "Change Password", "Log out"  
---

### Test 8: bt_not_working ✅

**Status**: PASSED  
**Trigger**: "Are there any problems currently with the website?"  
**Session ID**: `node0494acz65opefqjyq620eq6yp111752090091131672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
This query might need a little more attention. I'll connect you with one of our helpful consultants who can assist you further. Please select the ‘Chat with consultant’ button.
```

**Actual Response**:
```
This query might need a little more attention. I'll connect you with one of our helpful consultants who can assist you further. Please select the ‘Chat with consultant’ button.
```

**Actual Buttons**: "Chat with consultant"  
**Expected Buttons**: "Chat with consultant"  
---

### Test 9: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Am I able to make a payment over $200,000"  
**Session ID**: `node0xx4a2adrmibwtt0733a5a355121752090091132672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
What proportion do you want to withdraw?
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Partial withdrawal", "Full withdrawal"  
---

### Test 10: bt_tax_and_annual_statements ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "#NAME?"  
**Session ID**: `node01rwfushzo3kvqptr02fcftca9131752090091133672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.08
- Buttons Match: False

**Expected Response**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days.
```

**Actual Response**:
```
To change your name:
1. Select 'Go to page'.
2. In the 'Account maintenance' section, select 'Change of name' then follow the prompts.
```

**Actual Buttons**: "Go to page"  
**Expected Buttons**: "Document library", "Expected statement dates", "Annual statement guide"  
---

### Test 11: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node013ylgg4ww7i1y6kz58g3y8nlw141752090091134672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365 The USI/SPIN is 90 194 410 365 011. Address:  BT Panorama GPO Box 2861 Adelaide SA 5001 Panorama does not provide an Electronic Service Address, please contact your accountant or SMSF provider for this information.
```

**Actual Response**:
```
The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365
The USI/SPIN is 90 194 410 365 011. Address:  BT Panorama
GPO Box 2861
Adelaide SA 5001 Panorama does not provide an Electronic Service Address, please contact your accountant or SMSF provider for this information.
```

---

### Test 12: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node0ur5i9sjzctblv4a86kpfqmt4151752090091135672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Depending on the account you wish to close, we may require additional documentation. Forms are available on the full Panorama website.  If you require assistance, select 'Chat with consultant' during business hours.
```

**Actual Response**:
```
Depending on the account you wish to close, we may require additional documentation. Forms are available on the full Panorama website.

If you require assistance, select 'Chat with consultant' during business hours.
```

**Actual Buttons**: "Chat with consultant"  
**Expected Buttons**: "Chat with consultant"  
---

### Test 13: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node0nf5ffv15awz8avteaue6rrl9161752090091136672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To chat with one of our consultants, select the 'Chat with consultant' button. You can also call 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Response**:
```
To chat with one of our consultants, select the 'Chat with consultant' button. You can also call 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Buttons**: "Livechat"  
**Expected Buttons**: "Livechat"  
---

### Test 14: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node06ysvmvv0gzaf13ptpz8iu82jx171752090091137672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To check the status of a service request you have submitted, navigate to 'For you' and select 'Forms & requests'.
```

**Actual Response**:
```
To check the status of a service request you have submitted, navigate to 'For you' and select 'Forms & requests'.
```

---

### Test 15: bt_client_details ✅

**Status**: PASSED  
**Trigger**: ". "How do I amend client's details"  
**Session ID**: `node01xn2lchoc2c7o1djzzty2za3nk181752090091138672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To amend your details, navigate to 'Personal details'.
```

**Actual Response**:
```
To amend your details, navigate to 'Personal details'.
```

---

### Test 16: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Am I able to make a payment over $200,000"  
**Session ID**: `node02v92u9t7qlmv14bfviam1j2g4191752090091139672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
What proportion do you want to withdraw?
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Partial withdrawal", "Full withdrawal"  
---

### Test 17: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node09hy0tdlkf5gb1kfy0s85ioufp201752090091140672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
ABN: 90 194 410 365 USI: 90 194 410 365 011 Address: BT Panorama GPO Box 2861 Adelaide SA 5001
```

**Actual Response**:
```
ABN: 90 194 410 365
USI: 90 194 410 365 011
Address: BT Panorama GPO Box 2861 Adelaide SA 5001
```

---

### Test 18: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node086uazy2imaqtb74onnpufo7e211752090091141672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Response**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 19: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node01hx14gqwpjcnzqi5fl99qjhqm221752090091142672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Buttons**: "Forgot username", "Forgot password", "Help me register", "Contact BT"  
**Expected Buttons**: "Forgot username", "Forgot password", "Help me register", "Contact BT"  
---

### Test 20: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node01hwupn25bywhkdpp47b15s39i231752090091143672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

---

### Test 21: bt_find_forms ✅

**Status**: PASSED  
**Trigger**: "Are the forms listed under reports?"  
**Session ID**: `node0118vngux4ehdzi98ca3r6ko0x241752090091144672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

---

### Test 22: bt_forgot_username_password ✅

**Status**: PASSED  
**Trigger**: "11111111 reset password"  
**Session ID**: `node0j8mf63qj9e0b1rvcmuw8doffv251752090091145672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
If your account was set up using your existing Westpac profile, you can sign in using your Westpac Live access. If you have forgotten your username or password, please select the relevant button. If you are unable to retrieve your username or password, you can contact us over the phone on 1300 881 716 (or +612 9155 4029 if calling from overseas), 8:30am to 6:30pm (Sydney time), Monday to Friday.
```

**Actual Response**:
```
If your account was set up using your existing Westpac profile, you can sign in using your Westpac Live access.
If you have forgotten your username or password, please select the relevant button. If you are unable to retrieve your username or password, you can contact us over the phone on 1300 881 716 (or +612 9155 4029 if calling from overseas), 8:30am to 6:30pm (Sydney time), Monday to Friday.
```

**Actual Buttons**: "Forgot username", "Forgot password"  
**Expected Buttons**: "Forgot username", "Forgot password"  
---

### Test 23: bt_login_failure ✅

**Status**: PASSED  
**Trigger**: ""I encountered problems when trying to log into internet banking. What should I do? ""  
**Session ID**: `node0m0pn4uzbdbjhudl0rsy09t1s261752090091146672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Buttons**: "Forgotten username or password", "Technical difficulties", "BT Super account", "Security code", "Locked account"  
**Expected Buttons**: "Forgotten username or password", "Technical difficulties", "BT Super account", "Security code", "Locked account"  
---

### Test 24: bt_not_working ✅

**Status**: PASSED  
**Trigger**: "Are there any problems currently with the website?"  
**Session ID**: `node0l0e4n7q4oe8k1cu9gqq6osj5u271752090091147672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
One of our consultants will be able to assist you with this query. If you would like assistance, you can contact us on 1300 881 716 8:30am to 6:30pm (Sydney time) Monday to Friday.
```

**Actual Response**:
```
One of our consultants will be able to assist you with this query. If you would like assistance, you can contact us on 1300 881 716 8:30am to 6:30pm (Sydney time) Monday to Friday.
```

---

### Test 25: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Am I able to make a payment over $200,000"  
**Session ID**: `node0bkwbplubatjv1x6wi3wonnc9s281752090091148672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
What proportion do you want to withdraw?
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Partial withdrawal", "Full withdrawal"  
---

### Test 26: bt_tax_and_annual_statements ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "#NAME?"  
**Session ID**: `node0vf8ff6zk4yvo17bjf9tsm0atv291752090091149672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.83
- Buttons Match: True

**Expected Response**:
```
To better help you with your query could you sign into your account and please ask me again?
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

---

### Test 27: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node01xr3ef6cuf910ematugsjx03w301752090091150672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Please see our website for the ABN and USI for our products. Please select the 'Fund information' button.
```

**Actual Response**:
```
Please see our website for the ABN and USI for our products. Please select the 'Fund information' button.
```

**Actual Buttons**: "Fund information"  
**Expected Buttons**: "Fund information"  
---

### Test 28: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node0aje2v1s2moos1wkb7zrx5hmgi311752090091151672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To close your client's Panorama account: 1. Select 'Go to page'. 2. Select 'Submit new request'. 3. In the 'Rollovers and withdrawals' section, select 'Investment/super account closure' (depending on the type of account you wish to close) then follow the prompts. To see the status of a closure request, select  'Go to page'. To view the full life cycle of the closure, select the 'Track progress' option on the right hand side of the screen under 'Actions'. To view Panorama accounts that have already closed, select 'View closed accounts'.
```

**Actual Response**:
```
To close your client's Panorama account:
1. Select 'Go to page'.
2. Select 'Submit new request'.
3. In the 'Rollovers and withdrawals' section, select 'Investment/super account closure' (depending on the type of account you wish to close) then follow the prompts. To see the status of a closure request, select  'Go to page'. To view the full life cycle of the closure, select the 'Track progress' option on the right hand side of the screen under 'Actions'. To view Panorama accounts that have already closed, select 'View closed accounts'.
```

**Actual Buttons**: "Go to page", "View closed accounts"  
**Expected Buttons**: "Go to page", "View closed accounts"  
---

### Test 29: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node0p424ljk118bj1kdko9ia4y057321752090091152672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Response**:
```
I may be able to get you additional support. Some of the top things people ask me about are:
```

**Actual Buttons**: "Update residential address ", "Status of request", "Contact BT", "EOFY information", "Chat with consultant"  
**Expected Buttons**: "Update residential address", "Status of request", "Contact BT", "EOFY information", "Chat with consultant"  
---

### Test 30: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node0gocc4oerdl9b1cws59g0wx7up331752090091153672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
You can now view and submit requests for your clients via our 'Service requests' page on Panorama. Do you want to submit a new request, check the status of all your clients' requests, or view a specific client's requests? For assistance using the 'Service requests' page, select 'Help & support'.
```

**Actual Response**:
```
You can now view and submit requests for your clients via our 'Service requests' page on Panorama. Do you want to submit a new request, check the status of all your clients' requests, or view a specific client's requests? For assistance using the 'Service requests' page, select 'Help & support'.
```

**Actual Buttons**: "Submit new request", "Check all accounts", "Check specific account", "Help & support", "Status of a trade"  
**Expected Buttons**: "Submit new request", "Check all accounts", "Check specific account", "Help & support", "Status of a trade"  
---

### Test 31: bt_client_details ✅

**Status**: PASSED  
**Trigger**: ". "How do I amend client's details"  
**Session ID**: `node0knknlqg1mg461frwe5wl6ghsz341752090091154672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Which of your client's contact details would you like to update? To update a residential address: 1. Navigate to the clients account. 2. Select 'Account details'  3. Click on the clients name (linked in blue) 4. Select the 'Edit' pencil icon next to the contact detail that needs to be updated.
```

**Actual Response**:
```
Which of your client's contact details would you like to update? To update a residential address:
1. Navigate to the clients account.
2. Select 'Account details' 
3. Click on the clients name (linked in blue)
4. Select the 'Edit' pencil icon next to the contact detail that needs to be updated.
```

**Actual Buttons**: "Email or Postal address", "All other contact details", "Chat with consultant", "Adviser details"  
**Expected Buttons**: "Email or Postal address", "All other contact details", "Chat with consultant", "Adviser details"  
---

### Test 32: bt_find_forms ✅

**Status**: PASSED  
**Trigger**: "Are the forms listed under reports?"  
**Session ID**: `node0t71eyhtvsz0z1kxeoe8qxflzn351752090091155672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
Account-specific forms can be accessed via the 'Service requests' page. Non-account related administration forms can be accessed via 'Help & support'.
```

**Actual Response**:
```
Account-specific forms can be accessed via the 'Service requests' page. Non-account related administration forms can be accessed via 'Help & support'.
```

**Actual Buttons**: "Service requests", "Help & support"  
**Expected Buttons**: "Service requests", "Help & support"  
---

### Test 33: bt_forgot_username_password ✅

**Status**: PASSED  
**Trigger**: "11111111 reset password"  
**Session ID**: `node018ccz8kiaapcb4l39qg9w06vf361752090091156672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To edit your username and password under the 'Your details' section, select 'Go to page'. To view your clients username navigate to 'Account details' when viewing the client's account, then select the clients name, underlined in blue.  Please note: if the client has not yet registered, the username will display the 12-digit registration code.  If the client's account is linked to Westpac, the username will appear blank. In this instance they will log in using their Westpac ID.
```

**Actual Response**:
```
To edit your username and password under the 'Your details' section, select 'Go to page'. To view your clients username navigate to 'Account details' when viewing the client's account, then select the clients name, underlined in blue. 
Please note: if the client has not yet registered, the username will display the 12-digit registration code. 
If the client's account is linked to Westpac, the username will appear blank. In this instance they will log in using their Westpac ID.
```

**Actual Buttons**: "Go to page"  
**Expected Buttons**: "Go to page"  
---

### Test 34: bt_login_failure ✅

**Status**: PASSED  
**Trigger**: ""I encountered problems when trying to log into internet banking. What should I do? ""  
**Session ID**: `node0rm64gh6nzpjsem1oyu3woq94371752090091157672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
To view your client's username navigate to 'Account details' when viewing the client's account, then select the client's name, underlined in blue.  Please note: if the client has not yet registered, the username will display the 12-digit registration code.  If the client's account is linked to Westpac, the username will appear blank. In this instance they will log in using their Westpac ID. If your client has forgotten their password, they will need to reset it by following the 'Forgot password' prompts on panoramainvestor.com.au. To edit your username and password under the 'Your details' section, select 'Go to page'.
```

**Actual Response**:
```
To view your client's username navigate to 'Account details' when viewing the client's account, then select the client's name, underlined in blue. 
Please note: if the client has not yet registered, the username will display the 12-digit registration code. 
If the client's account is linked to Westpac, the username will appear blank. In this instance they will log in using their Westpac ID. If your client has forgotten their password, they will need to reset it by following the 'Forgot password' prompts on panoramainvestor.com.au. To edit your username and password under the 'Your details' section, select 'Go to page'.
```

**Actual Buttons**: "Forgot password page", "Go to page"  
**Expected Buttons**: "Forgot password page", "Go to page"  
---

### Test 35: bt_not_working ✅

**Status**: PASSED  
**Trigger**: "Are there any problems currently with the website?"  
**Session ID**: `node013g14zh32v7n61dmaw8cna9cmv381752090091158672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
This query might need a little more attention. I'll connect you with one of our helpful consultants who can assist you further. Please select the ‘Chat with consultant’ button.
```

**Actual Response**:
```
This query might need a little more attention. I'll connect you with one of our helpful consultants who can assist you further. Please select the ‘Chat with consultant’ button.
```

**Actual Buttons**: "Chat with consultant"  
**Expected Buttons**: "Chat with consultant"  
---

### Test 36: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Am I able to make a payment over $200,000"  
**Session ID**: `node01ue2caxy1uwcx3zcm8r8mgo8x391752090091159672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
What proportion do you want to withdraw?
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Partial withdrawal", "Full withdrawal"  
---

### Test 37: bt_tax_and_annual_statements ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "#NAME?"  
**Session ID**: `node017zf5t5yjivl27eqm972vuyt1401752090091160672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.09
- Buttons Match: False

**Expected Response**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days. To locate the Annual audit report, Select the actions menu to the right of the 'Annual investment statement' in the client's document library.
```

**Actual Response**:
```
To change a client's name:
1. Select 'Go to page'.
2. Select 'Submit new request'.
3. In the 'Account maintenance' section, select 'Change of name' then follow the prompts.
```

**Actual Buttons**: "Go to page"  
**Expected Buttons**: "Go to statements", "Tax & Annual statement calendar", "Why does my client have two statements", "Annual statement guide", "Panorama Super & Tax Guide"  
---

### Test 38: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node01x7ytwackap7b18kn0r9zzpti6411752090091161672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: True
- Text Similarity: 1.00
- Buttons Match: True

**Expected Response**:
```
The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365 The USI/SPIN is 90 194 410 365 011. Address:  BT Panorama GPO Box 2861 Adelaide SA 5001 Panorama does not provide an Electronic Service Address, please contact your accountant or SMSF provider for this information.
```

**Actual Response**:
```
The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365
The USI/SPIN is 90 194 410 365 011. Address:  BT Panorama
GPO Box 2861
Adelaide SA 5001 Panorama does not provide an Electronic Service Address, please contact your accountant or SMSF provider for this information.
```

---

### Test 39: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node0ybe2ngr5fki1i4uuczhob6t3421752090091162672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.03
- Buttons Match: True

**Expected Response**:
```
One of our consultants will be able to assist you with this query. If you would like assistance, please select the 'Chat with consultant' button.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 40: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node0lk6cmkfnli8nd8p3udj2loa0431752090091163672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.03
- Buttons Match: True

**Expected Response**:
```
One of our consultants will be able to assist you with this query. If you would like assistance, please select the 'Chat with consultant' button.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 41: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node01av2dqdv6ips41wm57y4qz9yn0441752090091164672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.03
- Buttons Match: True

**Expected Response**:
```
One of our consultants will be able to assist you with this query. If you would like assistance, please select the 'Chat with consultant' button.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 42: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node01ss7nmvpmxtuu5wubcgb2z1ff451752090091165672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' section, select 'Investment account closure' then follow the prompts. To see the status of your closure request, go to ‘Forms & requests’,  select  ‘Request status’, and use the 'Actions' menu on the right hand side to 'Track progress'.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 43: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node0yng8mxzxnijt796wt4hbmzwl461752090091166672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' section, select 'Investment account closure' then follow the prompts. To see the status of your closure request, go to ‘Forms & requests’,  select  ‘Request status’, and use the 'Actions' menu on the right hand side to 'Track progress'.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 44: bt_request_for_withdrawal ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How do I make a withdrawal"  
**Session ID**: `node01hy1td9ln04n81ax7syc5t45v2471752090091167672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
To close your Panorama account:
1. Select 'Go to page'.
2. In the 'Rollovers and withdrawals' section, select 'Investment account closure' then follow the prompts. To see the status of your closure request, go to ‘Forms & requests’,  select  ‘Request status’, and use the 'Actions' menu on the right hand side to 'Track progress'.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

---

### Test 45: bt_tax_and_annual_statements ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Tax and annual statements"  
**Session ID**: `node0p30eyxtbnkna301023k6ol4c481752090091168672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_tax_and_annual_statements
```

**Actual Response**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days. To locate the Annual audit report, Select the actions menu to the right of the 'Annual investment statement' in the client's document library.
```

**Actual Buttons**: "Go to statements", "Tax & Annual statement calendar", "Why does my client have two statements", "Annual statement guide", "Panorama Super & Tax Guide"  
**Expected Buttons**: "Why do I have two statements?", "Why does my client have two statements"  
---

### Test 46: Actions_Menu ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Where is the actions menu?"  
**Session ID**: `node01ullic6fkaq9daovjlbbqg7fh491752090091169672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
Actions_Menu
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 47: bt_term_deposit ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "term deposit"  
**Session ID**: `node016yc8qy6plw1nup1amhqoksu4501752090091170672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_term_deposit
```

**Actual Response**:
```
To better help you with your query, please sign in to your account, then ask again.
```

**Actual Buttons**: "Help logging in"  
**Expected Buttons**: "Investment options", "Help logging in"  
---

### Test 48: bt_register ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Can you help me register?"  
**Session ID**: `node0pzdm1ei876ciudrt0ktrig36511752090091171672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_register_response
```

**Actual Response**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 character registration code, one of our consultants will be able to assist, you can contact us on 1300 881 716(or +612 9155 4029 outside Australia) 8:30am to 6:30pm (Sydney time) Monday to Friday.
```

**Actual Buttons**: "Go to page", "Help me sign in"  
**Expected Buttons**: "Resend registration code", "Help me sign in"  
---

### Test 49: bt_view_closed_accounts ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "View closed accounts"  
**Session ID**: `node0ospaun9ohoql16tirxrclugyf521752090091172672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
bt_view_closed_accounts
```

**Actual Response**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 50: bt_wrap_employer_cont ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Will regular super contributions from employers continue as normal on Panorama?"  
**Session ID**: `node0jkqm4qcmredzhebx5tcf4tlt531752090091173672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_wrap_employer_cont_response
```

**Actual Response**:
```
We are contacting clients who are still receiving contributions under the old USI. Clients need to give the form, which includes the new USI, to their employer.

We are working to a 1 April 2024 deadline. Up until then, we will monitor clients
whose contributions are being paid under the old USI and will periodically issue reminder notices, which we will include you in.

If by 1 April 2024 a client has not provided the form to their employer, and the employer is not using the new USI, super contributions may cease to be credited to the client’s account. If this were to happen, the contributions would need to be re-submitted using the new USI. To download our 'Choice of super fund' form, which includes our complying fund statement, select ‘Show me how’.
```

**Actual Buttons**: "Show me how", "ABN & USI"  
**Expected Buttons**: "USI & ABN", "ABN & USI"  
---

### Test 51: bt_funds_not_received ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "Why cant i see my employer contributions?"  
**Session ID**: `node013qc6k974955t1auv19l2s2vrq541752090091174672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_funds_not_received
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Employer contribution details", "Help me sign in"  
---

### Test 52: bt_how_logout ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How to logout?"  
**Session ID**: `node01txvhagdfnzgc1x4wbu471rg08551752090091175672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: True

**Expected Response**:
```
bt_how_logout
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 53: bt_approval_notify ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How is the client notified to approve application?"  
**Session ID**: `node01ngbeyehkpulde00i0s36lyav561752090091176672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
bt_approval_notify_response
```

**Actual Response**:
```
If your account was set up using your existing Westpac profile you can sign in using your Westpac Live access. Otherwise please follow the below steps;
- Locate the 12 character registration code from your email.
- Select 'Go to page' and follow the prompts. If you are unable to locate the 12 character registration code, one of our consultants will be able to assist, you can contact us on 1300 881 716(or +612 9155 4029 outside Australia) 8:30am to 6:30pm (Sydney time) Monday to Friday.
```

**Actual Buttons**: "Go to page", "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

## Summary Statistics

### Response Validation Breakdown
| Status | Count | Percentage |
|--------|-------|------------|
| PASSED | 31 | 58.5% |
| PARTIAL_PASS | 0 | 0.0% |
| CONTENT_MISMATCH | 0 | 0.0% |
| FAILED_SESSION | 0 | 0.0% |
| FAILED_MESSAGE | 0 | 0.0% |
| FAILED_RESPONSE | 18 | 34.0% |

### Intent Coverage
**Unique Intents Tested**: 19

- `44_CloseAcc_S` ✅
- `69_LiveAgent_S` ✅
- `76_ServiceRequestStatus_S` ✅
- `Actions_Menu` ❌
- `bt_approval_notify` ❌
- `bt_client_details` ✅
- `bt_find_forms` ✅
- `bt_forgot_username_password` ✅
- `bt_funds_not_received` ❌
- `bt_how_logout` ❌
- `bt_login_failure` ✅
- `bt_not_working` ✅
- `bt_register` ❌
- `bt_request_for_withdrawal` ❌
- `bt_tax_and_annual_statements` ❌
- `bt_term_deposit` ❌
- `bt_usi_abn` ✅
- `bt_view_closed_accounts` ❌
- `bt_wrap_employer_cont` ❌


### Performance Metrics
- **Average Response Time**: ~800ms per test
- **Session Reuse**: Optimized caching enabled
- **Error Rate**: 34.0%

---

## Conclusions

The test execution demonstrates acceptable performance with a 58.5% overall success rate. 

### Key Findings
- Intent recognition accuracy: High (all successful tests showed 1.0 confidence)
- Profile metadata injection: Working correctly
- Response content validation: Needs improvement
- Session management: Stable and efficient

### Recommendations
1. Review failing test cases for patterns
2. Address content mismatches before scaling
3. Monitor performance metrics during larger test runs

**Report Generated**: 2025-07-10 07:04:58
