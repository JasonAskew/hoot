#!/usr/bin/env python3
"""
CAPI Background Test Runner
Manages background execution of large CAPI test suites with multiple strategies.
"""

import os
import sys
import subprocess
import argparse
import json
import time
import signal
from datetime import datetime
from typing import Optional, Dict, List
import psutil

class BackgroundTestRunner:
    """Manages background execution of CAPI tests."""
    
    def __init__(self):
        self.pid_file = "capi_test_runner.pid"
        self.status_file = "capi_test_status.json"
        self.log_file = f"capi_background_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def save_status(self, status: Dict):
        """Save current execution status."""
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
    
    def load_status(self) -> Optional[Dict]:
        """Load execution status."""
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_pid(self, pid: int):
        """Save process ID for monitoring."""
        with open(self.pid_file, 'w') as f:
            f.write(str(pid))
    
    def load_pid(self) -> Optional[int]:
        """Load saved process ID."""
        if os.path.exists(self.pid_file):
            try:
                with open(self.pid_file, 'r') as f:
                    return int(f.read().strip())
            except:
                pass
        return None
    
    def is_process_running(self, pid: int) -> bool:
        """Check if a process is running."""
        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False
    
    def run_with_nohup(self, test_file: str, batch_size: Optional[int] = None):
        """Run tests using nohup for background execution."""
        print(f"Starting background test execution with nohup...")
        print(f"Test file: {test_file}")
        print(f"Log file: {self.log_file}")
        
        # Build command
        cmd = ["nohup", sys.executable, "capi_test_runner.py", "--test-file", test_file]
        
        # Start process
        with open(self.log_file, 'w') as log:
            process = subprocess.Popen(
                cmd,
                stdout=log,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid,  # Create new session
                start_new_session=True
            )
        
        # Save process info
        self.save_pid(process.pid)
        self.save_status({
            "method": "nohup",
            "pid": process.pid,
            "test_file": test_file,
            "batch_size": batch_size,
            "start_time": datetime.now().isoformat(),
            "log_file": self.log_file,
            "status": "running"
        })
        
        print(f"Background process started with PID: {process.pid}")
        print(f"Monitor progress with: python capi_test_monitor.py")
        print(f"View logs with: tail -f {self.log_file}")
        
        return process.pid
    
    def run_with_screen(self, test_file: str, batch_size: Optional[int] = None):
        """Run tests using GNU screen for background execution."""
        session_name = f"capi_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Starting background test execution with screen...")
        print(f"Session name: {session_name}")
        print(f"Test file: {test_file}")
        
        # Build command
        cmd = [
            "screen", "-dmS", session_name,
            sys.executable, "capi_test_runner.py", "--test-file", test_file
        ]
        
        # Start screen session
        subprocess.run(cmd, check=True)
        
        # Get screen PID
        time.sleep(1)  # Give screen time to start
        ps_output = subprocess.check_output(["screen", "-ls"]).decode()
        
        # Extract PID from screen output
        pid = None
        for line in ps_output.split('\n'):
            if session_name in line:
                # Extract PID from format: "12345.session_name"
                pid = int(line.strip().split('.')[0].split()[0])
                break
        
        if pid:
            self.save_pid(pid)
            self.save_status({
                "method": "screen",
                "pid": pid,
                "session_name": session_name,
                "test_file": test_file,
                "batch_size": batch_size,
                "start_time": datetime.now().isoformat(),
                "status": "running"
            })
            
            print(f"Screen session started: {session_name}")
            print(f"Attach to session with: screen -r {session_name}")
            print(f"Detach with: Ctrl+A, D")
            print(f"Monitor progress with: python capi_test_monitor.py")
        else:
            print("Warning: Could not determine screen session PID")
        
        return pid
    
    def run_with_tmux(self, test_file: str, batch_size: Optional[int] = None):
        """Run tests using tmux for background execution."""
        session_name = f"capi_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Starting background test execution with tmux...")
        print(f"Session name: {session_name}")
        print(f"Test file: {test_file}")
        
        # Build command
        cmd = [
            "tmux", "new-session", "-d", "-s", session_name,
            sys.executable, "capi_test_runner.py", "--test-file", test_file
        ]
        
        # Start tmux session
        subprocess.run(cmd, check=True)
        
        # Get tmux PID
        time.sleep(1)
        try:
            pid_output = subprocess.check_output(
                ["tmux", "list-panes", "-t", session_name, "-F", "#{pane_pid}"]
            ).decode().strip()
            pid = int(pid_output)
            
            self.save_pid(pid)
            self.save_status({
                "method": "tmux",
                "pid": pid,
                "session_name": session_name,
                "test_file": test_file,
                "batch_size": batch_size,
                "start_time": datetime.now().isoformat(),
                "status": "running"
            })
            
            print(f"Tmux session started: {session_name}")
            print(f"Attach to session with: tmux attach -t {session_name}")
            print(f"Detach with: Ctrl+B, D")
            print(f"Monitor progress with: python capi_test_monitor.py")
            
            return pid
        except subprocess.CalledProcessError:
            print("Warning: Could not determine tmux session PID")
            return None
    
    def run_batch_mode(self, test_file: str, batch_size: int = 100, parallel: int = 1):
        """Run tests in batch mode with optional parallelization."""
        print(f"Starting batch test execution...")
        print(f"Test file: {test_file}")
        print(f"Batch size: {batch_size}")
        print(f"Parallel workers: {parallel}")
        
        # Count total tests
        with open(test_file, 'r') as f:
            total_tests = sum(1 for line in f) - 1  # Subtract header
        
        print(f"Total tests to run: {total_tests}")
        
        # Calculate batches
        num_batches = (total_tests + batch_size - 1) // batch_size
        print(f"Number of batches: {num_batches}")
        
        # Create batch runner script
        batch_script = f"""#!/usr/bin/env python3
import subprocess
import time
import json
from datetime import datetime
import concurrent.futures

def run_batch(batch_num, start_idx, end_idx):
    log_file = "capi_batch_{{:04d}}.log".format(batch_num)
    cmd = [
        "{sys.executable}", "capi_batch_processor.py",
        "--test-file", "{test_file}",
        "--start", str(start_idx),
        "--end", str(end_idx),
        "--batch-num", str(batch_num),
        "--log-file", log_file
    ]
    
    print("Starting batch {{}}: tests {{}}-{{}}".format(batch_num, start_idx, end_idx))
    start_time = time.time()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    duration = time.time() - start_time
    print("Batch {{}} completed in {{:.1f}}s".format(batch_num, duration))
    
    return {{
        "batch_num": batch_num,
        "start_idx": start_idx,
        "end_idx": end_idx,
        "duration": duration,
        "success": result.returncode == 0,
        "log_file": log_file
    }}

# Main execution
batches = []
for i in range({num_batches}):
    start_idx = i * {batch_size}
    end_idx = min((i + 1) * {batch_size}, {total_tests})
    batches.append((i + 1, start_idx, end_idx))

print("Running {{}} batches with {parallel} parallel workers...".format(len(batches)))

with concurrent.futures.ProcessPoolExecutor(max_workers={parallel}) as executor:
    futures = [executor.submit(run_batch, *batch) for batch in batches]
    
    results = []
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        results.append(result)
        
        # Update status
        completed = len(results)
        print("Progress: {{}}/{{}} batches completed".format(completed, len(batches)))

# Save final results
with open("batch_execution_results.json", "w") as f:
    json.dump({{
        "total_batches": len(batches),
        "completed_batches": len(results),
        "results": results,
        "timestamp": datetime.now().isoformat()
    }}, f, indent=2)

print("Batch execution completed!")
"""
        
        # Save batch runner script
        batch_runner_file = "capi_batch_runner_temp.py"
        with open(batch_runner_file, 'w') as f:
            f.write(batch_script)
        
        os.chmod(batch_runner_file, 0o755)
        
        # Run batch runner in background
        with open(self.log_file, 'w') as log:
            process = subprocess.Popen(
                [sys.executable, batch_runner_file],
                stdout=log,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid
            )
        
        self.save_pid(process.pid)
        self.save_status({
            "method": "batch",
            "pid": process.pid,
            "test_file": test_file,
            "batch_size": batch_size,
            "parallel_workers": parallel,
            "total_tests": total_tests,
            "num_batches": num_batches,
            "start_time": datetime.now().isoformat(),
            "log_file": self.log_file,
            "status": "running"
        })
        
        print(f"Batch runner started with PID: {process.pid}")
        print(f"Monitor progress with: python capi_test_monitor.py")
        print(f"View logs with: tail -f {self.log_file}")
        
        return process.pid
    
    def stop(self):
        """Stop running background tests."""
        pid = self.load_pid()
        if not pid:
            print("No running test process found")
            return
        
        if not self.is_process_running(pid):
            print(f"Process {pid} is not running")
            # Clean up
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            return
        
        print(f"Stopping process {pid}...")
        
        try:
            # Try graceful shutdown first
            os.kill(pid, signal.SIGTERM)
            time.sleep(5)
            
            # Check if still running
            if self.is_process_running(pid):
                print("Process didn't stop gracefully, forcing...")
                os.kill(pid, signal.SIGKILL)
            
            print("Process stopped")
            
            # Update status
            status = self.load_status()
            if status:
                status["status"] = "stopped"
                status["stop_time"] = datetime.now().isoformat()
                self.save_status(status)
            
            # Clean up PID file
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
                
        except ProcessLookupError:
            print("Process already stopped")
        except Exception as e:
            print(f"Error stopping process: {e}")


