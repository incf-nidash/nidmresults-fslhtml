# ======================================================================
# This file contains a collection of small functions for reading in and
# encoding images as well as the CSS styling for FSL output pages.
#
# Author: Tom Maullin (04/12/2017)
# ======================================================================
import os
import shutil
import random
import base64


# Obtain the FSL directory.
def obtain_fsl_dir():

    return(os.environ['FSLDIR'])


# Obtain the FSL style sheet.
def find_css():

    cssStyleSheet = os.path.join(obtain_fsl_dir(), 'doc', 'fsl.css')
    return(cssStyleSheet)


# Encode an image for embedding
def encode_image(image):

    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string


# Find the FSL logo and get it's encoding for embedding in the HTML page.
def encode_logo():

    imageLink = os.path.join(obtain_fsl_dir(), 'doc', 'images', 'fsl-logo.jpg')
    encoded_string = encode_image(imageLink)

    return('data:image/jpg;base64,' + encoded_string.decode())


# Find the FSL color bar and get it's encoding for embedding in the HTML page.
def encode_color_bar():

    imageLink = os.path.join(obtain_fsl_dir(), 'etc', 'luts', 'ramp.gif')
    encoded_string = encode_image(imageLink)

    return('data:image/jpg;base64,' + encoded_string.decode())


# Find the FSL background and get it's encoding for embedding in the CSS
# style sheet.
def encode_bg():

    imageLink = os.path.join(obtain_fsl_dir(), 'doc', 'images', 'fsl-bg.jpg')
    encoded_string = encode_image(imageLink)

    return('background-image: url(data:image/jpg;base64,' +
           encoded_string.decode() + ');')


# Gets the raw stylesheet as a string in order to embed.
def get_raw_css():

    # Open the CSS file
    file = open(find_css(), "r")

    # Read the CSS file
    cssStyleSheet = file.read()

    # Replace the link to the logo with the embedded logo itself.
    cssStyleSheet = cssStyleSheet.replace(
                        'background-image: url("images/fsl-bg.jpg");',
                        encode_bg())

    # Close the file.
    file.close()

    return(cssStyleSheet)
