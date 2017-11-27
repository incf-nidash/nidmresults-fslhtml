import subprocess
import os
subprocess.call(['easy_install', 'Pillow'])
subprocess.call(['python', 'setup.py', 'install'])
curdir = os.getcwd()
os.chdir('C:\\Users\\owner\\Downloads')
subprocess.call(['pip', 'install', 'Pillow-3.4.2-cp36-cp36m-win32.whl'])
os.chdir(curdir)
