from nilearn import plotting
from nilearn.image import math_img
import numpy as np
from nilearn.masking import apply_mask
from nilearn.image import load_img, new_img_like, swap_img_hemispheres
from nilearn._utils.niimg_conversions import _safe_get_data
import nibabel as nib
import matplotlib.pyplot as plt
import sys
import math
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import shutil

#Image pixel width
pixelwidth = 750

#Setup
max_activation = 12
exc_set_file = 'ExcursionSet.nii.gz'

#Load in mask
n = nib.load(exc_set_file)
d = n.get_data()


#We first swap to from radiological to neurological view as
#this is what FSL does!
#
#(Note to future developers: If you add labels to plotting
#now the L and R will be the wrong way around! nilearn does
#not notice you've reoriented!!!)
n = swap_img_hemispheres(exc_set_file)

# Remove NaNs
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

#Making temporary directory - as there are currently issues saving row subplots
#in nilearn (white space is added that can't be removed and the black background
#cannot be saved) we have to save the images and combine them manually.
tempdir = 'nifti_image_temp'
os.mkdir(tempdir)

imageArray = []
#Create subplots
for i in list(range(0,numSlicePerCol)):
    display = plotting.plot_stat_map(to_display, black_bg = True, annotate = False, cut_coords=list(range(i*numSlicePerRow,i*numSlicePerRow + numSlicePerRow)), draw_cross=False, display_mode='z', threshold=0.05, colorbar=False, vmax=max_activation, title='')
    saveLocation = tempdir + '//temp'+str(i)+'.png'
    imageArray.append(saveLocation)
    plt.savefig(saveLocation, facecolor='k', edgecolor='k')

imgs = [Image.open(i) for i in imageArray]

#The nilearn toolbox doesn't have an option to label left and right as neurological
#(it always assumes radiological) so this has been done manually using imagedraw.
img_merge = np.vstack((np.asarray(i) for i in imgs ) )
img_merge = Image.fromarray(img_merge)
draw = ImageDraw.Draw(img_merge)
font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 30)

width_img, height_img = img_merge.size
width_slice = width_img/numSlicePerRow
height_slice = height_img/numSlicePerCol
for i in list(range(0,numSlicePerRow)):
    for j in list(range(0,numSlicePerCol)):
        draw.text((i*width_slice+10, j*height_slice+10),"R",(255,255,255),font=font)

img_merge.save('slicedisplay.png')

#Delete temporary file.
shutil.rmtree('nifti_image_temp')

