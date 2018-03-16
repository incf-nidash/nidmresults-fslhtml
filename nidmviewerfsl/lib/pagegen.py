#!/usr/bin/env python3
# =============================================================================
# This file contains functions used to create the HTML output of the viewer.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet
# =============================================================================
import os
import time
from dominate import document
import shutil
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style, br
from dominate.util import raw
from style.pagestyling import (
    encode_image, encode_color_bar, encode_logo, get_raw_css)
from nidmviewerfsl.lib.slicertools import get_val, generate_slice_image
from nidmviewerfsl.lib.statformat import *
from queries.querytools import run_query


# Generate a page of excursion set peak and cluster statistics
def generate_exc_page(g, outdir, excName, conData):

    # Get the name for the output file.
    outputName = get_clus_filename(g, excName)

    # Create new document.
    excPage = document(title="Cluster List")

    # Work out if we have cluster p value data.
    pDataAvailable = 'clusterPValues' in conData

    # Add CSS stylesheet.
    with excPage.head:
        style(raw(get_raw_css()))

    # Add header and link to main page.
    excPage += raw("<center>")
    excPage += hr()
    excPage += raw("Co-ordinate information for " +
                   outputName.replace('.html', '') +
                   " - ")
    excPage += raw("<a href='./report.html'>back</a>")
    excPage += raw(" to main page")
    excPage += hr()

    # Cluster statistics section.
    excPage += h1("Cluster List")

    # Make the cluster statistics table.
    excPage += raw("<table cellspacing='3' border='3'><tbody>")

    # If we have pvalues for clusters include them.
    if pDataAvailable:
        excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>P</th>"
                       "<th>-log10(P)</th><th>Z-MAX</th><th>Z-MAX X (mm)"
                       "</th><th>Z-MAX Y (mm)</th><th>Z-MAX Z (mm)</th></tr>")
    else:
        excPage += raw("<tr><th>Cluster Index</th><th>Voxels</th><th>Z-MAX"
                       "</th><th>Z-MAX X (mm)</th><th>Z-MAX Y (mm)</th><th>"
                       "Z-MAX Z (mm)</th></tr>")

    # Add the cluster statistics data into the table.
    for cluster in range(0, len(conData['clusSizes'])):

        # New row of cluster data.
        excPage += raw("<tr>")
        excPage += raw("<td>" + str(conData['clusIndices'][cluster]))
        excPage += raw("<td>" + str(conData['clusSizes'][cluster]))

        #If cluster p data is available
        if pDataAvailable:
            excPage += raw("<td>" +
                           ("%.4g" % conData['clusterPValues'][cluster]))
            excPage += raw("<td>" + 
                           ("%.2f" % conData['logClusterPValues'][cluster]))

        excPage += raw("<td>" + str(float('%.2f' % float(
            conData['clusPeakZstats'][cluster]))))

        # Peak location
        formattedLoc = conData['clusPeakLocations'][cluster].replace(
                                                    " ", "").replace(
                                                    "[", "").replace(
                                                    "]", "").split(",")
        excPage += raw("<td>" + '%g' % float(formattedLoc[0]))
        excPage += raw("<td>" + '%g' % float(formattedLoc[1]))
        excPage += raw("<td>" + '%g' % float(formattedLoc[2]))
        excPage += raw("</tr>")

    # Close table
    excPage += raw("</tbody></table>")

    # Formatting
    excPage += br()
    excPage += br()

    # Header
    excPage += h1("Local Maxima")

    # Make the peak statistics table.
    excPage += raw("<table cellspacing='3' border='3'><tbody>")
    excPage += raw("<tr><th>Cluster Index</th><th>Z</th><th>P</th>"
                   "<th>-log10(P)</th><th>x</th><th>y</th><th>z"
                   "</th></tr>")

    # Add the peak statistics data into the table.
    for peak in range(0, len(conData['peakZstats'])):

        # New row of peak data
        excPage += raw("<tr>")
        excPage += raw("<td>" + str(conData['peakClusIndices'][peak]))
        excPage += raw(
            "<td>" +
            str(float('%.2f' % float(conData['peakZstats'][peak]))))
        excPage += raw("<td>" + '%.4g' % float(conData['peakPVals'][peak]))
        excPage += raw("<td>" + '%.2f' % float(
            conData['logPeakPVals'][peak]))

        # Peak location
        formattedLoc = conData['peakLocations'][peak].replace(
            " ", "").replace("[", "").replace("]", "").split(",")

        excPage += raw("<td>" + '%g' % float(formattedLoc[0]))
        excPage += raw("<td>" + '%g' % float(formattedLoc[1]))
        excPage += raw("<td>" + '%g' % float(formattedLoc[2]))
        excPage += raw("</tr>")

    # Close table
    excPage += raw("</tbody></table>")

    # End of page.
    excPage += raw("</center>")

    # Write excPage to a html file.
    excFile = open(os.path.join(outdir, outputName), "x")
    print(excPage, file=excFile)
    excFile.close()