def main():
    parser = argparse.ArgumentParser(description='Run CAPI tests in background')
    parser.add_argument('--method', choices=['nohup', 'screen', 'tmux', 'batch'], 
                        default='nohup', help='Background execution method')
    parser.add_argument('--test-file', required=True, help='CSV file with test cases')
    parser.add_argument('--batch-size', type=int, default=100, 
                        help='Number of tests per batch (for batch mode)')
    parser.add_argument('--parallel', type=int, default=1,
                        help='Number of parallel workers (for batch mode)')
    parser.add_argument('--stop', action='store_true', help='Stop running tests')
    
    args = parser.parse_args()
    
    runner = BackgroundTestRunner()
    
    if args.stop:
        runner.stop()
        return
    
    # Check if tests are already running
    pid = runner.load_pid()
    if pid and runner.is_process_running(pid):
        print(f"Tests are already running (PID: {pid})")
        print("Use --stop to stop them or monitor with: python capi_test_monitor.py")
        return
    
    # Verify test file exists
    if not os.path.exists(args.test_file):
        print(f"Error: Test file not found: {args.test_file}")
        sys.exit(1)
    
    # Run tests based on method
    if args.method == 'nohup':
        runner.run_with_nohup(args.test_file, args.batch_size)
    elif args.method == 'screen':
        runner.run_with_screen(args.test_file, args.batch_size)
    elif args.method == 'tmux':
        runner.run_with_tmux(args.test_file, args.batch_size)
    elif args.method == 'batch':
        runner.run_batch_mode(args.test_file, args.batch_size, args.parallel)


if __name__ == "__main__":
    # Install psutil if not available
    try:
        import psutil
    except ImportError:
        print("Installing required dependency: psutil")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    
    main()