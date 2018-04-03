# ==============================================================================
#
# The following functions are designed to resize SPM nifti maps to align with
# the given SPM template nifti using FSL and nilearn commands and output a
# slice image of the two niftis overlaid.
#
# ==============================================================================
#
# Authors: Tom Maullin, Camille Maumet (29/11/2017)

import subprocess
import os
import shutil
import random
import shlex
import numpy as np
import nibabel as nib
from nibabel.processing import resample_from_to
from queries.queryTools import runQuery


def nifDim(nifti, k):
    # Retrieve the k dimension of a nifti using nibabel.

    # Retrieve image header.
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


def resizeExcSet(exc_set, template, tempDir):
    # This function resizes an SPM excursion set to an SPM template if
    # necessary.

    # Load the images
    template_img = nib.load(template)
    excset_img = nib.load(exc_set)

    # Resample if necessary
    img_resl = resample_from_to(excset_img, template_img)

    nib.save(img_resl, os.path.join(tempDir, "resizedExcSet.nii.gz"))


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


def overlay(exc_set, template, o_exc_set, tempDir):
    # Overlay exc_set onto template. The output is saved as outputTemp

    # Get min and max values of the original excursion set.
    minZ = str(getVal(o_exc_set, 'min'))
    maxZ = str(getVal(o_exc_set, 'max'))

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


def generateSliceImage(exc_set, SPMorFSL):

    tempFolder = 'temp_NIDM_viewer' + str(random.randint(0, 999999))
    os.mkdir(tempFolder)
    FSLDIR = os.environ['FSLDIR']

    # Make a copy of the original name of the excursion set.
    o_exc_set = exc_set

    # Load the excursion set.
    n_exc = nib.load(exc_set)

    # If we are looking at FSL data use the FSL template.
    if SPMorFSL == 'FSL':
        if nifDim(exc_set, 'pix') == 1:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_1mm_brain.nii.gz')
        else:
            template = os.path.join(FSLDIR, 'data', 'standard',
                                    'MNI152_T1_2mm_brain.nii.gz')
    else:
        #  NaN values.
        d = n_exc.get_data()
        exc_set_nonan = nib.Nifti1Image(np.nan_to_num(d),
                                        n_exc.affine,
                                        header=n_exc.header)

        # Save the result.
        nib.save(exc_set_nonan, os.path.join(tempFolder,
                                             'excset_nonan.nii.gz'))
        exc_set = os.path.join(tempFolder, 'excset_nonan.nii.gz')

        # Use the SPM template.
        template = os.path.join(
            os.path.split(
                os.path.split(
                    os.path.split(os.path.realpath(__file__))[0])[0])[0],
            'templates', 'T1_skullStripped.nii')

    # Load the template.
    n_tem = nib.load(template)

    # If the images are different sizes/ have different affine
    # matrices, resize the excursion set. 
    if (n_tem.affine != n_exc.affine).any():
        # Check which is bigger and resize if necessary
        resizeExcSet(exc_set, template, tempFolder)

    # If we've resized the excursion set we want to look at the resized
    # file.
    exc_set = os.path.join(tempFolder, 'resizedExcSet.nii.gz')

    # Overlay niftis
    overlay(exc_set, template, o_exc_set, tempFolder)

    # Get the slices image
    getSliceImageFromNifti(tempFolder, o_exc_set.replace(
        '.nii', '').replace('.gz', '')+'.png')

    shutil.rmtree(tempFolder)

    return(o_exc_set.replace('.nii', '').replace('.gz', '')+'.png')
