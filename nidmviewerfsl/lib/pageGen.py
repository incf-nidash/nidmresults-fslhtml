#!/usr/bin/env python3
#==============================================================================
# This file contains functions used to create the HTML output of the viewer. 
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet
#==============================================================================
import os
import time
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style, br
from dominate.util import raw
from style.pageStyling import encodeImage, encodeColorBar, encodeLogo, getRawCSS
from nidmviewerfsl.lib.slicerTools import getVal, generateSliceImage_SPM
from nidmviewerfsl.lib.statFormat import *
from queries.queryTools import runQuery

#Generate a page of excursion set peak and cluster statistics
def generateExcPage(outdir, excName, conData):

    #Create new document.
    excPage = document(title="Cluster List") 

    #Add CSS stylesheet.
    with excPage.head:
        style(raw(getRawCSS()))

    #Add header and link to main page.
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
    excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>Z-MAX" \
                   "</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>" \
                   "Z-MAX Z (mm)</th></tr>")
    
    #Add the cluster statistics data into the table.
    for cluster in range(0, len(conData['clusSizes'])):

        #New row of cluster data.
        excPage += raw("<tr>")
        excPage += raw("<td>" + str(conData['clusIndices'][cluster]) + 
                       "</td>")
        excPage += raw("<td>" + str(conData['clusSizes'][cluster]) + 
                       "</td>")
        excPage += raw("<td>" + 
         str(float('%.2f' % float(conData['clusPeakZstats'][cluster])))
                       + "</td>")

        #Peak location
        formattedLoc = conData['clusPeakLocations'][cluster].replace(
                                                    " ", "").replace(
                                                    "[", "").replace(
                                                    "]","").split(",")
        excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
        excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
        excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
        excPage += raw("</tr>")

    #Close table
    excPage += raw("</tbody></table>")

    #Formatting
    excPage += br()
    excPage += br()

    #Header
    excPage += h1("Local Maxima")
    
    #Make the peak statistics table.
    excPage += raw("<table cellspacing='3' border='3'><tbody>")
    excPage += raw("<tr><th>Cluster Index</th><th>Z-MAX</th><th>Z-MAX X" \
                   " (mm)</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th>" \
                   "</tr>")

    #Add the peak statistics data into the table.
    for peak in range(0, len(conData['peakZstats'])):

        #New row of peak data
        excPage += raw("<tr>")
        excPage += raw("<td>" + str(conData['peakClusIndices'][peak]) +
                       "</td>")
        excPage += raw("<td>" + 
                   str(float('%.2f' % float(conData['peakZstats'][peak]
                                            ))) + 
                   "</td>")

        #Peak location
        formattedLoc = conData['peakLocations'][peak].replace(" ", ""
                                                    ).replace("[", ""
                                                    ).replace("]",""
                                                    ).split(",")
        excPage += raw("<td>" + str(formattedLoc[0]) + "</td>")
        excPage += raw("<td>" + str(formattedLoc[1]) + "</td>")
        excPage += raw("<td>" + str(formattedLoc[2]) + "</td>")
        excPage += raw("</tr>")

    #Close table
    excPage += raw("</tbody></table>")

    #End of page.
    excPage += raw("</center>")

    #Write excPage to a html file.
    excFile = open(os.path.join(outdir, excName + ".html"), "x")
    print(excPage, file = excFile) 
    excFile.close()  

#Generates the main HTML page
def generateMainHTML(graph, mainFilePath = "Main.html"): 
    
    #Create new document.
    main = document(title="FSL Viewer")

    #Add CSS stylesheet.
    with main.head:
        style(raw(getRawCSS()))

    #Add the logo to the page.
    main += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src' \
                '="' + encodeLogo() + '" align="right"></a>')

    #Viewer title.
    main += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    #Description of where and when the display was generated
    main += raw(os.path.dirname(mainFilePath)+'<br>')
    main += raw('NIDM-Results display generated on '+time.strftime("%c") +
                '<br>')

    #Links to other pages.
    main += raw('<a href="stats.html" target="_top"> Stats </a> - <' \
                'a href="postStats.html" target="_top"> Post-stats </a></div>')

    #Write main page to a HTML file.
    mainFile = open(mainFilePath, "x")
    print(main, file = mainFile)
    mainFile.close()

