# http://127.0.0.1:5000

import subprocess
import sys
import time

def run_flask_script(script_name, port):
    process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script_name} executed successfully:\n{result.stdout}")
    else:
        print(f"Error executing {script_name}:\n{result.stderr}")

if __name__ == "__main__":
    # Start the Flask server in the background
    print("Starting uploadFile.py...")
    flask_process_upload = run_flask_script("uploadFile.py", 5000)
    
    # Give the server a few seconds to start up
    time.sleep(5)
    
    # Start the second Flask server in the background
    print("Starting testingGrammarModel.py...")
    flask_process_testing = run_flask_script("testingGrammarModel.py", 5001)
    
    # Wait for the user to terminate the Flask servers
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        flask_process_upload.terminate()
        flask_process_testing.terminate()
        print("Flask servers terminated.")
