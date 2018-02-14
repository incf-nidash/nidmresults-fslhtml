import subprocess
import os
import shutil
import random
import shlex


def nifDim(niftiFilename, k):
    # Retrieve the k dimension of a nifti given it's filename using FSL.

    if k == 'x':
        arg = 'dim1'
    elif k == 'y':
        arg = 'dim2'
    elif k == 'z':
        arg = 'dim3'
    elif k == 'pix':
        arg = 'pixdim1'
    else:
        error('Enter a valid dimension... x, y, z or pix')

    # Make the commands
    getDimString1 = ["fslhd", niftiFilename]
    getDimString2 = ["cat", "-v"]
    getDimString3 = ["grep", "^" + arg]

    # Run the command
    process_1 = subprocess.Popen(getDimString1, shell=False,
                                 stdout=subprocess.PIPE)
    process_2 = subprocess.Popen(getDimString2, shell=False,
                                 stdin=process_1.stdout,
                                 stdout=subprocess.PIPE)
    process_3 = subprocess.Popen(getDimString3, shell=False,
                                 stdin=process_2.stdout,
                                 stdout=subprocess.PIPE)

    # Close all streams and retreive output.
    process_1.stdout.close()
    process_2.stdout.close()
    output = process_3.communicate()

    dimension = int(float(output[0].decode('utf-8').rstrip(
        '\r|\n').replace(arg, '').replace(' ', '')))

    return(dimension)

print(nifDim('ExcursionSet.nii.gz', 'pix'))
