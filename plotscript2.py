from nilearn import plotting
from nilearn.image import math_img
import numpy as np
from nilearn.masking import apply_mask
from nilearn.image import load_img, new_img_like
from nilearn._utils.niimg_conversions import _safe_get_data
import nibabel as nib
import matplotlib.pyplot as plt
import sys
import math
import os

#Image pixel width
pixelwidth = 750

#Load in data
max_activation = 12
exc_set_file = 'ExcursionSet.nii.gz'

# Remove NaNs
n = nib.load(exc_set_file)
d = n.get_data()
exc_set_nonan = nib.Nifti1Image(np.nan_to_num(d), n.affine, header=n.header)

# Combine activations and deactivations in a single image 
to_display = exc_set_nonan

#Get the image z dimension
header = n.header
dimensions = header['dim']
zdim = dimensions[3]

#Work out number of slices per row for the display.
numSlicePerRow = math.ceil((pixelwidth/zdim))
numSlicePerCol = math.ceil((zdim/numSlicePerRow))

#Making temporary directory - as there are currently issues saving row subplots we have to save the images and combine them manually.
tempdir = 'nifti_image_temp'
os.mkdir(tempdir)

#Create subplots
for i in list(range(0,numSlicePerCol)):
    display = plotting.plot_stat_map(to_display, black_bg = True, cut_coords=list(range(i*numSlicePerRow,i*numSlicePerRow + numSlicePerRow)), draw_cross=False, display_mode='z', threshold=0.05, colorbar=False, vmax=max_activation, title='')
    saveLocation = tempdir + '//temp'+str(i)+'.png'
    plt.savefig(saveLocation, facecolor='k', edgecolor='k')
