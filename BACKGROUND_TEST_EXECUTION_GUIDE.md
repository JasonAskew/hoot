# CAPI Background Test Execution Guide

This guide explains how to run large CAPI test suites in the background without timeout issues.

## Overview

The background test execution system provides multiple strategies for running thousands of tests:

1. **Nohup Mode** - Simple background execution
2. **Screen Mode** - Attachable terminal sessions
3. **Tmux Mode** - Modern terminal multiplexer
4. **Batch Mode** - Parallel execution of test batches

## Quick Start

### Simple Background Execution

```bash
# Run all tests in background using nohup
./run_capi_tests_background.sh

# Monitor progress
python3 capi_test_monitor.py
```

### Parallel Batch Execution (Recommended for Large Test Suites)

```bash
# Run tests in batches with 4 parallel workers
./run_capi_tests_background.sh --method batch --parallel 4 --batch 100

# Monitor batch progress
python3 capi_test_monitor.py
```

## Components

### 1. Background Runner (`capi_background_runner.py`)

Main orchestrator that manages different execution strategies:

```bash
# Run with nohup
python3 capi_background_runner.py --method nohup --test-file consolidated_tests_capi_20250709_095005.csv

# Run with screen
python3 capi_background_runner.py --method screen --test-file consolidated_tests_capi_20250709_095005.csv

# Run in batch mode with parallelization
python3 capi_background_runner.py --method batch --test-file consolidated_tests_capi_20250709_095005.csv --batch-size 100 --parallel 4

# Stop running tests
python3 capi_background_runner.py --stop
```

### 2. Batch Processor (`capi_batch_processor.py`)

Processes specific ranges of tests (used internally by batch mode):

```bash
# Process tests 0-100
python3 capi_batch_processor.py --test-file tests.csv --start 0 --end 100 --batch-num 1
```

### 3. Test Monitor (`capi_test_monitor.py`)

Real-time monitoring of test execution:

```bash
# Start monitoring (auto-detects execution mode)
python3 capi_test_monitor.py

# Custom refresh interval
python3 capi_test_monitor.py --interval 10

# Generate summary report
python3 capi_test_monitor.py --summary
```

### 4. Results Aggregator (`capi_results_aggregator.py`)

Combines results from multiple batch executions:

```bash
# Aggregate all results
python3 capi_results_aggregator.py

# Custom output files
python3 capi_results_aggregator.py --output-csv final_results.csv --output-report summary.txt
```

## Execution Strategies

### Nohup Mode
- **Pros**: Simple, no dependencies, survives terminal disconnect
- **Cons**: No interactive access, basic logging only
- **Best for**: Overnight runs, simple deployments

```bash
./run_capi_tests_background.sh --method nohup
```

### Screen Mode
- **Pros**: Can attach/detach from session, see real-time output
- **Cons**: Requires GNU screen installation
- **Best for**: Interactive monitoring, debugging

```bash
./run_capi_tests_background.sh --method screen

# Attach to session
screen -r capi_test_TIMESTAMP

# Detach: Press Ctrl+A, then D
```

### Tmux Mode
- **Pros**: Modern, feature-rich, better than screen
- **Cons**: Requires tmux installation
- **Best for**: Power users, complex workflows

```bash
./run_capi_tests_background.sh --method tmux

# Attach to session
tmux attach -t capi_test_TIMESTAMP

# Detach: Press Ctrl+B, then D
```

### Batch Mode (Recommended for Large Test Suites)
- **Pros**: Parallel execution, fault tolerance, resumable
- **Cons**: More complex, multiple log files
- **Best for**: Large test suites (>1000 tests)

```bash
# Run with 8 parallel workers, 50 tests per batch
./run_capi_tests_background.sh --method batch --parallel 8 --batch 50
```

## Monitoring and Progress Tracking

### Real-time Monitoring

The monitor provides live updates on:
- Tests completed
- Success rate
- Estimated time remaining
- Current test being executed

```bash
python3 capi_test_monitor.py
```

Monitor display example:
```
================================================================================
                        CAPI Test Execution Monitor                        
================================================================================

Execution Method: batch
Test File: consolidated_tests_capi_20250709_095005.csv
Process ID: 12345
Status: RUNNING
Started: 2025-07-09T10:30:00
Elapsed: 45.3m

Tests Completed: 2,456 / 4,180
Progress: [########################------------] 58.8%
Rate: 0.9 tests/second
ETA: 31.9m

Last Update: 2025-07-09T11:15:23

Log File: capi_background_20250709_103000.log
View logs: tail -f capi_background_20250709_103000.log
```

