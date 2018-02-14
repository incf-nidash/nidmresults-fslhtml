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


def nifDim(header, k):
    # Retrieve the k dimension of a nifti given it's header using FSL.

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


def overlay(exc_set, template, tempDir):
    # Overlay exc_set onto template. The output is saved as outputTemp

    # Get min and max values of the excursion set.
    minZ = getVal(exc_set, 'min')
    maxZ = getVal(exc_set, 'max')

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


def generateSliceImage_SPM(exc_set, SPMorFSL):

    tempFolder = 'temp_NIDM_viewer' + str(random.randint(0, 999999))
    os.mkdir(tempFolder)
    FSLDIR = os.environ['FSLDIR']

    #Retrieve image header.
    n = nib.load(exc_set)
    header = n.header

    # If we are looking at FSL data use the FSL template.
    if SPMorFSL == 'FSL':
        if nifDim(header, 'pix') == 1:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_1mm_brain.nii.gz')
        else:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_2mm_brain.nii.gz')
    else:
        #Remove NaN values.
        d = n.get_data()
        exc_set_nonan = nib.Nifti1Image(np.nan_to_num(d), n.affine, header=n.header)

        # Combine activations and deactivations in a single image 
        nib.save(exc_set_nonan, os.path.join(tempFolder, 'excset_nonan.nii.gz'))
        exc_set = os.path.join(tempFolder, 'excset_nonan.nii.gz')

        #Use the SPM template.
        template = '/home/tom/Documents/Repos/nidmresults-fslhtml/templates/T1.nii'

    # Check which is bigger and resize if necessary
    #resizeSPMtoFSL(exc_set, template, scalefactor, tempFolder)
    #resized_exc_set = os.path.join(tempFolder, 'resizedNifti.nii.gz')

    # Overlay niftis
    overlay(exc_set, template, tempFolder)

    # Get the slices image
    getSliceImageFromNifti(tempFolder, exc_set.replace(
        '.nii', '').replace('.gz', '')+'.png')

    shutil.rmtree(tempFolder)

    return(exc_set.replace('.nii', '').replace('.gz', '')+'.png')

generateSliceImage_SPM('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/fsl_default_130_test/ExcursionSet.nii.gz', 'SPM')
