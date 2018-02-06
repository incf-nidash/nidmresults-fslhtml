# !/usr/bin/env python3
# ==============================================================================
# This file contains the main function used to run the FSL NIDM-Results viewer.
# It takes as inputs:
# 
# nidmfile - the location of the nidm-results zip pack.
# htmlfolder - the output location.
# overwrite - whether the user gives permission for data to be overwritten.
# 
# Authors: Peter Williams, Tom Maullin, Camille Maumet (11/01/2018)
# ==============================================================================
import os
import shutil
import rdflib
import zipfile
import glob
from nidmviewerfsl.lib.pageGen import pageGenerate
    
# This function attempts to create folder for HTML files, quits program if 
# folder already exists
def createOutputDirectory(outputFolder): 
    
    try:
    
        os.makedirs(outputFolder)
        
    except OSError:
    
        print("Error - %s directory already exists" % outputFolder)
        exit()

def extractZip(htmlFolder, nidmFile):

    # Read in the Zip file.
    zip = zipfile.ZipFile(nidmFile, "r")

    # Extract zip file to destination folder
    zip.extractall(htmlFolder) 

    # Create RDF graph.
    g = rdflib.Graph()

    # Locate the ttl data
    turtleFile = glob.glob(os.path.join(htmlFolder, "*.ttl"))

    # Parse the ttl file.
    g.parse(turtleFile[0], format = "turtle")

    # Generate pages.
    pageGenerate(g, htmlFolder)             
                

def main(nidmFile, htmlFolder, overwrite=False): # Main program
    
    # First we check if we can overwrite htmlFolder if we need to.
    if not overwrite and os.path.isdir(htmlFolder):
        
        # Ask the user if we can overwrite.
        print("The folder %s already exists, would you like to" \
              " overwrite it? y/n" % htmlFolder)

        # Read in result.
        reply = input()
        overwrite = (reply == "y")

        # If they said no, exit. 
        if not overwrite:

            exit()

    # Overwrite htmlFolder if we need to.
    if overwrite and os.path.isdir(htmlFolder):

        shutil.rmtree(htmlFolder) 

    # Nidm Zip file specified 
    if nidmFile.endswith(".nidm.zip"):         
            
            extractZip(htmlFolder, nidmFile)  
    
    else:
        
        g = rdflib.Graph()
        g.parse(nidmFile, format = rdflib.util.guess_format(nidmFile))
        
        # User wants to overwite folder
        if overwrite == True: 
            print("Overwrite")
            # Check if directory already exists
            if os.path.isdir(htmlFolder) == True: 
        
                print("Removing %r" % htmlFolder)
            
                if os.path.isdir(htmlFolder + "Backup") == False:
                    
                    # Backup the folder
                    shutil.copytree(htmlFolder, htmlFolder + \
                                    "Backup") 
                
                # Remove the folder
                shutil.rmtree(htmlFolder) 
        
        # Create the html folder
        createOutputDirectory(htmlFolder) 
    
        currentDir = os.getcwd()
        dirLocation = os.path.join(currentDir, htmlFolder)

        pageGenerate(g, dirLocation)
    
    return(htmlFolder) # Return the html/zip-extraction folder
