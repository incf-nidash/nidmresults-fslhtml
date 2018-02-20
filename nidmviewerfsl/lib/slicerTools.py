# ==============================================================================
#
# The following functions are designed to resize SPM nifti maps to align with
# an FSL template and create corresponding slice images. It does this by
# making several calls to FSL using the bash command line through fsl
# subprocess. To create an FSL slice image for an SPM excursion set simply call
# generateSliceImage(<excursion set filepath>)`.
#
# Note: This resizing is necessary as the SPM excursion set map will be
# surrounded by less blank space (e.g. there will be less zeros/NaNs on the
# border of the NIFTI image) than the FSL template and without this
# adjustment, the excursion set will not be aligned with the background it is
# displayed on.
#
# ==============================================================================
#
# Documentation of matrix creation:
#
# ==============================================================================
#
# When the voxel size in mm in both maps is the same:
#
# An SPM map containing a brain volume will be larger than an FSL template
# holding a brain volume of the same size (more blank space is included at the
# edges/sides). In order to display a slice view this extra blank space at the
# side of the nifti must be accounted for (else the FSL template and SPM
# excursion set will not align in the slice display) and to do this, we must
# resize the SPM nifti by adding more blank space to the side (note this does
# not affect the statistic values inside the excursion set).
#
# To resize an SPM map to match the layout of an FSL template the FSL function
# `flirt` can be used. However, to do this specific transform a resize matrix
# is required.
#
# By default, if resizing a smaller map to a larger map `flirt` creates an
# empty map of the same size
# as the larger map and places the smaller map in the front-left hand corner,
# centered in the z-axis.
#
# In other words when the smaller map is enlarged, (x, y, z) in the original
# small map becomes (x, y, {l_z-s_z}/2 + z) in the larger map where l_z is the
# z dimension of the larger map and s_z is the z dimension of the smaller map.
#
# This means the z dimensions of the SPM brain volume is now aligned with the
# z dimension of the FSL template brain volume but the x and y dimensions are
# not. To rectify this the following transform
# matrix must be used in flirt:
#
#  / 1 0 0 dx \
# |  0 1 0 dy  |
# |  0 0 1 0   |
#  \ 0 0 0 1  /
#
# Where dx = l_x - s_x, the difference in size of the x dimensions.
# and dy = l_y - s_y, the difference in size of the y dimensions.
#
# ------------------------------------------------------------------------------
#
# When the voxel size in mm in both maps is not the same:
#
# When the voxel size in mm is not the same a scaling factor must be added.
# When the SPM map has a voxel size larger than 2, the matrix to scale and
# align the SPM map to the FSL 2mm template simplifies to:
#
#  / 1 0 0 s*dx \
# |  0 1 0 s*dy  |
# |  0 0 1  0    |
#  \ 0 0 0  1   /
#
# where s = 1/v_spm where v_spm is the voxel size of the SPM map.
#
# ------------------------------------------------------------------------------
# Source: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FLIRT/FAQ
# Author: Tom Maullin (29/11/2017)

import subprocess
import os
import shutil
import random
import shlex
import numpy as np
import nibabel as nib
from queries.queryTools import runQuery


def nifDim(nifti, k):
    # Retrieve the k dimension of a nifti using nibabel.

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


def createResizeMatrix(niftiFilename1, niftiFilename2, scalefactor, tempDir):
    # This creates the resize matrix for the resizing of the niftis and saves
    # it as resizeMatrix.mat

    xShift = -abs(nifDim(niftiFilename1, 'x') - nifDim(niftiFilename2, 'x'))
    yShift = -abs(nifDim(niftiFilename1, 'y') - nifDim(niftiFilename2, 'y'))

    # Open the matrix file.
    matrixFile = open(os.path.join(tempDir, 'resizeMatrix.mat'), 'w')

    # Write the matrix file
    matrixFile.write('1 0 0 ' + str(scalefactor*xShift) + ' \n')
    matrixFile.write('0 1 0 ' + str(scalefactor*yShift) + ' \n')
    matrixFile.write('0 0 1 0 \n')
    matrixFile.write('0 0 0 1 \n')

    # Close the matrix file.
    matrixFile.close()


