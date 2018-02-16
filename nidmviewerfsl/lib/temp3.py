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

    # Retrieve image data.
    n = nib.load(niftiFilename)
    d = n.get_data()

    # Ensure there are no NaN's
    d = np.nan_to_num(d)

    # We are only interested in non-zero values.
    d = d[d.nonzero()]

    if minOrMax == 'min':
        return(d.min())
    else:
        return(d.max())
    
print(getVal('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_default_test/ExcursionSet.nii.gz', 'min'))

print(getVal2('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_default_test/ExcursionSet.nii.gz', 'min'))

print(getVal('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_default_test/ExcursionSet.nii.gz', 'max'))

print(getVal2('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_default_test/ExcursionSet.nii.gz', 'max'))

