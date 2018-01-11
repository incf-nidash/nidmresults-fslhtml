#!/usr/bin/env python3
import os
import shutil
import rdflib
import zipfile
import glob
from nidmviewerfsl.lib.pageGen import pageGenerate
    
# This function attempts to create folder for HTML files, quits program if 
#folder already exists
def createOutputDirectory(outputFolder): 
    
    try:
    
        os.makedirs(outputFolder)
        
    except OSError:
    
        print("Error - %s directory already exists" % outputFolder)
        exit()

def main(nidmFile, htmlFolder, overwrite=False): #Main program

    g = rdflib.Graph()
    filepath = nidmFile
    
    if filepath.endswith(".nidm.zip"): #Nidm Zip file specified
    
        destinationFolder = htmlFolder
        
        #Html/extract folder already exists
        if os.path.isdir(htmlFolder) == True: 
        
            if not overwrite:
                print("The folder %s already exists, would you like to" \
                      " overwrite it? y/n" % htmlFolder)
                reply = input()
                overwrite = (reply == "y")

            if overwrite: #User wants to overwrite folder
                                
                shutil.rmtree(htmlFolder) #Removes folder
                zip = zipfile.ZipFile(filepath, "r")
                #Extract zip file to destination folder
                zip.extractall(htmlFolder) 
                turtleFile = glob.glob(os.path.join(htmlFolder, "*.ttl"))
                g.parse(turtleFile[0], format = "turtle")

                pageGenerate(g, htmlFolder)             
                
            else:
            
                exit()
            
        else:
            
            zip = zipfile.ZipFile(filepath, "r")
            #Extract zip file to destination folder
            zip.extractall(htmlFolder) 
            turtleFile = glob.glob(os.path.join(htmlFolder, "*.ttl"))
            print(turtleFile)
            g.parse(turtleFile[0], 
                    format = rdflib.util.guess_format(turtleFile[0]))

            pageGenerate(g, htmlFolder)
            
        
    
    else:
    
        g.parse(filepath, format = rdflib.util.guess_format(filepath))
        destinationFolder = htmlFolder
    
        if overwrite == True: #User wants to overwite folder
            print("Overwrite")
            #Check if directory already exists
            if os.path.isdir(destinationFolder) == True: 
        
                print("Removing %r" % destinationFolder)
            
                if os.path.isdir(destinationFolder + "Backup") == False:
            
                    shutil.copytree(destinationFolder, destinationFolder + \
                                    "Backup") #Backup the folder
                
                shutil.rmtree(destinationFolder) #Remove the folder
            
        createOutputDirectory(htmlFolder) #Create the html folder
    
        currentDir = os.getcwd()
        dirLocation = os.path.join(currentDir, destinationFolder)

        pageGenerate(g, dirLocation)
    
    return(destinationFolder) #Return the html/zip-extraction folder
