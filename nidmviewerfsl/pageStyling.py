#======================================================================
# This file contains a collection of small functions for reading in and
# encoding images as well as the CSS styling for FSL output pages. It
# assumes FSL is installed.
#
# Author: Tom Maullin (04/12/2017)
#======================================================================
import subprocess
import os
import shutil
import random
import base64

#Obtain the FSL directory.
def obtainFSLdir():
    
    return(os.environ['FSLDIR'])

#Obtain the FSL style sheet.
def findCSS():

    cssStyleSheet = os.path.join(obtainFSLdir(), 'doc', 'fsl.css')
    return(cssStyleSheet)

#Encode an image for embedding
def encodeImage(image):

    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string

#Find the FSL logo and get it's encoding for embedding in the HTML page.
def encodeLogo():
    
    imageLink = os.path.join(obtainFSLdir(), 'doc', 'images', 'fsl-logo.jpg')
    encoded_string = encodeImage(imageLink)

    return('data:image/jpg;base64,' + encoded_string.decode())

#Find the FSL color bar and get it's encoding for embedding in the HTML page.
def encodeColorBar():
    
    imageLink = os.path.join(obtainFSLdir(), 'etc', 'luts', 'ramp.gif')
    encoded_string = encodeImage(imageLink)

    return('data:image/jpg;base64,' + encoded_string.decode())

#Find the FSL background and get it's encoding for embedding in the CSS style sheet.
def encodeBG():
    
    imageLink = os.path.join(obtainFSLdir(), 'doc', 'images', 'fsl-bg.jpg')
    encoded_string = encodeImage(imageLink)

    return('background-image: url(data:image/jpg;base64,' + encoded_string.decode() + ');')

#Gets the raw stylesheet as a string in order to embed.
def getRawCSS():

    #Open the CSS file
    file = open(findCSS(), "r")

    #Read the CSS file
    cssStyleSheet = file.read()

    #Replace the link to the logo with the embedded logo itself.
    cssStyleSheet = cssStyleSheet.replace('background-image: url("images/fsl-bg.jpg");', encodeBG())
    
    return(cssStyleSheet)
