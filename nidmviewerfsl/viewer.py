# !/usr/bin/env python3
# ==============================================================================
# This file contains the main function used to run the FSL NIDM-Results viewer.
# It takes as inputs:
#
# nidmPack - the location of the nidm-results zip pack.
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
from nidmviewerfsl.lib.pagegen import page_generate
import webbrowser


# This function attempts to create folder for HTML files, quits program if
# folder already exists
def create_output_directory(outputFolder):

    try:

        os.makedirs(outputFolder)
        os.makedirs(os.path.join(outputFolder, 'NIDMData'))

    except OSError:

        print("Error - %s directory already exists" % outputFolder)
        exit()


def extract_zip(htmlFolder, nidmPack):

    # Read in the Zip file.
    zip = zipfile.ZipFile(nidmPack, "r")

    # Extract_zzip file to destination folder
    zip.extractall(os.path.join(htmlFolder, 'NIDMData'))

    # Create RDF graph.
    g = rdflib.Graph()

    # Locate the ttl data
    turtleFile = glob.glob(os.path.join(htmlFolder, 'NIDMData', "*.ttl"))

    # Parse the ttl file.
    g.parse(turtleFile[0], format="turtle")

    return(g)


def main(nidmPack, htmlFolder, overwrite=False, display=False):  # Main program

    # First we check if we can overwrite htmlFolder if we need to.
    if not overwrite and os.path.isdir(htmlFolder):

        # Ask the user if we can overwrite.
        print("The folder %s already exists, would you like to"
              " overwrite it? y/n" % htmlFolder)

        # Read in result.
        reply = input()
        overwrite = (reply == "y")

        # If they said no, exit.
        if not overwrite:

            print('Program exited. Cause: Overwrite permission'
                  ' denied.')
            exit()

    # Overwrite htmlFolder if we need to.
    if overwrite and os.path.isdir(htmlFolder):

        print('Overwriting: ' + htmlFolder)
        shutil.rmtree(htmlFolder)

    # Create the output directory.
    create_output_directory(htmlFolder)

    # Tell the user the code is running.
    print('Generating display...')

    # Nidm Zip file specified
    if nidmPack.endswith(".nidm.zip"):

        g = extract_zip(htmlFolder, nidmPack)

        # Generate pages.
        page_generate(g, htmlFolder, os.path.join(htmlFolder, 'NIDMData'))

    else:

        # Create RDF graph.
        g = rdflib.Graph()

        # Locate the ttl data
        turtleFile = glob.glob(os.path.join(nidmPack, "*.ttl"))

        # Parse the ttl file.
        g.parse(turtleFile[0], format="turtle")

        page_generate(g, htmlFolder, nidmPack)

    # Remove the temporary data folder.
    shutil.rmtree(os.path.join(htmlFolder, 'NIDMData'))

    # Tell the user the display is ready.
    print('FSL NIDM-Results display now available at: ' + htmlFolder)

    # Display if necessary
    if display:
        webbrowser.open(os.path.join(htmlFolder, 'report_stats.html'))

    return(htmlFolder)  # Return the html/zip-extraction folder
