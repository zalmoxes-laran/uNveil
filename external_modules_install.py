import subprocess
import sys
import os

print(str(sys.prefix))
# path to python.exe
#python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
python_exe = os.path.join(sys.prefix, 'bin', 'python3.9')
print(str(python_exe))
# upgrade pip
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# install required packages
#subprocess.call([python_exe, "-m", "pip", "install", "pyzenodo3"])
subprocess.call([python_exe, "-m", "pip", "install", "python-telegram-bot"])
subprocess.call([python_exe, "-m", "pip", "install", "exchange"])

import bpy, os
import sys

is_windows = sys.platform.startswith('win')
if is_windows:
    print("Il sistema è windows")
print(os.name)