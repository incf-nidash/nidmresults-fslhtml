import subprocess
import os
import shutil
import random
import shlex
import numpy as np
import nibabel as nib
from queries.queryTools import runQuery

def getVal(niftiFilename, minOrMax):
    # Retrieve the min or max values of the image.

    getValString1 = "fslstats '" + niftiFilename + "' -l 0.01 -R"
    if minOrMax == 'min':
        getValString2 = "awk '{print $1}'"
    elif minOrMax == 'max':
        getValString2 = "awk '{print $2}'"
    else:
        error('Please enter "min" or "max"')

    # Process the command to obtain the value
    process_1 = subprocess.Popen(shlex.split(getValString1), shell=False,
                                 stdout=subprocess.PIPE)
    process_2 = subprocess.Popen(shlex.split(getValString2), shell=False,
                                 stdin=process_1.stdout,
                                 stdout=subprocess.PIPE)

    # Close all streams and retrieve output.
    process_1.stdout.close()
    output = process_2.communicate()

    # Return value.
    return(output[0].decode('utf-8').rstrip('\r|\n'))

def getVal2(niftiFilename, minOrMax):
    # Retrieve the min or max values of the image.

    #Retrieve image header.
    n = nib.load(niftiFilename)
    header = n.header
    print(header)
    if minOrMax == 'min':
        return(header['Min'][0])
    else:
        return(0)

print(getVal2('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_default_test/ExcursionSet.nii.gz', 'min'))

