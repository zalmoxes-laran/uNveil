import subprocess
import sys
import os

def install_modules():
    is_windows = sys.platform.startswith('win')
    if is_windows:
        python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
    is_mac = sys.platform.startswith('darwin')
    if is_mac:
        python_exe = os.path.join(sys.prefix, 'bin', 'python3.9')
        python_exe = python_exe.replace(' ', '\\ ')
    is_linux = sys.platform.startswith('linux') # correggere
    if is_windows:
        print("Il sistema è windows")
    print(os.name)

    #print(str(sys.prefix))
    # path to python.exe

    print(str(python_exe))

    list_of_modules =["google-api-python-client", "google-auth-httplib2", "google-auth-oauthlib", "googleapiclient"]

    # upgrade pip
    subprocess.call([python_exe, "-m", "ensurepip"])
    subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

    # install required packages
    #subprocess.call([python_exe, "-m", "pip", "install", "pyzenodo3"])
    #subprocess.call([python_exe, "-m", "pip", "install", "python-telegram-bot"])
    
    for install_module in list_of_modules:
        subprocess.call([python_exe, "-m", "pip", "install", install_module])

if __name__ == '__main__':
    install_modules()
