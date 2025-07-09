# CAPI Test Execution Report - 50 Test Cases

**Generated**: 2025-07-10 08:11:54  
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
- **Failed Tests**: 9
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
**Session ID**: `node0y1zsogkrmanb1fnmx8349xmvf1421752090091262672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0190hys6bb0c97papcynmxvxdi1431752090091263672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01sxmlqme9y5rr41s4lszdu4l1441752090091264672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0a9hvaahg3dwu1heg4y3t77h3e1451752090091265672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01kvjaott2n1cj1t0iambw6kn8n1461752090091266672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01gexw8oy3r6dg1jdbvo8c7wlis1471752090091267672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01pzychzqoqjzn5z0msgc4v4fv1481752090091268672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01uyywd2wd1iltq32a5xo9wbr11491752090091269672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0zmvvrduz4x2l9fkk8zed5sva1501752090091270672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01dz5sjvx59m181nncgle1t7l8l1511752090091271672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node014a3sithhe0nv128h0ytiwhovd1521752090091272672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01fz78c1rpj9c31irjmcoj6gbjd1531752090091273672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0kslni5fpeuje12rso19fjb8ft1541752090091274672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node013sehek1tal58hft7nobs75k41551752090091275672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0qn75qmro7voj1p34wmkmvmj7f1561752090091276672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node04qybtdyo5i1m1g340iig0fk3p1571752090091277672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0xipu00moh4b716tr31btdc08k1581752090091278672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node018ayxfd6brv4a10m730ti6ov8f1591752090091279672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01amoq5kowjhdsfcuzpr5vztex1601752090091280672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0cepqmb7ukco6bpe00gz6v75d1611752090091281672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0xfzamnt5kacf14cxlqrc75zxy1621752090091282672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node05k3tkj9juslda8uxmkrfvsvo1631752090091283672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0s7qqblim2zpc1dv8ap3pfpzpy1641752090091284672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0o90zjrh3mq2kxvqv4gvn2kdr1651752090091285672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0q599d0o365kfi49b49gykuyv1661752090091286672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01o95k1e2ujkvg1nyf1k9cuwrft1671752090091287672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node017fr64lv0sr82i2diuci0u0q41681752090091288672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0dl45q558s7vk12jbjjw56fxa51691752090091289672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01h0gp7oqnqdty17fuzzwfud8t21701752090091290672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01gf7q8cr1ky7irxtv5hotp1yc1711752090091291672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01x7uo2bjdordr15t1nzbbqggya1721752090091292672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node09ky20sh7wviv11ugtehn060fc1731752090091293672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0q3wu8fuagm9sotgded1pq03m1741752090091294672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0gi6iw1mp9tmgokq1t7n66u7f1751752090091295672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01wbeq3cobtovgih91e0l6gbr41761752090091296672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01ooyq4i1od5nj1jnxt3ag26mda1771752090091297672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0zhaiyn78c54wyvuv5acuts751781752090091298672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node0rmc6lu4uw8wutnaadbhf8uko1791752090091299672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01izjwa655skir1k4dd43qxt66t1801752090091300672b3096-f11c-4e0a-a094-4109a3611fe4`  

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

**Status**: FAILED_RESPONSE  
**Trigger**: "Why cant i see my employer contributions?"  
**Session ID**: `node01o72rq2csutt21iw5hk67ddwur1811752090091301672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01e56kddcwy72ha90f7c4lg0v1821752090091302672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
**Session ID**: `node01uubhk9l27d8n7qp9scisg0001831752090091303672b3096-f11c-4e0a-a094-4109a3611fe4`  

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
| FAILED_RESPONSE | 9 | 21.4% |

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
- **Error Rate**: 21.4%

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

**Report Generated**: 2025-07-10 08:11:54