# Generates the main HTML page
def generate_main_html(graph, mainFilePath):

    # Create new document.
    main = document(title="FSL Viewer")

    # Add CSS stylesheet.
    with main.head:
        style(raw(get_raw_css()))

    # Add the logo to the page.
    main += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src'
                '="' + encode_logo() + '" align="right"></a>')

    # Viewer title.
    main += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    # Description of where and when the display was generated
    main += raw(os.path.dirname(mainFilePath)+'<br>')
    main += raw('NIDM-Results display generated on '+time.strftime("%c") +
                '<br>')

    # Links to other pages.
    main += raw('<a href="report_stats.html" target="_top"> Stats </a> - <'
                'a href="report_poststats.html" target="_top"> Post-stats'
                ' </a></div>')

    # Write main page to a HTML file.
    mainFile = open(mainFilePath, "x")
    print(main, file=mainFile)
    mainFile.close()


# Generates the Stats HTML section
def generate_stats_html(graph, statsFilePath, nidmData):

    # Obtain version number.
    softwareLabelNum = run_query(graph, 'selectVersionNum', 'Select')

    # Create new document.
    stats = document(title="FSL Viewer")

    # Add CSS stylesheet.
    with stats.head:
        style(raw(get_raw_css()))

    # Add the logo to the page.
    stats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki"><img src' +
                 '="' + encode_logo() + '" align="right"></a>')

    # Viewer title.
    stats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    # Description of where and when the display was generated
    stats += raw(os.path.dirname(statsFilePath)+'<br>')
    stats += raw('NIDM-Results display generated on ' + time.strftime("%c") +
                 '<br>')

    # Links to other pages.
    stats += raw('<a href="report.html" target="_top"> Up to main page </a> -'
                 ' <a href="report_stats.html" target="_top"> Stats </a> - <a '
                 'href="report_poststats.html" target="_top"> Post-stats </a>'
                 '</div>')

    # Page title.
    stats += h2("Stats")
    stats += hr()

    # Section header.
    stats += h3("Analysis Methods")

    # If SPM was used we should display a string of SPM version number.
    if run_query(graph, 'askSPM', 'Ask'):

        stats += p("FMRI data processing was carried out using SPM Version "
                   "%s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." %
                   softwareLabelNum[1])

    # Otherwise we should display fsl Feat version and software label.
    elif run_query(graph, 'askFSL', 'Ask'):

        fslFeatVersion = run_query(graph, 'selectFslFeatVersion', 'Select')
        stats += p("FMRI data processing was carried out using FEAT (FMRI "
                   "Expert Analysis Tool) Version %s, part of FSL %s (FMRIB'"
                   "s Software Library, www.fmrib.ox.ac.uk/fsl)."
                   % (fslFeatVersion[0], softwareLabelNum[1]))

    stats += hr()

    # Section header.
    stats += h3("Design Matrix")

    # Work out where the design matrix is stored.
    designMatrixLocation = run_query(graph, 'selectDesignMatrixLocation',
                                     'Select')

    # Make a copy of the design matrix csv file in the output folder.
    shutil.copyfile(os.path.join(nidmData, designMatrixLocation[0]),
                    os.path.join(os.path.split(statsFilePath)[0],
                                 designMatrixLocation[0]))

    # Adds design matrix image (as a link) to html page
    stats += a(img(src='data:image/jpg;base64,' + encode_image(
                        os.path.join(nidmData,
                                     designMatrixLocation[1])).decode(),
                   style="border:5px solid black",
                   border=0,
                   width=250),
               href=designMatrixLocation[0])

    # If we are looking at SPM data the contrast vectors are not given in the
    # design matrix image.
    if run_query(graph, 'askSPM', 'Ask'):

        # Add a contrast vector section.
        stats += h3("Contrast Vectors")

        # Get the data
        conData = run_query(graph, 'selectContrastVector', 'Select')
        conNames = list(set([conData[i] for i in range(0, len(conData), 2)]))
        conVal = list(set([conData[i] for i in range(1, len(conData), 2)]))

        # First we must find the min and maximum contrast vector values.
        conVec = [[0]]*len(conNames)
        vmin = 0
        vmax = 1

        # Read in the contrast vectors and check for min/max values.
        for i in range(0, len(conNames)):

            # Read an individual contrast vector
            conVecStr = conVal[i].replace('[', '').replace(
                ']', '').replace(',', '').split()
            conVec[i] = [float(conVecStr[i]) for i in range(0, len(conVecStr))]

            # Update vmin and vmax. This is for the color range of the
            # contrast vector.
            vmin = min(min(np.ones(len(conVec[i]))-conVec[i]), vmin)
            vmax = max(max(np.ones(len(conVec[i]))-conVec[i]), vmax)

        # Then we must display each contrast vector.
        for i in range(0, len(conNames)):

            # Display an image of the contrast vector.
            stats += img(src=contrast_vec(conVec[i], vmin, vmax),
                         style="float:left;margin-right:1em;padding-top:4px;",
                         width="120",
                         height="30")

            # Add contrast name and values
            stats += conNames[i]
            stats += br()
            stats += conVal[i]
            stats += raw("<br><br>")

    stats += br()
    stats += br()

    # Write stats page to HTML file.
    statsFile = open(statsFilePath, "x")
    print(stats, file=statsFile)
    statsFile.close()


