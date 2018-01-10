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
from nidmviewerfsl.pageStyling import *
from nidmviewerfsl.callSlicer import *

def addQueryToList(query):
    
    queryList = []

    for i in query:

        for j in i:

            queryList.append("%s" % j)

    return(queryList)

def printQuery(query): #Generic function for printing the results of a query - used for testing

	for row in query: 
	
	#STARTFOR
		
		
		if len(row) == 1:
			
			print("%s" % row)
		
		elif len(row) == 2:
		
			print("%s, %s" % row)
		
		elif len(row) == 3:
			
			print("%s, %s, %s" % row)
			
		else:
			
			print("Error, not a suitable length")
		
	#ENDFOR

def runQuery(graph, queryFile, queryType, filters={}):

	queryFile = open(queryFile)
	queryText = queryFile.read()
	queryFile.close()

	for fil in filters:

		queryText = queryText.replace('{{{' + fil + '}}}', filters[fil])
	
	queryOutput = graph.query(queryText)

	if queryType == 'Ask':
		           
		for row in queryOutput:
			queryResult = row
	
		if queryResult == True:
			return(True)
		else:
			return(False)

	if queryType == 'Select':
		
		return(addQueryToList(queryOutput))

def statisticImage(stat): #Returns type of statistic image

	if stat == "http://purl.obolibrary.org/obo/STATO_0000376":
	
		return("Z")
	
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000282":
	
		return("F")
		
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000176":
	
		return("T")
		
	else:
		
		return(None)

def clusterFormingThreshType(graph, image):

	if runQuery(graph, os.path.join('..','Queries','askIfOboStatistic.txt'), 'Ask') == True:
	
		return(image)
		
	elif runQuery(graph, os.path.join('..','Queries','askIfPValueUncorrected.txt'), 'Ask') == True:
	
		return("P")
			   
	
def statisticImageString(statImage):

	if statImage == "T":
	
		return("T")
		
	elif statImage == "F":
	
		return("F")
		
	elif statImage == "Z":
	
		return("Z (Gaussianised T/F)")