### Log Files

Different log files are created based on execution method:

- **Nohup**: `capi_background_TIMESTAMP.log`
- **Batch Mode**: 
  - Main log: `capi_background_TIMESTAMP.log`
  - Batch logs: `batch_0001.log`, `batch_0002.log`, etc.

View logs in real-time:
```bash
# Main log
tail -f capi_background_*.log

# Specific batch log
tail -f batch_0001.log

# All batch logs
tail -f batch_*.log
```

## Handling Failures and Resumption

### Automatic Checkpointing

The system automatically saves progress:
- Standard mode: Every 10 tests
- Batch mode: Every 5 tests per batch

### Resume After Failure

If execution is interrupted:

1. **Standard Mode**: Will automatically resume from checkpoint
   ```bash
   ./run_capi_tests_background.sh
   ```

2. **Batch Mode**: Failed batches can be re-run
   ```bash
   # Check batch status
   ls batch_status_*.json
   
   # Re-run specific batch if needed
   python3 capi_batch_processor.py --test-file tests.csv --start 1000 --end 1100 --batch-num 11
   ```

## Results Management

### Aggregate Results

After batch execution, combine all results:

```bash
# Aggregate results
python3 capi_results_aggregator.py

# This creates:
# - aggregated_results_TIMESTAMP.json (full data)
# - aggregated_results_TIMESTAMP.csv (for analysis)
# - test_summary_report_TIMESTAMP.txt (summary)
```

### Clean Up

After successful completion:

```bash
# Remove batch files (keep aggregated results)
rm batch_status_*.json
rm batch_results_*.json
rm batch_checkpoint_*.json
rm batch_*.log

# Remove checkpoint files
rm test_checkpoint.json
rm capi_test_runner.pid
```

## Best Practices

1. **For Small Test Suites (<500 tests)**
   - Use nohup mode for simplicity
   - Single process is sufficient

2. **For Medium Test Suites (500-2000 tests)**
   - Use screen/tmux for ability to monitor
   - Consider batch mode with 2-4 workers

3. **For Large Test Suites (>2000 tests)**
   - Use batch mode with parallel execution
   - Start with workers = CPU cores / 2
   - Batch size 50-100 tests

4. **Network Considerations**
   - Add delays between API calls (already included)
   - Monitor for rate limiting
   - Use smaller batch sizes if seeing timeouts

5. **Resource Management**
   - Each worker uses ~100-200MB RAM
   - Monitor system resources with `htop` or `top`
   - Reduce parallel workers if system is constrained

## Troubleshooting

### Tests Won't Start
```bash
# Check if already running
ps aux | grep capi_test_runner

# Force stop and cleanup
./run_capi_tests_background.sh --stop
rm capi_test_runner.pid
```

### High Failure Rate
- Reduce parallel workers (API rate limiting)
- Increase delay between tests
- Check API credentials and endpoints

### Out of Memory
- Reduce batch size
- Reduce parallel workers
- Use standard mode instead of batch mode

### Can't Find Results
```bash
# List all result files
ls test_results_*.json
ls batch_results_*.json

# Aggregate any found results
python3 capi_results_aggregator.py
```

## Example Workflows

### Production Test Run
```bash
# 1. Start tests in batch mode
./run_capi_tests_background.sh --method batch --parallel 6 --batch 75 --monitor

# 2. Monitor completes automatically, aggregate results
python3 capi_results_aggregator.py

# 3. Review summary
cat test_summary_report_*.txt
```

### Debug Test Run
```bash
# 1. Start with screen for interactive access
./run_capi_tests_background.sh --method screen --file debug_tests.csv

# 2. Attach to watch execution
screen -r capi_test_*

# 3. Detach and let it run
# Press Ctrl+A, then D
```

### Overnight Test Run
```bash
# 1. Start with nohup
nohup ./run_capi_tests_background.sh --method batch --parallel 4 &

# 2. Check progress next day
python3 capi_test_monitor.py --summary

# 3. Aggregate results
python3 capi_results_aggregator.py
```

## Performance Expectations

Based on the system configuration:

- **Single Process**: ~0.5-1 test/second (including API delays)
- **Batch Mode (4 workers)**: ~2-4 tests/second
- **Batch Mode (8 workers)**: ~4-8 tests/second

For 4,180 tests:
- Single process: ~2-4 hours
- 4 parallel workers: ~30-60 minutes
- 8 parallel workers: ~15-30 minutes

Note: Actual performance depends on API response times and network conditions.