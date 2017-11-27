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

#Create subplots
fig = plt.figure(figsize=(numSlicePerRow-1,numSlicePerCol-1))
for i in list(range(0,numSlicePerCol)):
    axis = plt.subplot2grid((numSlicePerRow, numSlicePerCol), (i, 0), rowspan =1, colspan=numSlicePerCol)
    plotting.plot_stat_map(to_display, axes=axis, figure = fig, cut_coords=list(range(i*numSlicePerRow,i*numSlicePerRow + numSlicePerRow)), draw_cross=False, display_mode='z', threshold=0.05, colorbar=False, vmax=max_activation, title='')

fig.subplots_adjust(bottom=None, top = None, left = None, right = None)
plt.show()