#Generates the Stats HTML section
def generateStatsHTML(graph,statsFilePath = "stats.html"):
    
    #Obtain version number.
    softwareLabelNum = runQuery(graph, 'selectVersionNum', 'Select')
    
    #Create new document.
    stats = document(title="FSL Viewer") 

    #Add CSS stylesheet.
    with stats.head:
        style(raw(getRawCSS()))

    #Add the logo to the page.
    stats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src' +
                 '="' + encodeLogo() + '" align="right"></a>')

    #Viewer title.
    stats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    #Description of where and when the display was generated
    stats += raw(os.path.dirname(statsFilePath)+'<br>')
    stats += raw('NIDM-Results display generated on '+time.strftime("%c")+
                 '<br>')

    #Links to other pages.
    stats += raw('<a href="main.html" target="_top"> Up to main page </a> -' \
                 ' <a href="stats.html" target="_top"> Stats </a> - <a ' \
                 'href="postStats.html" target="_top"> Post-stats </a></div>')

    #Page title.
    stats += h2("Stats")
    stats += hr()

    #Section header.
    stats += h3("Analysis Methods")
    
    #If SPM was used we should display a string of SPM version number.
    if runQuery(graph, 'askSPM', 'Ask') == True: 
        
        stats += p("FMRI data processing was carried out using SPM Version " \
                   "%s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." % 
                   softwareLabelNum[1])
    
    #Otherwise we should display fsl Feat version and software label.
    elif runQuery(graph, 'askFSL', 'Ask') == True: 
        
        fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')
        stats += p("FMRI data processing was carried out using FEAT (FMRI " \
                   "Expert Analysis Tool) Version %s, part of FSL %s (FMRIB'" \
                   "s Software Library, www.fmrib.ox.ac.uk/fsl)." 
                   % (fslFeatVersion[0], softwareLabelNum[1]))
        
    stats += hr()

    #Section header.
    stats += h3("Design Matrix")
    
    #Work out where the design matrix is stored.
    designMatrixLocation = runQuery(graph, 'selectDesignMatrixLocation', 
                                    'Select')
    
    #Adds design matrix image (as a link) to html page
    stats += a(img(src = designMatrixLocation[1], style = 
                   "border:5px solid black", border = 0, width = 250), href = 
                   designMatrixLocation[0]) 
    
    #Write stats page to HTML file.
    statsFile = open(statsFilePath, "x")
    print(stats, file = statsFile) 
    statsFile.close()

