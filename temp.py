import numpy as np
import nibabel as nib
import sys
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
nib.save(exc_set_nonan, 'ExcursionSet2.nii.gz')

#Get the image z dimension
header = n.header

print(header)
