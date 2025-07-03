# Test Generation - Current Setup

## Latest Generated Files (2025-07-03)
- `consolidated_tests_capi_20250703_125743.csv` - All CAPI tests (3,631 tests)
- `consolidated_tests_hoot_20250703_125743.csv` - All HOOT tests (19,345 rows)  
- `test_generation_report_20250703_125743.md` - Generation report

## Active Python Files

### Main Generator
- `consolidated_test_generator.py` - **Main generator** combining all test types

### Supporting Generators (used by consolidated generator)
- `conversation_flow_test_generator.py` - Multi-turn conversation flows
- `intent_navigation_test_generator.py` - Intent navigation through buttons/quick replies
- `generate_matrix_with_segment_matching.py` - Matrix tests with segment validation
- `segment_intent_validator.py` - Validates intent/segment combinations

### Utility Scripts
- `generate_matrix_from_files.py` - Basic matrix generation
- `generate_profiles_from_segments.py` - Profile generation utilities
- `kg_loader_complete.py` - Knowledge graph utilities
- `kg_verification.py` - Verification utilities
- `sample_intent_data_loader.py` - Intent data loading

## How to Generate Tests

### Generate All Tests (Recommended)
```bash
python consolidated_test_generator.py
```
This generates both CAPI and HOOT formats with datetime in filenames.

### Generate Specific Format Only
```bash
# CAPI format only
python consolidated_test_generator.py --capi

# HOOT format only  
python consolidated_test_generator.py --hoot
```

## Test Types Generated

1. **Matrix Tests** (Breadth) - Standard intent/segment combinations
2. **Conversation Flow Tests** (Depth) - Multi-turn conversations with clarification responses
3. **Intent Navigation Tests** (Depth) - Intent-to-intent navigation through buttons

## Cleanup History

**2025-07-03 13:02:58** - Moved 78 old/redundant files to `backup/cleanup_20250703_130258/`
- Old test outputs (CSV, JSON, logs)
- Redundant generators and runners
- Old documentation and reports
- Temporary files

## Key Directories
- `intents/` - Intent definitions
- `responses/` - Response definitions  
- `entities/` - Entity definitions
- `profiles/` - User profiles
- `intent_data/` - Intent training data
- `backup/` - Historical files and backups