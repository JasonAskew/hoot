# CAPI Test Runner Version Comparison

## Overview
This document compares the current `capi_test_runner.py` with the backup version from `backup/cleanup_20250703_130258/capi_test_runner.py`.

## Key Differences

### 1. API Endpoints and URLs

| Aspect | Current Version (btfin.com) | Backup Version (Westpac/Kasisto) |
|--------|----------------------------|----------------------------------|
| Base URL | `https://capi-uat.btfin.com/conversational-api/chat` | `https://westpac-kai-sandbox-en-au-stage.kitsys.net` |
| Endpoints | Single endpoint for chat | Two endpoints: `/kai/api/v2/capi/event` (START_SESSION) and `/kai/api/v2/capi/user_message` |
| API Version | Not specified | v5.8 |

### 2. Authentication Mechanisms

| Aspect | Current Version | Backup Version |
|--------|----------------|----------------|
| Auth Type | API Key Header | Basic Auth + Secret |
| API Key | `x-api-key: x9XaQNmJJtZtV8drJHGHIhPDTSlbnB` | N/A |
| Basic Auth | N/A | `Basic c3lzY3VzOjIzM2hfYWRqS0pzYWU4Mw==` |
| Secret | N/A | `670b7c4a-3091-4d6f-b02e-c16d9c911428` |
| Assistant Info | N/A | `assistant_name: default_assistant`, `assistant_target: prod` |

### 3. Request/Response Formats

#### Current Version (Simple Format)
```python
payload = {
    "query": user_input,
    "metadata": {
        "profile": test.get('segment', 'default')
    }
}
```

#### Backup Version (Complex Format)
```python
payload = {
    "context": {
        "device": {
            "os": "Mac OS - 10.15.7",
            "model": "Chrome - 137.0.0.0",
            "type": "web",
            "id": ""
        },
        "platform": {
            "name": platform_name,
            "conversation_id": "",
            "session_id": session_id,
            "version": "3.5.0-RC.5 - build 6",
            "user_id": "5ece450782c937c6db19de093f2e4fb8"
        },
        "user": {
            "meta_fields": meta_fields,
            "time_zone": "America/New_York",
            "session_id": session_id,
            "locale": "en_AU"
        },
        "api_version": "5.8",
        "features": {
            "allowed": ["nlu_details"]
        }
    },
    "type": "TEXT",
    "payload": {
        "text": message_text
    }
}
```

### 4. Overall Structure and Logic

| Feature | Current Version | Backup Version |
|---------|----------------|----------------|
| Session Management | Simple, no explicit session creation | Two-step: START_SESSION then USER_MESSAGE |
| Test Formats | Standard CSV only | Standard CSV + "Hoot" format |
| Checkpoint/Resume | No | Yes, with automatic checkpointing |
| Profile Loading | No | Yes, loads JSON profile metadata |
| Response Validation | Basic text/button matching | Advanced JSON path validation |
| Reporting | Basic results JSON | Detailed markdown reports + failure analysis |
| Error Handling | Basic | Advanced with checkpoint recovery |

### 5. Test Data Format Support

#### Current Version
- Single CSV format: `consolidated_tests_capi_20250703_125743.csv`
- Basic fields: intent, segment, example_trigger, expected_response

#### Backup Version
- Standard format: `segment_intent_matrix_with_matching_full.csv`
- Hoot format: `hoot_tests_full.csv` with JSON path validation
- Profile metadata from JSON files in `profiles/` directory

### 6. Response Processing

| Feature | Current Version | Backup Version |
|---------|----------------|----------------|
| Intent Extraction | Simple metadata.intent.name | Complex nlu_details parsing |
| Segment Validation | Basic profile check | Segment names list validation |
| Text Comparison | Basic normalization | Advanced normalization with similarity scoring |
| Button Extraction | Quick replies + button payloads | Quick replies + message_contents buttons |

## Environment Determination

### Current Version (btfin.com)
- **Purpose**: Appears to be a simplified testing environment
- **Use Case**: Basic conversational API testing
- **Complexity**: Lower, suitable for quick tests
- **Features**: Minimal, focused on core functionality

### Backup Version (Westpac/Kasisto)
- **Purpose**: Enterprise-grade testing for Westpac KAI platform
- **Use Case**: Comprehensive testing with profile-based personalization
- **Complexity**: High, with advanced features
- **Features**: 
  - Profile metadata injection
  - Session persistence
  - Resumable execution
  - Detailed reporting
  - Multiple test formats

## Recommendations

1. **For btfin.com Testing**: Use the current version
   - Simpler and more appropriate for the btfin.com API
   - Less overhead for basic testing needs

2. **For Westpac/Kasisto Testing**: Use the backup version
   - Required for the complex authentication and session management
   - Needed for profile-based testing
   - Better error recovery and reporting

3. **Environment Clues**:
   - URLs clearly indicate which environment each is for
   - Authentication methods are environment-specific
   - The backup version's complexity suggests enterprise use

## Conclusion

The two versions serve different purposes:
- **Current version**: Simplified tester for btfin.com CAPI
- **Backup version**: Enterprise tester for Westpac KAI Sandbox

Choose based on your target environment and testing requirements.