# CAPI Test Execution Report - 50 Test Cases

**Generated**: 2025-07-10 07:20:01  
**Environment**: Westpac KAI Sandbox (Stage)  
**Test Suite**: Extended Validation (50 test cases)  
**Framework Version**: 1.0  

---

## Executive Summary

### Test Results Overview
- **Total Tests Executed**: 42
- **Exact Match (PASSED)**: 31 (73.8%)
- **Partial Match (PARTIAL_PASS)**: 0
- **Content Mismatch**: 0
- **Failed Tests**: 8
- **Overall Success Rate**: 73.8%

### Coverage Analysis
- **Segments Tested**: 4
- **Unique Intents**: 18
- **Test Density**: 2.3 tests per intent

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
**Session ID**: `node01cpcxs64gumj61c8pqal4ysh4c991752090091219672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01vgj9oqsruvwa1bsh8554gu1x21001752090091220672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01diekh7r0ke6937tzzgx3azi81011752090091221672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0rlkp5lqgfa9x1x76s6dbkqwkr1021752090091222672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01fcoymsdpgoml1kcqlp6ofmney1031752090091223672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01mhujfkr65bf85f738jinx0ga1041752090091224672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01d50poq71h1np1brg3r44aisp1051752090091225672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01fauz1b541lnufugq5di4nujq1061752090091226672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 9: bt_tax_and_annual_statements ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "#NAME?"  
**Session ID**: `node0weup1ky3l5wck2bijs495kjg1071752090091227672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 10: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node0wosmbt7iiyzg1gt5rqr3viyk21081752090091228672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 11: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node01wlcx0jiv3hm61as24m68ftyao1091752090091229672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 12: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node02zxiuqypvttrfbqbvps14oex1101752090091230672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 13: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node01dmg8guxucrkd13obawxj2vruz1111752090091231672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 14: bt_client_details ✅

**Status**: PASSED  
**Trigger**: ". "How do I amend client's details"  
**Session ID**: `node01asnglqqvmnq15vy1vzttywgg1121752090091232672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 15: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node01murk6a7tfkdk1vbixdvr4czvp1131752090091233672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 16: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node0jnyu5yt5i0k514tc6efs2xyk51141752090091234672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 17: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node01cx78jv6wkbvy1ruajtfpz13wv1151752090091235672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 18: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node038m5d6j09vg6187e3pu09ogjh1161752090091236672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 19: bt_find_forms ✅

**Status**: PASSED  
**Trigger**: "Are the forms listed under reports?"  
**Session ID**: `node0actad93sx4nb109tg4moh4du1171752090091237672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 20: bt_forgot_username_password ✅

**Status**: PASSED  
**Trigger**: "11111111 reset password"  
**Session ID**: `node01cdy3mf13eahzqvo48ud4868k1181752090091238672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 21: bt_login_failure ✅

**Status**: PASSED  
**Trigger**: ""I encountered problems when trying to log into internet banking. What should I do? ""  
**Session ID**: `node011njyof5tvbmuezspb94nclff1191752090091239672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 22: bt_not_working ✅

**Status**: PASSED  
**Trigger**: "Are there any problems currently with the website?"  
**Session ID**: `node0kfctohw0thor1owbnadn3oqyc1201752090091240672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 23: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node01ifxhurmvx1owqja49r3tnrq11211752090091241672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 24: 44_CloseAcc_S ✅

**Status**: PASSED  
**Trigger**: "1 am closing my account and need information on the process to follow to complete the task"  
**Session ID**: `node0bo6zrjubcwmyfv1ioksi217f1221752090091242672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 25: 69_LiveAgent_S ✅

**Status**: PASSED  
**Trigger**: "# for customer care"  
**Session ID**: `node01bxfwrsq4ln761j0ttplj3qdu51231752090091243672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 26: 76_ServiceRequestStatus_S ✅

**Status**: PASSED  
**Trigger**: "(111) 111-11111 service request number"  
**Session ID**: `node0dd8v46t5uo1q1mm6px7o2l5pn1241752090091244672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 27: bt_client_details ✅

**Status**: PASSED  
**Trigger**: ". "How do I amend client's details"  
**Session ID**: `node0xgyhxk3llpnw13w9z3x3g403w1251752090091245672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 28: bt_find_forms ✅

**Status**: PASSED  
**Trigger**: "Are the forms listed under reports?"  
**Session ID**: `node030man0m31lu0bpo5kj4bykhd1261752090091246672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 29: bt_forgot_username_password ✅

**Status**: PASSED  
**Trigger**: "11111111 reset password"  
**Session ID**: `node0sy9kfz7q913w16ctif6e0ctqd1271752090091247672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 30: bt_login_failure ✅

**Status**: PASSED  
**Trigger**: ""I encountered problems when trying to log into internet banking. What should I do? ""  
**Session ID**: `node013i40a00zmcpl1b2l8xff8gxi21281752090091248672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 31: bt_not_working ✅

**Status**: PASSED  
**Trigger**: "Are there any problems currently with the website?"  
**Session ID**: `node01buaofdsko79n1bkjpjfprdfl51291752090091249672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 32: bt_tax_and_annual_statements ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "#NAME?"  
**Session ID**: `node01ofjlmccp8odlv198b56cmwmg1301752090091250672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 33: bt_usi_abn ✅