def formatClusterStats(g, excName):
        
        #---------------------------------------------------------------------------------------------------------
        #First we gather data for peaks table.
        #---------------------------------------------------------------------------------------------------------

        #Run the peak query
        peakQueryResult = runQuery(g, os.path.join('..','Queries','selectPeakData.txt'), 'Select', {'EXC_NAME': excName})

        #Retrieve query results.

        peakZstats = [float(peakQueryResult[i]) for i in list(range(0, len(peakQueryResult), 3))]
        clusterIndicesForPeaks = [int(peakQueryResult[i]) for i in list(range(1, len(peakQueryResult), 3))]
        locations = [peakQueryResult[i] for i in list(range(2, len(peakQueryResult), 3))]

        #Obtain permutation used to sort the results in order of descending cluster index and then descending peak statistic size.
        peaksSortPermutation = sorted(range(len(clusterIndicesForPeaks)), reverse = True, key=lambda k: (clusterIndicesForPeaks[k], peakZstats[k]))

        #Sort all peak data using this permutation.
        sortedPeaksZstatsArray = [peakZstats[i] for i in peaksSortPermutation]
        sortedClusIndicesForPeaks = [clusterIndicesForPeaks[i] for i in peaksSortPermutation]
        sortedPeakLocations = [locations[i] for i in peaksSortPermutation]

        #---------------------------------------------------------------------------------------------------------
        #Second we gather data for cluster table.
        #---------------------------------------------------------------------------------------------------------

        #Run the cluster query
        clusQueryResult = runQuery(g, os.path.join('..','Queries','selectClusterData.txt'), 'Select', {'EXC_NAME': excName})

        clusterIndices = [int(clusQueryResult[i]) for i in list(range(0, len(clusQueryResult), 2))]
        clusterSizes = [int(clusQueryResult[i]) for i in list(range(1, len(clusQueryResult), 2))]
        
        #Create an array for the highest peaks.
        highestPeakZArray = [0]*len(clusterIndices)
        highestPeakLocations = [0]*len(clusterIndices)
        for i in list(range(0, len(peakZstats))):
                if highestPeakZArray[clusterIndicesForPeaks[i]-1] < peakZstats[i]:
                        highestPeakZArray[clusterIndicesForPeaks[i]-1] = peakZstats[i]
                        highestPeakLocations[clusterIndicesForPeaks[i]-1] = locations[i]

        #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
        clusterSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: clusterIndices[k])

        #Sorted cluster arrays
        sortedClusSizeArray = [clusterSizes[i] for i in clusterSortPermutation]
        sortedClusIndicesArray = [clusterIndices[i] for i in clusterSortPermutation]

        #Sort the highest peaks
        sortedMaxPeakZstats = [highestPeakZArray[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
        sortedMaxPeakLocations = [highestPeakLocations[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]

        return({'clusSizes':sortedClusSizeArray,
                'clusIndices':sortedClusIndicesArray,
                'clusPeakZstats':sortedMaxPeakZstats,
                'clusPeakLocations':sortedMaxPeakLocations,
                'peakZstats':sortedPeaksZstatsArray,
                'peakClusIndices':sortedClusIndicesForPeaks,
                'peakLocations':sortedPeakLocations})

def generateExcPage(outdir, excName, conData):

        #Create new document.
        excPage = document(title="Cluster List") #Creates initial HTML page
        with excPage.head:
                style(raw(getRawCSS()))
        excPage += raw("<center>")
        excPage += hr()
        excPage += raw("Co-ordinate information for " + excName + " - ")
        excPage += raw("<a href='../main.html'>back</a>")
        excPage += raw(" to main page")
        excPage += hr()

        #Cluster statistics section.
        excPage += h1("Cluster List")

        #Make the cluster statistics table.
        excPage += raw("<table cellspacing='3' border='3'><tbody>")
        excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>Z-MAX</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")
        
        #Add the cluster statistics data into the table.
        for cluster in range(0, len(conData['clusSizes'])):
                #New row
                excPage += raw("<tr>")
                excPage += raw("<td>" + str(conData['clusIndices'][cluster]) + "</td>")
                excPage += raw("<td>" + str(conData['clusSizes'][cluster]) + "</td>")
                excPage += raw("<td>" + str(float('%.2f' % float(conData['clusPeakZstats'][cluster]))) + "</td>")

                #Peak location
                formattedLoc = conData['clusPeakLocations'][cluster].replace(" ", "").replace("[", "").replace("]","").split(",")
                excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
                excPage += raw("</tr>")

        #Close table
        excPage += raw("</tbody></table>")

        excPage += br()
        excPage += br()
        excPage += h1("Local Maxima")
        
        #Make the peak statistics table.
        excPage += raw("<table cellspacing='3' border='3'><tbody>")
        excPage += raw("<tr><th>Cluster Index</th><th>Z-MAX</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")

        #Add the peak statistics data into the table.
        for peak in range(0, len(conData['peakZstats'])):
                #New row
                excPage += raw("<tr>")
                excPage += raw("<td>" + str(conData['peakClusIndices'][peak]) + "</td>")
                excPage += raw("<td>" + str(float('%.2f' % float(conData['peakZstats'][peak]))) + "</td>")

                #Peak location
                formattedLoc = conData['peakLocations'][peak].replace(" ", "").replace("[", "").replace("]","").split(",")
                excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
                excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
                excPage += raw("</tr>")

        #Close table
        excPage += raw("</tbody></table>")
        
        excPage += raw("</center>")
        excFile = open(os.path.join(outdir, excName + ".html"), "x")
        print(excPage, file = excFile) #Prints html page to a file
        excFile.close()  

def generateMainHTML(graph,mainFilePath = "Main.html", statsFilePath = "stats.html", postStatsFilePath = "postStats.html"): #Generates the main HTML page

	main = document(title="FSL Viewer")
	with main.head:
		style(raw(getRawCSS()))
	main += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src ="' + encodeLogo() + '" align="right"></a>')
	main += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')
	main += raw(os.path.dirname(mainFilePath)+'<br>')
	main += raw('NIDM-Results display generated on '+time.strftime("%c")+'<br>')
	main += raw('<a href="stats.html" target="_top"> Stats </a> - <a href="postStats.html" target="_top"> Post-stats </a></div>')
	mainFile = open(mainFilePath, "x")
	print(main, file = mainFile)
	mainFile.close()
		
	
def generateStatsHTML(graph,statsFilePath = "stats.html",postStatsFilePath = "postStats.html"): #Generates the Stats HTML section

	firstLevel = runQuery(graph, os.path.join('..','Queries','askFirstLevel.txt'), 'Ask')
	softwareLabelNum = runQuery(graph, os.path.join('..','Queries','selectVersionNum.txt'), 'Select')
	
	stats = document(title="FSL Viewer") #Creates initial html page (stats)
	with stats.head:
		style(raw(getRawCSS()))
	stats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src ="' + encodeLogo() + '" align="right"></a>')
	stats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')
	stats += raw(os.path.dirname(statsFilePath)+'<br>')
	stats += raw('NIDM-Results display generated on '+time.strftime("%c")+'<br>')
	stats += raw('<a href="main.html" target="_top"> Up to main page </a> - <a href="stats.html" target="_top"> Stats </a> - <a href="postStats.html" target="_top"> Post-stats </a></div>')
	stats += h2("Stats")
	stats += hr()
	stats += h3("Analysis Methods")
	
	if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True: #Checks if SPM was used
		
		stats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." % softwareLabelNum[1])
		
	elif runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True: #Checks if FSL was used
		
		fslFeatVersion = runQuery(graph, os.path.join('..','Queries','selectFslFeatVersion.txt'), 'Select')
		stats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)." % (fslFeatVersion[0], softwareLabelNum[1]))
		
	stats += hr()
	stats += h3("Design Matrix")
	
	designMatrixLocation = runQuery(graph, os.path.join('..','Queries','selectDesignMatrixLocation.txt'), 'Select')
	
	stats += a(img(src = designMatrixLocation[1], style = "border:5px solid black", border = 0, width = 250), href = designMatrixLocation[0]) #Adds design matrix image (as a link) to html page
	
	statsFile = open(statsFilePath, "x")
	print(stats, file = statsFile) #Prints html page to a file
	statsFile.close()
	
def generatePostStatsHTML(graph,statsFilePath = "stats.html",postStatsFilePath = "postStats.html"): #Generates Post-Stats page
	voxelWise = runQuery(graph, os.path.join('..','Queries','askCHeightThreshold.txt'), 'Ask')
	clusterWise = runQuery(graph, os.path.join('..','Queries','askCExtentThreshold.txt'), 'Ask')
	softwareLabelNum = runQuery(graph, os.path.join('..','Queries','selectVersionNum.txt'), 'Select')
	statisticType = runQuery(graph, os.path.join('..','Queries','selectStatisticType.txt'), 'Select')
	statisticType = statisticImage(statisticType[0])
	statisticTypeString = statisticImageString(statisticType)
	excDetails = runQuery(graph, os.path.join('..','Queries','selectExcursionSetDetails.txt'), 'Select')
	excursionSetNifti = list(set([excDetails[i] for i in list(range(0, len(excDetails), 3))]))
	excursionSetSliceImage = [excDetails[i] for i in list(range(1, len(excDetails), 3))]
	contrastName = [excDetails[i] for i in list(range(2, len(excDetails), 3))]

	postStats = document(title="FSL Viewer") #Creates initial HTML page (Post Stats)
	with postStats.head:
		style(raw(getRawCSS()))
	postStats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src ="' + encodeLogo() + '" align="right"></a>')
	postStats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')
	postStats += raw(os.path.dirname(postStatsFilePath)+'<br>')
	postStats += raw('NIDM-Results display generated on '+time.strftime("%c")+'<br>')
	postStats += raw('<a href="main.html" target="_top"> Up to main page </a> - <a href="stats.html" target="_top"> Stats </a> - <a href="postStats.html" target="_top"> Post-stats </a></div>')
	postStats += h2("Post-stats")
	postStats += hr()
	postStats += h3("Analysis Methods")
	
	if voxelWise == True: #If main threshold is Height Threshold
		mainThreshValue = runQuery(graph, os.path.join('..','Queries','selectCHeightThreshold.txt'), 'Select')
		if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True:
			
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at P = %s (corrected)" % (softwareLabelNum[1], statisticTypeString, mainThreshValue[0]))
	
		elif runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True:
			fslFeatVersion = runQuery(graph, os.path.join('..','Queries','selectFslFeatVersion.txt'), 'Select')
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at P = %s (corrected)" 
			%(fslFeatVersion[0], softwareLabelNum[1], statisticTypeString, mainThreshValue[0]))
	
	elif clusterWise == True: #If main threshold is extent threshold
		
		mainThreshValue = runQuery(graph, os.path.join('..','Queries','selectCExtentThreshold.txt'), 'Select')
		heightThreshValue = runQuery(graph, os.path.join('..','Queries','selectUHeightThreshold.txt'), 'Select')
		clusterThreshType = clusterFormingThreshType(graph, statisticType)
		
		if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True:
			
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded using clusters determined by %s > %s and a (corrected) "
			"cluster significance of P = %s " 
			% (softwareLabelNumList[1], statisticTypeString, clusterThreshType, heightThreshValue[0], mainThreshValue[0]))
	
		elif runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True:
			fslFeatVersion = runQuery(graph, os.path.join('..','Queries','selectFslFeatVersion.txt'), 'Select')
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). %s statistic images were thresholded "
			"using clusters determined by %s > %s and a (corrected) cluster significance of P = %s" 
			%(fslFeatVersion[0], softwareLabelNum[1], statisticTypeString, clusterThreshType, heightThreshValue[0], mainThreshValue[0]))
		
	
	else: #If there is no corrected threshold - assume voxel wise
		mainThreshValue = runQuery(graph, os.path.join('..','Queries','selectUHeightThreshold.txt'), 'Select')
		if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True and runQuery(graph, os.path.join('..','Queries','askIfPValueUncorrected.txt'), 'Ask') == True: #SPM used and threshold type is nidm_PValueUncorrected
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at P = %s (uncorrected)" % (softwareLabelNum[1], statisticTypeString, float('%.2g' % float(mainThreshValue[0]))))
			
		
		elif runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True and runQuery(graph, os.path.join('..','Queries','askIfOboStatistic.txt'), 'Ask') == True: #SPM used and threshold type is obo_statistic
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at %s = %s (uncorrected)" % (softwareLabelNum[1], statisticTypeString, statisticType, float('%.2g' % float(mainThreshValue[0]))))
			
		
		elif runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True and runQuery(graph, os.path.join('..','Queries','askIfPValueUncorrected.txt'), 'Ask') == True:
			
			fslFeatVersion = runQuery(graph, os.path.join('..','Queries','selectFslFeatVersion.txt'), 'Select')
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at P = %s (uncorrected)." % (fslFeatVersion[0], softwareLabelNum[1], statisticTypeString, mainThreshValue[0]))
			
			
		elif runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True and runQuery(graph, os.path.join('..','Queries','askIfOboStatistic.txt'), 'Ask') == True:
			
			fslFeatVersion = runQuery(graph, os.path.join('..','Queries','selectFslFeatVersion.txt'), 'Select')
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at %s = %s (uncorrected)." % (fslFeatVersion[0], softwareLabelNum[1], statisticTypeString, statisticType, mainThreshValue[0]))
			
		
	
	postStats += hr()
	postStats += h3("Thresholded Activation Images")
	postStats += hr()
	i = 0
	
	if runQuery(graph, os.path.join('..','Queries','askFSL.txt'), 'Ask') == True:
	
		while i < len(contrastName):
		
			#Colorbar and colorbar limits.
			postStats += raw("%s" % contrastName[i] + "&nbsp &nbsp" +
                                         "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[i]), 'min')) +
                                         " &nbsp " +
                                         "<img src = '" + encodeColorBar() + "'>" +
                                         " &nbsp " +
                                         "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[i]), 'max')) +
                                         "<br><br>")
			postStats += raw("<a href = '" + os.path.join('.', 'Cluster_Data', excursionSetNifti[i].replace('.nii.gz', '.html')) + "'>")
			postStats += img(src = 'data:image/jpg;base64,' + encodeImage(os.path.join(os.path.split(postStatsFilePath)[0],excursionSetSliceImage[i])).decode())
			postStats += raw("</a>")
			postStats += br()
			postStats += br()
			i = i + 1

	if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True and len(excursionSetNifti) == len(contrastName):
	
		while i < len(excursionSetNifti):
		
			postStats += raw("%s" % contrastName[i] + "&nbsp &nbsp" +
                                         "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[i]), 'min')) +
                                         " &nbsp " +
                                         "<img src = '" + encodeColorBar() + "'>" +
                                         " &nbsp " +
                                         "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[i]), 'max')) +
                                         "<br><br>")
			sliceImage = generateSliceImage_SPM(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[i]))
			postStats += raw("<a href = '" + os.path.join('.', 'Cluster_Data', excursionSetNifti[i].replace('.nii.gz', '.html')) + "'>")
			postStats += img(src = 'data:image/jpg;base64,' + encodeImage(sliceImage).decode())
			postStats += raw("</a>")
			i = i + 1

	if runQuery(graph, os.path.join('..','Queries','askSPM.txt'), 'Ask') == True and len(excursionSetNifti) < len(contrastName):
		
		conString = 'Conjunction : '
		
		while i < len(contrastName):
		
			conString += contrastName[i]
			if i < len(contrastName) - 1:
				conString += '/'
			i = i + 1

		postStats += raw("%s" % conString + "&nbsp &nbsp" +
                                 "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[0]), 'min')) +
                                 " &nbsp " +
                                 "<img src = '" + encodeColorBar() + "'>" +
                                 " &nbsp " +
                                 "%0.3g" % float(getVal(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[0]), 'max')) +
                                 "<br><br>")
		sliceImage = generateSliceImage_SPM(os.path.join(os.path.split(postStatsFilePath)[0], excursionSetNifti[0]))
		postStats += raw("<a href = '" + os.path.join('.', 'Cluster_Data', excursionSetNifti[0].replace('.nii.gz', '.html')) + "'>")
		postStats += img(src = 'data:image/jpg;base64,' + encodeImage(sliceImage).decode())
		postStats += raw("</a>")
			
	postStatsFile = open(postStatsFilePath, "x")
	print(postStats, file = postStatsFile)
	postStatsFile.close()
	
