import os
import subprocess
import sys

# Find and kill process on port 5000
try:
    print("Checking for processes on port 5000...")
    output = subprocess.check_output('netstat -aon', shell=True).decode()
    pids = set()
    for line in output.splitlines():
        if ':5000' in line:
            parts = line.strip().split()
            if len(parts) >= 5:
                pid = parts[-1]
                if pid.isdigit() and pid != '0':
                    pids.add(pid)
    
    for pid in pids:
        print(f"Terminating PID: {pid}")
        os.system(f"taskkill /F /PID {pid}")
except Exception as e:
    print("No process found on port 5000 or error occurred:", e)

# Start app.py
print("Starting CloudQueueX server...")
os.system(f'"{sys.executable}" d:/cloudqueuex-ai/app.py')