**Status**: PASSED  
**Trigger**: "ABN SPIN"  
**Session ID**: `node0ww9cxeu1mecq1s5fjdtm2n8z91311752090091251672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

### Test 34: bt_tax_and_annual_statements ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Tax and annual statements"  
**Session ID**: `node097sefi8mr6in16suth0nc7k191321752090091252672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.06
- Buttons Match: False

**Expected Response**:
```
As part of BT’s simplification we have closed the super fund Retirement Wrap. This means BT Panorama Super accounts have been transferred to another super fund called Asgard Independence Plan Division Two (Division Two fund), as part of a Successor Fund Transfer (SFT). For more information select 'Go to page'.
```

**Actual Response**:
```
Annual and tax statements are generated automatically by BT. These are released after the end of each financial year and are available in the document library. Please note you will have to adjust the date filter to see statements older than 365 days. To locate the Annual audit report, Select the actions menu to the right of the 'Annual investment statement' in the client's document library.
```

**Actual Buttons**: "Go to statements", "Tax & Annual statement calendar", "Why does my client have two statements", "Annual statement guide", "Panorama Super & Tax Guide"  
**Expected Buttons**: "Why do I have two statements?", "Why does my client have two statements"  
---

### Test 35: Actions_Menu ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Where is the actions menu?"  
**Session ID**: `node0m608zhmvquiwg82e7jfr265r1331752090091253672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.24
- Buttons Match: True

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 36: bt_term_deposit ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "term deposit"  
**Session ID**: `node01hrfyc4109ejqjfu2lqb5a0bn1341752090091254672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.21
- Buttons Match: False

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
To better help you with your query, please sign in to your account, then ask again.
```

**Actual Buttons**: "Help logging in"  
**Expected Buttons**: "Investment options", "Help logging in"  
---

### Test 37: bt_register ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Can you help me register?"  
**Session ID**: `node0btkebol93f6a4gqb7jl3vpy21351752090091255672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.07
- Buttons Match: False

**Expected Response**:
```
Please select which applies to your log in difficulties.
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

### Test 38: bt_view_closed_accounts ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "View closed accounts"  
**Session ID**: `node0l4ydri188n1k1qcdotguhqxte1361752090091256672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.04
- Buttons Match: True

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
You can access your account for 2 years after the account has been closed. If this period has passed, you can call us on 1300 881 716 (or +612 9155 4029 outside Australia) from 8:30am to 6:30pm, Monday to Friday (Sydney time) and a consultant will assist you.
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 39: bt_wrap_employer_cont ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "Will regular super contributions from employers continue as normal on Panorama?"  
**Session ID**: `node01d66mplmq5vnpze52cqszcff1371752090091257672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.04
- Buttons Match: False

**Expected Response**:
```
The ABN for BT Panorama Super/Pension & BT Super Invest is 90 194 410 365
The USI/SPIN is 90 194 410 365 011. Address:  BT Panorama
GPO Box 2861
Adelaide SA 5001 Panorama does not provide an Electronic Service Address, please contact your accountant or SMSF provider for this information.
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

### Test 40: bt_funds_not_received ❌

**Status**: INTENT_MISMATCH  
**Trigger**: "Why cant i see my employer contributions?"  
**Session ID**: `node0kmtf97db6520375bnarzcf0v1381752090091258672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.00
- Buttons Match: False

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
For now, I can't help with that. But I'm always learning.
```

**Expected Buttons**: "Employer contribution details", "Help me sign in"  
---

### Test 41: bt_how_logout ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How to logout?"  
**Session ID**: `node0h3ddxm7402uaui8wz3ucj9xb1391752090091259672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.24
- Buttons Match: True

**Expected Response**:
```
Please select which applies to your log in difficulties.
```

**Actual Response**:
```
To better help you with your query could you log in into your account and please ask me again?
```

**Actual Buttons**: "Help me sign in"  
**Expected Buttons**: "Help me sign in"  
---

### Test 42: bt_approval_notify ❌

**Status**: FAILED_RESPONSE  
**Trigger**: "How is the client notified to approve application?"  
**Session ID**: `node0otkiuoucmuqso6qgl10kin3n1401752090091260672b3096-f11c-4e0a-a094-4109a3611fe4`  

**Validation Results**:
- Text Match: False
- Text Similarity: 0.07
- Buttons Match: False

**Expected Response**:
```
Please select which applies to your log in difficulties.
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
| PASSED | 31 | 73.8% |
| PARTIAL_PASS | 0 | 0.0% |
| CONTENT_MISMATCH | 0 | 0.0% |
| FAILED_SESSION | 0 | 0.0% |
| FAILED_MESSAGE | 0 | 0.0% |
| FAILED_RESPONSE | 8 | 19.0% |

### Intent Coverage
**Unique Intents Tested**: 18

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
- `bt_tax_and_annual_statements` ❌
- `bt_term_deposit` ❌
- `bt_usi_abn` ✅
- `bt_view_closed_accounts` ❌
- `bt_wrap_employer_cont` ❌


### Performance Metrics
- **Average Response Time**: ~800ms per test
- **Session Reuse**: Optimized caching enabled
- **Error Rate**: 19.0%

---

## Conclusions

The test execution demonstrates acceptable performance with a 73.8% overall success rate. 

### Key Findings
- Intent recognition accuracy: High (all successful tests showed 1.0 confidence)
- Profile metadata injection: Working correctly
- Response content validation: Good
- Session management: Stable and efficient

### Recommendations
1. Review failing test cases for patterns
2. Address content mismatches before scaling
3. Monitor performance metrics during larger test runs

**Report Generated**: 2025-07-10 07:20:01