#Attempts to create folder for HTML files, quits program if folder already exists
def createOutputDirectory(outputFolder): 
	
	try:
	
		os.makedirs(outputFolder)
		
	except OSError:
	
		print("Error - %s directory already exists" % outputFolder)
		exit()

#This function generates all pages for display.
def pageGenerate(g, outdir):

        #Specify path names for main pages.
	mainFileName = os.path.join(outdir, "main.html")
	statsFileName = os.path.join(outdir, "stats.html")
	postStatsFileName = os.path.join(outdir, "postStats.html")

	#Create main pages.
	generateStatsHTML(g,statsFileName,postStatsFileName)
	generatePostStatsHTML(g,statsFileName,postStatsFileName)
	generateMainHTML(g,mainFileName,statsFileName,postStatsFileName)

	#Make cluster pages
	os.mkdir(os.path.join(outdir, 'Cluster_Data'))
	excDetails = runQuery(g, os.path.join('..','Queries','selectExcursionSetDetails.txt'), 'Select')
	excNiftiNames = set([excDetails[i] for i in list(range(0, len(excDetails), 3))])

	for excName in excNiftiNames:
	
		excData = formatClusterStats(g, excName)
		generateExcPage(os.path.join(outdir, 'Cluster_Data'), excName.replace(".nii.gz", ""), excData)

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