def resizeTemplateOrExcSet(exc_set, template, scalefactor, tempDir):
    # This function resizes an SPM excursion set to an SPM template if
    # necessary.

    # Create necessary tranformation.
    createResizeMatrix(exc_set, template, scalefactor, tempDir)

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

def getVal(niftiFilename, minOrMax):
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


def overlay(exc_set, template, tempDir):
    # Overlay exc_set onto template. The output is saved as outputTemp

    # Get min and max values of the excursion set.
    minZ = str(getVal(exc_set, 'min'))
    maxZ = str(getVal(exc_set, 'max'))

    # Place the template onto the excursion set using overlay
    overlayCommand = "overlay 1 1 " + template + " -a " + exc_set + " " + \
                     minZ + " " + maxZ + " " + \
                     os.path.join(tempDir, "outputTemp.nii.gz")
    subprocess.check_call(shlex.split(overlayCommand), shell=False)
    process = subprocess.Popen(shlex.split(overlayCommand), shell=False)
    process.wait()


def getSliceImageFromNifti(tempDir, outputName):
    # Get Slices. Slices are saved as slices.png.

    slicerCommand = "slicer '" + os.path.join(tempDir, "outputTemp.nii.gz") + \
                    "' -s 0.72 -S 2 750 '" + outputName + "'"
    subprocess.check_call(shlex.split(slicerCommand), shell=False)
    process = subprocess.Popen(shlex.split(slicerCommand), shell=False)
    process.wait()

    print(outputName)


def generateSliceImage(exc_set, SPMorFSL):

    tempFolder = 'temp_NIDM_viewer' + str(random.randint(0, 999999))
    os.mkdir(tempFolder)
    FSLDIR = os.environ['FSLDIR']

    #Make a copy of the original name of the excursion set.
    o_exc_set = exc_set

    # If we are looking at FSL data use the FSL template.
    if SPMorFSL == 'FSL':
        if nifDim(exc_set, 'pix') == 1:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_1mm_brain.nii.gz')
        else:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_2mm_brain.nii.gz')
    else:
        #Remove NaN values.
        n = nib.load(exc_set)
        d = n.get_data()
        exc_set_nonan = nib.Nifti1Image(np.nan_to_num(d), n.affine, header=n.header)

        # Save the result.
        nib.save(exc_set_nonan, os.path.join(tempFolder, 'excset_nonan.nii.gz'))
        exc_set = os.path.join(tempFolder, 'excset_nonan.nii.gz')

        #Use the SPM template.
        template = os.path.join(
            os.path.split(
                os.path.split(
                    os.path.split(os.path.realpath(__file__))[0])[0])[0],
            'templates', 'T1_skullStripped.nii')

        #Calculate the scale factor.
        if nifDim(exc_set, 'pix') <= 2:
            scalefactor = 1
        else:
            scalefactor = 1/nifDim(exc_set, 'pix')

        # Check which is bigger and resize if necessary
        resizeTemplateOrExcSet(exc_set, template, scalefactor, tempFolder)

        # If we've resized the excursion set we want to look at the resized file.
        if nifDim(exc_set, 'x') > nifDim(template, 'x'):
            exc_set = os.path.join(tempFolder, 'resizedNifti.nii.gz')

        # If we've resized the template we want to look at the resized file.
        if nifDim(exc_set, 'x') < nifDim(template, 'x'):
            template = os.path.join(tempFolder, 'resizedNifti.nii.gz')

    # Overlay niftis
    overlay(exc_set, template, tempFolder)

    # Get the slices image
    getSliceImageFromNifti(tempFolder, o_exc_set.replace(
        '.nii', '').replace('.gz', '')+'.png')

    shutil.rmtree(tempFolder)

    return(o_exc_set.replace('.nii', '').replace('.gz', '')+'.png')
