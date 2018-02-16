import subprocess
import os
import shutil
import random
import shlex
import numpy as np
import nibabel as nib
from queries.queryTools import runQuery


def nifDim(nifti, k):
    # Retrieve the k dimension of a nifti given it's header using FSL.

    #Retrieve image header.
    n = nib.load(nifti)
    header = n.header
    
    if k == 'x':
        dimension = header['dim'][1]
    elif k == 'y':
        dimension = header['dim'][2]
    elif k == 'z':
        dimension = header['dim'][3]
    elif k == 'pix':
        dimension = header['pixdim'][1]
    else:
        error('Enter a valid dimension... x, y, z or pix')

    return(dimension)

def createResizeMatrix(niftiFilename1, niftiFilename2, tempDir):
    # This creates the resize matrix for the resizing of the niftis and saves
    # it as resizeMatrix.mat

    xShift = -abs(nifDim(niftiFilename1, 'x') - nifDim(niftiFilename2, 'x'))
    yShift = -abs(nifDim(niftiFilename1, 'y') - nifDim(niftiFilename2, 'y'))

    # Open the matrix file.
    matrixFile = open(os.path.join(tempDir, 'resizeMatrix.mat'), 'w')

    # Write the matrix file
    matrixFile.write('1 0 0 ' + str(xShift) + ' \n')
    matrixFile.write('0 1 0 ' + str(yShift) + ' \n')
    matrixFile.write('0 0 1 0 \n')
    matrixFile.write('0 0 0 1 \n')

    # Close the matrix file.
    matrixFile.close()


def resizeTemplateToExcSet(exc_set, template, tempDir):
    # This function resizes an SPM excursion set to a FSL template if
    # necessary, assuming the volume of the brain in both the template and
    # excursion set are the same and they are correctly aligned.

    # Create necessary tranformation.
    createResizeMatrix(exc_set, template, tempDir)

    if nifDim(exc_set, 'x') > nifDim(template, 'x'):
        # Run the command  if necessary.
        resizeCommand = "flirt -init " + \
                        os.path.join(tempDir, "resizeMatrix.mat") + \
                        " -in " + exc_set + " -ref " + template + " -out " + \
                        os.path.join(tempDir, "resizedNifti.nii.gz") + " -applyxfm"

    if nifDim(exc_set, 'x') < nifDim(template, 'x'):
        # Run the command  if necessary.
        resizeCommand = "flirt -init " + \
                        os.path.join(tempDir, "resizeMatrix.mat") + \
                        " -in " + template + " -ref " + exc_set + " -out " + \
                        os.path.join(tempDir, "resizedNifti.nii.gz") + " -applyxfm"

    subprocess.check_call(shlex.split(resizeCommand), shell=False)
    process = subprocess.Popen(shlex.split(resizeCommand), shell=False)
    process.wait()

def getSliceImageFromNifti(tempDir, outputName):
    # Get Slices. Slices are saved as slices.png.

    slicerCommand = "slicer '" + os.path.join(tempDir, "rendered.nii.gz") + \
                    "' -s 0.72 -S 2 750 '" + outputName + "'"
    subprocess.check_call(shlex.split(slicerCommand), shell=False)
    process = subprocess.Popen(shlex.split(slicerCommand), shell=False)
    process.wait()

os.chdir('/home/tom/Documents/Repos/nidmresults-fslhtml')
print(getVal('ExcursionSet.nii.gz', 'min'))
print(getVal('ExcursionSet.nii.gz', 'max'))
resizeTemplateToExcSet('ExcursionSet.nii.gz', 'templates/T1_skullStripped.nii', '.')
getSliceImageFromNifti('.', 'slices.png')