#Generates the PostStats HTML page
def generatePostStatsHTML(graph, postStatsFilePath = "postStats.html"): 

    #Work out if there are voxelwise or clusterwise_corrected thresholds.
    voxelWise_corrected = runQuery(graph, 'askCHeightThreshold', 'Ask')
    clusterWise_corrected = runQuery(graph, 'askCExtentThreshold', 'Ask')
    clusterWise_uncorrected = runQuery(graph, 'askUExtentThreshold', 'Ask')

    #Retrieve the software label.
    softwareLabelNum = runQuery(graph, 'selectVersionNum', 'Select')

    #Retrieve and format height threshold statistic type.
    statisticType = runQuery(graph, 'selectStatisticType', 'Select')
    statisticType = statisticImage(statisticType[0])
    statisticTypeString = statisticImageString(statisticType)

    #Retrieve excursion set details and format them.
    excDetails = runQuery(graph, 'selectExcursionSetDetails', 'Select')
    excursionSetNifti = list(set([excDetails[i] for i in list(range(0, 
                             len(excDetails), 3))]))
    excursionSetSliceImage = [excDetails[i] for i in list(range(1, 
                             len(excDetails), 3))]
    contrastName = [excDetails[i] for i in list(range(2, len(excDetails), 3))]

    #Creates initial HTML page (Post Stats)
    postStats = document(title="FSL Viewer") 

    #Add CSS stylesheet.
    with postStats.head:
        style(raw(getRawCSS()))

    #Add the logo to the page.
    postStats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki">' \
                     '<img src ="' + encodeLogo() + '" align="right"></a>')

    #Viewer title.
    postStats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    #Description of where and when the display was generated
    postStats += raw(os.path.dirname(postStatsFilePath)+'<br>')
    postStats += raw('NIDM-Results display generated on '+time.strftime("%c")
                     +'<br>')

    #Links to other pages.
    postStats += raw('<a href="main.html" target="_top"> Up to main page </a' \
                     '> - <a href="stats.html" target="_top"> Stats </a> - <' \
                     'a href="postStats.html" target="_top"> Post-stats </a>' \
                     '</div>')

    #Page title.
    postStats += h2("Post-stats")
    postStats += hr()

    #Section header.
    postStats += h3("Analysis Methods")

    #==========================================================================
    #WIP
    postStats += raw('<p>')

    print(postStatsFilePath)
    print("voxelwise_corrected")
    print(voxelWise_corrected)
    print("clusterwise_corrected")
    print(clusterWise_corrected)

    #If there is no extent threshold set this to 0.
    extentCorrected = 0

    #Retrieve the extent threshold.
    extentThreshValue = runQuery(graph, 'selectUExtentThreshold', 'Select')
    print("uncorrected extent")
    print(extentThreshValue)
    if extentThreshValue == []:
        extentThreshValue = runQuery(graph, 'selectCExtentThreshold', 'Select')

    print(clusterWise_corrected or clusterWise_uncorrected)
    print("extentThreshValue")
    print(extentThreshValue)

    #Retrieve the height threshold.
    heightThreshValue = runQuery(graph, 'selectUHeightThreshold', 'Select')   
    if heightThreshValue == []:
        heightThreshValue = runQuery(graph, 'selectCHeightThreshold', 
            'Select')

    #Check if the data was generated using SPM or FSL.
    if runQuery(graph, 'askSPM', 'Ask') == True:
            
        postStats += raw("FMRI data processing was carried out using SPM" \
                         " Version %s (SPM, http://www.fil.ion.ucl.ac.uk/" \
                         "spm/). " % (softwareLabelNum[1]))

    elif runQuery(graph, 'askFSL', 'Ask') == True:

        #Work out which FEAT version was used.
        fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')

        postStats += raw("FMRI data processing was carried out using FEAT" \
                       " (FMRI Expert Analysis Tool) Version %s, part of" \
                       " FSL %s (FMRIB's Software Library," \
                       " www.fmrib.ox.ac.uk/fsl). " %(fslFeatVersion[0], 
                        softwareLabelNum[1]))
    
    #Now display thresholding details.
    postStats += raw("%s statistic images were thresholded " % (
                     statisticTypeString))

    #If is a corrected extent threshold display it. 
    if clusterWise_corrected or clusterWise_uncorrected: 

        #Check to see if corrected.
        corrStr = ''
        if clusterWise_corrected:
            corrStr = '(corrected)'

        postStats += raw("using clusters determined by %s < %s and a" \
                       " %s cluster significance of P = %s " % (
                        statisticType, heightThreshValue[0], 
                        corrStr, extentThreshValue[0]))

    #Othewise we only have a height threshold to display.
    else:

        #Check to see if corrected.
        corrStr = '(uncorrected)'
        if voxelWise_corrected:
            corrStr = '(corrected)'

        postStats += raw("at %s = %s %s" % (statisticType, float('%.2g' 
                         % float(heightThreshValue[0])), corrStr))


    postStats += raw('</p>')

    #=====================================================================

    #If there is a Height Threshold display it.
    if voxelWise_corrected == True: 

        #Retrieve threshold value. 
        mainThreshValue = runQuery(graph, 'selectCHeightThreshold', 'Select')

        #If the data was generated using SPM display a string detailing which 
        #version of spm was used.
        if runQuery(graph, 'askSPM', 'Ask') == True:
            
            postStats += p("FMRI data processing was carried out using SPM" \
                           " Version %s (SPM, http://www.fil.ion.ucl.ac.uk/" \
                           "spm/). %s statistic images were thresholded at P" \
                           " = %s (corrected)" % (softwareLabelNum[1], 
                           statisticTypeString, mainThreshValue[0]))
        
        #If the data was generated using FSL display a string detailing which 
        #version of spm was used.
        elif runQuery(graph, 'askFSL', 'Ask') == True:

            #Work out which FEAT version was used.
            fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')

            postStats += p("FMRI data processing was carried out using FEAT" \
                           " (FMRI Expert Analysis Tool) Version %s, part of" \
                           " FSL %s (FMRIB's Software Library," \
                           " www.fmrib.ox.ac.uk/fsl). %s statistic images we" \
                           "re thresholded at P = %s (corrected)" 
                           %(fslFeatVersion[0], softwareLabelNum[1], 
                            statisticTypeString, mainThreshValue[0]))

    else: #If there is no corrected threshold - assume voxel wise
        mainThreshValue = runQuery(graph, 'selectUHeightThreshold', 'Select')
        #SPM used and threshold type is nidm_PValueUncorrected
        if runQuery(graph, 'askSPM', 'Ask') == True and runQuery(graph, 'askIfPValueUncorrected', 'Ask') == True: 
            postStats += p("FMRI data processing was carried out using SPM" \
                           " Version %s (SPM, http://www.fil.ion.ucl.ac.uk/" \
                           "spm/). %s statistic images were thresholded at P" \
                           " = %s (uncorrected)" % (softwareLabelNum[1], 
                            statisticTypeString, float('%.2g' % float(
                            mainThreshValue[0]))))
            
        #SPM used and threshold type is obo_statistic
        elif runQuery(graph, 'askSPM', 'Ask') == True and runQuery(graph, 'askIfOboStatistic', 'Ask') == True: 
            postStats += p("FMRI data processing was carried out using SPM " \
                           "Version %s (SPM, http://www.fil.ion.ucl.ac.uk/" \
                           "spm/). %s statistic images were thresholded at" \
                           " %s = %s (uncorrected)" % (softwareLabelNum[1],
                           statisticTypeString, statisticType, float('%.2g' 
                           % float(mainThreshValue[0]))))
            
        
        elif runQuery(graph, 'askFSL', 'Ask') == True and runQuery(graph, 'askIfPValueUncorrected', 'Ask') == True:
            
            fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')
            postStats += p("FMRI data processing was carried out using FEAT " \
                           "(FMRI Expert Analysis Tool) Version %s, part of " \
                           "FSL %s (FMRIB's Software Library, www.fmrib.ox" \
                           ".ac.uk/fsl). %s statistic images were thresholde" \
                           "d at P = %s (uncorrected)." % (fslFeatVersion[0], 
                            softwareLabelNum[1], statisticTypeString, 
                            mainThreshValue[0]))
            
            
        elif runQuery(graph, 'askFSL', 'Ask') == True and runQuery(graph, 'askIfOboStatistic', 'Ask') == True:
            
            fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')
            postStats += p("FMRI data processing was carried out using FEAT" \
                           " (FMRI Expert Analysis Tool) Version %s, part " \
                           "of FSL %s (FMRIB's Software Library, www.fmrib.o" \
                           "x.ac.uk/fsl). %s statistic images were threshold" \
                           "ed at %s = %s (uncorrected)." % (fslFeatVersion[0],
                           softwareLabelNum[1], statisticTypeString, 
                           statisticType, mainThreshValue[0]))
    
    #If is an extent threshold display it. 
    if clusterWise_corrected == True: 

        
        mainThreshValue = runQuery(graph, 'selectCExtentThreshold', 'Select')
        heightThreshValue = runQuery(graph, 'selectUHeightThreshold', 'Select')
        if heightThreshValue == []:
            heightThreshValue = runQuery(graph, 'selectCHeightThreshold', 'Select')
        clusterThreshType = heightThreshType(graph, statisticType)
        
        if runQuery(graph, 'askSPM', 'Ask') == True:
            
            postStats += p("FMRI data processing was carried out using SPM" \
                           " Version %s (SPM, http://www.fil.ion.ucl.ac.uk/" \
                           "spm/). %s statistic images were thresholded usin" \
                           "g clusters determined by %s > %s and a (correcte" \
                           "d) cluster significance of P = %s " % (
                            softwareLabelNum[1], statisticTypeString, 
                            clusterThreshType, heightThreshValue[0], 
                            mainThreshValue[0]))
    
        elif runQuery(graph, 'askFSL', 'Ask') == True:
            fslFeatVersion = runQuery(graph, 'selectFslFeatVersion', 'Select')
            postStats += p("FMRI data processing was carried out using FEAT" \
                           " (FMRI Expert Analysis Tool) Version %s, part of" \
                           " FSL %s (FMRIB's Software Library, " \
                           "www.fmrib.ox.ac.uk/fsl). %s statistic images" \
                           " were thresholded using clusters determined by" \
                           " %s > %s and a (corrected) cluster significance" \
                           "of P = %s" 
                           %(fslFeatVersion[0], softwareLabelNum[1], 
                             statisticTypeString, clusterThreshType, 
                             heightThreshValue[0], mainThreshValue[0]))
            
        
    
    postStats += hr()
    postStats += h3("Thresholded Activation Images")
    postStats += hr()
    i = 0
    
    if runQuery(graph, 'askFSL', 'Ask') == True:
    
        while i < len(contrastName):
        
            #Colorbar and colorbar limits.
            postStats += raw("%s" % contrastName[i] + "&nbsp &nbsp" +
                             "%0.3g" % float(getVal(os.path.join(os.path.split(
                             postStatsFilePath)[0], excursionSetNifti[i]), 
                             'min')) +
                             " &nbsp " +
                             "<img src = '" + encodeColorBar() + "'>" +
                             " &nbsp " +
                             "%0.3g" % float(getVal(os.path.join(os.path.split(
                             postStatsFilePath)[0], excursionSetNifti[i]), 
                             'max')) +
                             "<br><br>")
            postStats += raw("<a href = '" + 
                             os.path.join('.', 'Cluster_Data', 
                                excursionSetNifti[i].replace('.nii.gz', '.html'
                             )) 
                             + "'>")
            postStats += img(src = 'data:image/jpg;base64,' + 
                             encodeImage(os.path.join(os.path.split(
                                postStatsFilePath)[0],excursionSetSliceImage[i]
                             )).decode())
            postStats += raw("</a>")
            postStats += br()
            postStats += br()
            i = i + 1

    if runQuery(graph, 'askSPM', 'Ask') == True and len(excursionSetNifti) == len(contrastName):
    
        while i < len(excursionSetNifti):
        
            postStats += raw("%s" % contrastName[i] + "&nbsp &nbsp" +
                             "%0.3g" % float(getVal(os.path.join(os.path.split(
                             postStatsFilePath)[0], excursionSetNifti[i]), 
                             'min')) +
                             " &nbsp " +
                             "<img src = '" + encodeColorBar() + "'>" +
                             " &nbsp " +
                             "%0.3g" % float(getVal(os.path.join(os.path.split(
                             postStatsFilePath)[0], excursionSetNifti[i]), 
                             'max')) +
                             "<br><br>")
            sliceImage = generateSliceImage_SPM(os.path.join(os.path.split(
                postStatsFilePath)[0], excursionSetNifti[i]))
            postStats += raw("<a href = '" + os.path.join('.', 'Cluster_Data', 
                excursionSetNifti[i].replace('.nii.gz', '.html')) + "'>")
            postStats += img(src = 'data:image/jpg;base64,' + encodeImage(
                sliceImage).decode())
            postStats += raw("</a>")
            i = i + 1

    if runQuery(graph, 'askSPM', 'Ask') == True and len(excursionSetNifti) < len(contrastName):
        
        conString = 'Conjunction : '
        
        while i < len(contrastName):
        
            conString += contrastName[i]
            if i < len(contrastName) - 1:
                conString += '/'
            i = i + 1

        postStats += raw("%s" % conString + "&nbsp &nbsp" +
                         "%0.3g" % float(getVal(os.path.join(os.path.split(
                         postStatsFilePath)[0], excursionSetNifti[0]), 'min'))+
                         " &nbsp " +
                         "<img src = '" + encodeColorBar() + "'>" +
                         " &nbsp " +
                         "%0.3g" % float(getVal(os.path.join(os.path.split(
                         postStatsFilePath)[0], excursionSetNifti[0]), 'max'))+
                         "<br><br>")
        sliceImage = generateSliceImage_SPM(os.path.join(os.path.split(
            postStatsFilePath)[0], excursionSetNifti[0]))
        postStats += raw("<a href = '" + os.path.join('.', 'Cluster_Data', 
            excursionSetNifti[0].replace('.nii.gz', '.html')) + "'>")
        postStats += img(src = 'data:image/jpg;base64,' + encodeImage(
            sliceImage).decode())
        postStats += raw("</a>")
            
    postStatsFile = open(postStatsFilePath, "x")
    print(postStats, file = postStatsFile)
    postStatsFile.close()

#This function generates all pages for display.
def pageGenerate(g, outdir):

        #Specify path names for main pages.
    mainFileName = os.path.join(outdir, "main.html")
    statsFileName = os.path.join(outdir, "stats.html")
    postStatsFileName = os.path.join(outdir, "postStats.html")

    #Create main pages.
    generateStatsHTML(g,statsFileName)
    generatePostStatsHTML(g,postStatsFileName)
    generateMainHTML(g,mainFileName)

    #Make cluster pages
    os.mkdir(os.path.join(outdir, 'Cluster_Data'))
    excDetails = runQuery(g, 'selectExcursionSetDetails', 'Select')
    excNiftiNames = set([excDetails[i] for i in list(range(0, 
                                                len(excDetails), 3))])

    for excName in excNiftiNames:
    
        excData = formatClusterStats(g, excName)
        generateExcPage(os.path.join(outdir, 'Cluster_Data'), 
                        excName.replace(".nii.gz", ""), excData)