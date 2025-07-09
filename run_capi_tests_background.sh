#!/bin/bash
#
# CAPI Background Test Runner
# Convenient script to run CAPI tests in background with various strategies
#

# Default values
TEST_FILE="consolidated_tests_capi_20250709_095005.csv"
METHOD="nohup"
BATCH_SIZE=100
PARALLEL=1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -f, --file FILE      Test CSV file (default: $TEST_FILE)"
    echo "  -m, --method METHOD  Execution method: nohup, screen, tmux, batch (default: nohup)"
    echo "  -b, --batch SIZE     Batch size for batch mode (default: 100)"
    echo "  -p, --parallel N     Number of parallel workers for batch mode (default: 1)"
    echo "  -s, --stop           Stop running tests"
    echo "  -M, --monitor        Start monitoring after launching tests"
    echo "  -h, --help           Display this help message"
    echo ""
    echo "Examples:"
    echo "  # Run with nohup (simple background execution)"
    echo "  $0"
    echo ""
    echo "  # Run with screen (attachable terminal)"
    echo "  $0 --method screen"
    echo ""
    echo "  # Run in batch mode with 4 parallel workers"
    echo "  $0 --method batch --parallel 4 --batch 50"
    echo ""
    echo "  # Monitor running tests"
    echo "  python3 capi_test_monitor.py"
}

# Parse command line arguments
MONITOR_AFTER=false
STOP_TESTS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--file)
            TEST_FILE="$2"
            shift 2
            ;;
        -m|--method)
            METHOD="$2"
            shift 2
            ;;
        -b|--batch)
            BATCH_SIZE="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL="$2"
            shift 2
            ;;
        -s|--stop)
            STOP_TESTS=true
            shift
            ;;
        -M|--monitor)
            MONITOR_AFTER=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Stop tests if requested
if [ "$STOP_TESTS" = true ]; then
    echo -e "${YELLOW}Stopping CAPI tests...${NC}"
    python3 capi_background_runner.py --stop
    exit $?
fi

# Check if test file exists
if [ ! -f "$TEST_FILE" ]; then
    echo -e "${RED}Error: Test file not found: $TEST_FILE${NC}"
    exit 1
fi

# Count total tests
TOTAL_TESTS=$(tail -n +2 "$TEST_FILE" | wc -l)
echo -e "${GREEN}Test file: $TEST_FILE${NC}"
echo -e "${GREEN}Total tests: $TOTAL_TESTS${NC}"

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import psutil" 2>/dev/null || {
    echo "Installing psutil..."
    pip3 install psutil
}

# Recommendations based on test count
if [ $TOTAL_TESTS -gt 1000 ]; then
    echo ""
    echo -e "${YELLOW}Recommendation: With $TOTAL_TESTS tests, consider using:${NC}"
    echo "  - Batch mode with parallel execution for fastest results"
    echo "  - Screen/tmux for ability to check progress interactively"
    echo ""
fi

# Check if tests are already running
if [ -f "capi_test_runner.pid" ]; then
    PID=$(cat capi_test_runner.pid)
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Warning: Tests are already running (PID: $PID)${NC}"
        echo "Use '$0 --stop' to stop them or 'python3 capi_test_monitor.py' to monitor"
        exit 1
    fi
fi

# Run based on method
echo -e "${GREEN}Starting CAPI tests with method: $METHOD${NC}"

case $METHOD in
    nohup)
        echo "Running with nohup (simple background execution)..."
        python3 capi_background_runner.py --method nohup --test-file "$TEST_FILE"
        ;;
    screen)
        # Check if screen is installed
        if ! command -v screen &> /dev/null; then
            echo -e "${RED}Error: GNU screen is not installed${NC}"
            echo "Install with: brew install screen (macOS) or apt-get install screen (Linux)"
            exit 1
        fi
        echo "Running with screen (attachable terminal)..."
        python3 capi_background_runner.py --method screen --test-file "$TEST_FILE"
        ;;
    tmux)
        # Check if tmux is installed
        if ! command -v tmux &> /dev/null; then
            echo -e "${RED}Error: tmux is not installed${NC}"
            echo "Install with: brew install tmux (macOS) or apt-get install tmux (Linux)"
            exit 1
        fi
        echo "Running with tmux (modern terminal multiplexer)..."
        python3 capi_background_runner.py --method tmux --test-file "$TEST_FILE"
        ;;
    batch)
        echo "Running in batch mode..."
        echo "  Batch size: $BATCH_SIZE"
        echo "  Parallel workers: $PARALLEL"
        python3 capi_background_runner.py --method batch --test-file "$TEST_FILE" \
            --batch-size "$BATCH_SIZE" --parallel "$PARALLEL"
        ;;
    *)
        echo -e "${RED}Error: Unknown method: $METHOD${NC}"
        usage
        exit 1
        ;;
esac

# Check if launch was successful
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}Tests started successfully!${NC}"
    echo ""
    echo "Monitor progress with:"
    echo "  python3 capi_test_monitor.py"
    echo ""
    echo "View logs with:"
    echo "  tail -f capi_background_*.log"
    echo ""
    echo "Stop tests with:"
    echo "  $0 --stop"
    
    # Start monitoring if requested
    if [ "$MONITOR_AFTER" = true ]; then
        echo ""
        echo "Starting monitor in 3 seconds..."
        sleep 3
        python3 capi_test_monitor.py
    fi
else
    echo -e "${RED}Failed to start tests${NC}"
    exit 1
fi