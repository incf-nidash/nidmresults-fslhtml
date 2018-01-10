#!/usr/bin/env python3
import os
import shutil
import time
import sys
import rdflib
import zipfile
import glob
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style, br
from dominate.util import raw
import errno
from style.pageStyling import *
from nidmviewerfsl.lib.slicerTools import *
from nidmviewerfsl.lib.pageGen import pageGenerate
from queries.queryTools import *
	
#Attempts to create folder for HTML files, quits program if folder already exists
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
		
		if os.path.isdir(htmlFolder) == True: #Html/extract folder already exists
		
			if not overwrite:
				print("The folder %s already exists, would you like to overwrite it? y/n" % htmlFolder)
				reply = input()
				overwrite = (reply == "y")

			if overwrite: #User wants to overwrite folder
                                
				shutil.rmtree(htmlFolder) #Removes folder
				zip = zipfile.ZipFile(filepath, "r")
				zip.extractall(htmlFolder) #Extract zip file to destination folder
				turtleFile = glob.glob(os.path.join(htmlFolder, "*.ttl"))
				g.parse(turtleFile[0], format = "turtle")

				pageGenerate(g, htmlFolder)				
				
			else:
			
				exit()
			
		else:
			
			zip = zipfile.ZipFile(filepath, "r")
			zip.extractall(htmlFolder) #Extract zip file to destination folder
			turtleFile = glob.glob(os.path.join(htmlFolder, "*.ttl"))
			print(turtleFile)
			g.parse(turtleFile[0], format = rdflib.util.guess_format(turtleFile[0]))

			pageGenerate(g, htmlFolder)
			
		
	
	else:
	
		g.parse(filepath, format = rdflib.util.guess_format(filepath))
		destinationFolder = htmlFolder
	
		if overwrite == True: #User wants to overwite folder
			print("Overwrite")
			if os.path.isdir(destinationFolder) == True: #Check if directory already exists
		
				print("Removing %r" % destinationFolder)
			
				if os.path.isdir(destinationFolder + "Backup") == False:
			
					shutil.copytree(destinationFolder, destinationFolder + "Backup") #Backup the folder
				
				shutil.rmtree(destinationFolder) #Remove the folder
			
		createOutputDirectory(htmlFolder) #Create the html folder
	
		currentDir = os.getcwd()
		dirLocation = os.path.join(currentDir, destinationFolder)

		pageGenerate(g, dirLocation)
	
	return(destinationFolder) #Return the html/zip-extraction folder
