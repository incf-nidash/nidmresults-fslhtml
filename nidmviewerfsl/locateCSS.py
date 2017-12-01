import subprocess
import os
import shutil
import random

#Obtain the FSL directory.
def obtainFSLdir():
    
    fsldirCommand = "echo $FSLDIR"
    process = subprocess.Popen(fsldirCommand, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()
    return(output[0].decode('utf-8').rstrip('\r|\n'))

def cssStyleSheet():

    cssStyleSheet = os.path.join(obtainFSLdir(), 'doc', 'fsl.css')
    print('active')
    return(cssStyleSheet)
