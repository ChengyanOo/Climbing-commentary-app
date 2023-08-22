import subprocess
from subprocess import Popen
import os
import time
import signal

cv_python_script_path = '/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/cv/MovementTracking.py'
activate_and_run_python_script_command = f'source /Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/cv/movement_track_system_venv/bin/activate && python3 {cv_python_script_path}'
cv_process = subprocess.Popen(activate_and_run_python_script_command, shell=True, executable='/bin/bash')

express_server_frames_path = '/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/express_server/frames'
subprocess.run('rm *.jpg', shell=True, cwd=express_server_frames_path)

express_server_path = '/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/express_server'
express_process = Popen(['npm', 'start'], cwd=express_server_path)

react_app_path = '/Users/tonsonwang/Desktop/Climbing-commentary-app/Commentary/react_frontend/igu'
react_process = Popen(['npm', 'start'], cwd=react_app_path)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    os.killpg(os.getpgid(cv_process.pid), signal.SIGTERM)
    express_process.terminate()
    react_process.terminate()
    print("Terminated the processes.")