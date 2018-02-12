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
#nilearn, nibabel, sklearn
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

print(header)