# Generates the PostStats HTML page
def generate_poststats_html(graph, postStatsFilePath, nidmData):

    # Work out if there are voxelwise or clusterwise_corrected thresholds.
    voxelWise_corrected = run_query(graph, 'askCHeightThreshold', 'Ask')
    clusterWise_corrected = run_query(graph, 'askCExtentThreshold', 'Ask')
    clusterWise_uncorrected = run_query(graph, 'askUExtentThreshold', 'Ask')

    # Retrieve the software label and name.
    softwareLabelNum = run_query(graph, 'selectVersionNum', 'Select')
    askSPM = run_query(graph, 'askSPM', 'Ask')
    askFSL = run_query(graph, 'askFSL', 'Ask')
    if askSPM:
        softType = 'SPM'
    if askFSL:
        softType = 'FSL'

    # Retrieve and format height threshold statistic type.
    statistic = run_query(graph, 'selectStatisticType', 'Select')
    statistic = statistic_type(statistic[0])
    statisticString = statistic_type_string(statistic)

    # Check if the statistic or P value was used.
    if run_query(graph, 'askIfPValueUncorrected',
                 'Ask') or voxelWise_corrected:
        statistic = "P"

    # Retrieve excursion set details and format them.
    excDetails = run_query(graph, 'selectExcursionSetDetails', 'Select')
    excursionSetNifti = [excDetails[i] for i in list(
        range(0, len(excDetails), 3))]

    excursionSetSliceImage = [excDetails[i] for i in list(
        range(1, len(excDetails), 3))]
    contrastName = [excDetails[i] for i in list(range(2, len(excDetails), 3))]

    # Creates initial HTML page (Post Stats)
    postStats = document(title="FSL Viewer")

    # Add CSS stylesheet.
    with postStats.head:
        style(raw(get_raw_css()))

    # Add the logo to the page.
    postStats += raw('<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki">'
                     '<img src ="' + encode_logo() + '" align="right"></a>')

    # Viewer title.
    postStats += raw('<div align="center"><h1>FSL NIDM-Results Viewer</h1>')

    # Description of where and when the display was generated
    postStats += raw(os.path.dirname(postStatsFilePath)+'<br>')
    postStats += raw('NIDM-Results display generated on ' +
                     time.strftime("%c") +
                     '<br>')

    # Links to other pages.
    postStats += raw('<a href="report.html" target="_top"> Up to main page </a'
                     '> - <a href="report_stats.html" target="_top"> Stats </a'
                     '> - <a href="report_poststats.html" target="_top"> Post-'
                     'stats </a></div>')

    # Page title.
    postStats += h2("Post-stats")
    postStats += hr()

    # Section header.
    postStats += h3("Analysis Methods")
    postStats += raw('<p>')

    # If there is no extent threshold set this to 0.
    extentCorrected = 0

    # Retrieve the extent threshold.
    if clusterWise_corrected:
        extentThreshValue = run_query(graph, 'selectCExtentThreshold',
                                      'Select')
    if clusterWise_uncorrected:
        extentThreshValue = run_query(graph, 'selectUExtentThreshold',
                                      'Select')

    # Retrieve the height threshold.
    heightThreshValue = run_query(graph, 'selectUHeightThreshold', 'Select')
    if heightThreshValue == []:
        heightThreshValue = run_query(graph, 'selectCHeightThreshold',
                                      'Select')

    # Check if the data was generated using SPM or FSL.
    if askSPM:

        postStats += raw("FMRI data processing was carried out using SPM"
                         " Version %s (SPM, http://www.fil.ion.ucl.ac.uk/"
                         "spm/). " % (softwareLabelNum[1]))

    elif askFSL:

        # Work out which FEAT version was used.
        fslFeatVersion = run_query(graph, 'selectFslFeatVersion', 'Select')

        postStats += raw("FMRI data processing was carried out using FEAT"
                         " (FMRI Expert Analysis Tool) Version %s, part of"
                         " FSL %s (FMRIB's Software Library,"
                         " www.fmrib.ox.ac.uk/fsl). " % (
                            fslFeatVersion[0], softwareLabelNum[1]))

    # Now display thresholding details.
    postStats += raw("%s statistic images were thresholded " % (
                     statisticString))

    # If is a corrected extent threshold display it.
    if clusterWise_corrected or clusterWise_uncorrected:

        # If we are using a P value the threshold is equals. e.g. P=0.05.
        # If it's a statistic value then we use greater than. e.g. Z>1.6.
        ineq = '='
        if statistic != 'p' and statistic != 'P':
            ineq = '>'

        # Check to see if corrected.
        corrStr = ' (uncorrected)'
        if clusterWise_corrected:
            corrStr = ' (corrected)'

        postStats += raw("using clusters determined by %s %s %.2g and a"
                         "%s cluster significance of P = %.2g " % (
                            statistic, ineq,
                            float(heightThreshValue[0]),
                            corrStr, float(extentThreshValue[0])))

    # Othewise we only have the height threshold to display.
    else:

        # Check to see if corrected.
        corrStr = '(uncorrected)'
        if voxelWise_corrected:
            corrStr = '(corrected)'
        postStats += raw("at %s = %s %s." % (statistic, float(
                                               '%.2g'
                                               % float(heightThreshValue[0])),
                                             corrStr))

    postStats += raw('</p><hr>')
    postStats += h3("Thresholded Activation Images")
    postStats += hr()

    # Work out if we are looking at a conjunction datapack or not.
    askConjunction = len(list(set(excursionSetNifti))) != len(contrastName)

    # If this is a conjunction we need to initialise an empty string to store
    # contrast names and check for duplicate recordings of niftis.
    if askConjunction:
        conString = ''
        excursionSetNifti = list(set(excursionSetNifti))

    for i in range(0, len(contrastName)):

        # If this isn't a conjunction pack display each image with a contrast
        # name.
        if not askConjunction:

            # Add the colorbar and it's limits.
            postStats += raw(
                "%s" % contrastName[i] + "&nbsp &nbsp" +
                "%0.3g" % float(get_val(os.path.join(
                    nidmData, excursionSetNifti[i]),
                    'min')) +
                " &nbsp " +
                "<img src = '" + encode_color_bar() + "'>" +
                " &nbsp " +
                "%0.3g" % float(get_val(os.path.join(
                    nidmData, excursionSetNifti[i]),
                    'max')) +
                "<br><br>")

            # Add a link to the clusterData page.
            postStats += raw("<a href = '" +
                             os.path.join(
                                '.',
                                get_clus_filename(
                                    graph, excursionSetNifti[i].replace(
                                        '.nii.gz', '')))
                                + "'>")

            # If the slice image already exists add it.
            if (excursionSetSliceImage[
                    i] is not None and os.path.exists(
                        os.path.join(nidmData,
                                     excursionSetSliceImage[i]))):
                postStats += img(
                    src='data:image/jpg;base64,' +
                    encode_image(
                        os.path.join(nidmData,
                                     excursionSetSliceImage[i])
                        ).decode())

            # Otherwise recreate the slice image.
            else:
                sliceImage = generate_slice_image(os.path.join(
                                                nidmData,
                                                excursionSetNifti[i]),
                                                softType)
                postStats += img(src='data:image/jpg;base64,' +
                                 encode_image(sliceImage).decode())

            postStats += raw("</a><br><br>")

        # If this is a conjunction retrieve all the contrast names at once.
        if askConjunction:

            conString += contrastName[i]

            # Add a slash between each contrast name.
            if i < len(contrastName) - 1:
                conString += '/'

    # If we have a conjunction all names are added to one slice image.
    if askConjunction:

        # Add the contrast names and colorbar.
        postStats += raw(
            "%s" % conString + "&nbsp &nbsp" +
            "%0.3g" % float(get_val(os.path.join(
                    nidmData, excursionSetNifti[0]),
                'min')) +
            " &nbsp " +
            "<img src = '" + encode_color_bar() + "'>" +
            " &nbsp " +
            "%0.3g" % float(get_val(os.path.join(
                    nidmData, excursionSetNifti[0]),
                'max')) +
            "<br><br>")

        # Make the slice image.
        sliceImage = generate_slice_image(os.path.join(
                                        nidmData,
                                        excursionSetNifti[0]),
                                        'SPM')

        # Add the link to the cluster data page.
        postStats += raw("<a href = '" + os.path.join(
            '.', get_clus_filename(graph, excursionSetNifti[0].replace(
                                        '.nii.gz', ''))) + "'>")

        # Add the slice image.
        postStats += img(src='data:image/jpg;base64,' + encode_image(
                                                        sliceImage).decode())
        postStats += raw("</a>")

    # Write to the file.
    postStatsFile = open(postStatsFilePath, "x")
    print(postStats, file=postStatsFile)
    postStatsFile.close()


# This function generates all pages for display. It takes as input
# a graph g, an output directory and a path to the NIDM extracted
# data pack.
def page_generate(g, outdir, nidmData):

    # Specify path names for main pages.
    mainFileName = os.path.join(outdir, "report.html")
    statsFileName = os.path.join(outdir, "report_stats.html")
    postStatsFileName = os.path.join(outdir, "report_poststats.html")

    # Create main pages.
    generate_stats_html(g, statsFileName, nidmData)
    generate_poststats_html(g, postStatsFileName, nidmData)
    generate_main_html(g, mainFileName)

    # Make cluster pages
    excDetails = run_query(g, 'selectExcursionSetDetails', 'Select')
    excNiftiNames = set([excDetails[i] for i in list(
        range(0, len(excDetails), 3))])

    for excName in excNiftiNames:

        excData = format_cluster_stats(g, excName)
        generate_exc_page(g, outdir,
                          excName.replace(".nii.gz", ""), excData)
