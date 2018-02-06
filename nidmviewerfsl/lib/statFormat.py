# !/usr/bin/env python3
# ======================================================================
#
# This file contains functions used for formatting statistical data
# returned by SPARQL queries on NIDM-Results packs.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet (10/01/18)
#
# ======================================================================
from queries.queryTools import runQuery


# This function converts obo statistic types into the corresponding statistic.
def statisticImage(stat):

    if stat == "http://purl.obolibrary.org/obo/STATO_0000376":

        return("Z")

    elif stat == "http://purl.obolibrary.org/obo/STATO_0000282":

        return("F")

    elif stat == "http://purl.obolibrary.org/obo/STATO_0000176":

        return("T")

    else:

        return("P")


# This function returns the cluster forming threshold type of an image.
def heightThreshType(graph, imageType):

    if runQuery(graph, 'askIfOboStatistic', 'Ask'):

        return(imageType)

    else:

        return("P")


# This function returns the statistic type of a statistic
def statisticImageString(statImage):

    if statImage == "T":

        return("T")

    elif statImage == "F":

        return("F")

    elif statImage == "Z":

        return("Z (Gaussianised T/F)")


def formatClusterStats(g, excName):

    # ----------------------------------------------------------------------
    # First we gather data for peaks table.
    # ----------------------------------------------------------------------

    # Run the peak query
    peakQueryResult = runQuery(g, 'selectPeakData', 'Select',
                               {'EXC_NAME': excName})

    # Retrieve query results.

    peakZstats = [float(peakQueryResult[i]) for i in list(range(0, len(
                                                    peakQueryResult), 3))]
    clusterIndicesForPeaks = [int(peakQueryResult[i]) for i in list(range(
                                             1, len(peakQueryResult), 3))]
    locations = [peakQueryResult[i] for i in list(range(2, len(
                                                    peakQueryResult), 3))]

    # Obtain permutation used to sort the results in order of descending
    # cluster index and then descending peak statistic size.
    peaksSortPermutation = sorted(range(len(clusterIndicesForPeaks)),
                                  reverse=True,
                                  key=lambda k: (clusterIndicesForPeaks[k],
                                                 peakZstats[k]))

    # Sort all peak data using this permutation.
    sortedPeaksZstatsArray = [peakZstats[i] for i in peaksSortPermutation]
    sortedClusIndicesForPeaks = [
        clusterIndicesForPeaks[i] for i in peaksSortPermutation]
    sortedPeakLocations = [locations[i] for i in peaksSortPermutation]

    # ----------------------------------------------------------------------
    # Second we gather data for cluster table.
    # ----------------------------------------------------------------------

    # Run the cluster query
    clusQueryResult = runQuery(g, 'selectClusterData', 'Select',
                               {'EXC_NAME': excName})

    clusterIndices = [
        int(clusQueryResult[i]) for i in list(
            range(0, len(clusQueryResult), 2))]
    clusterSizes = [
        int(clusQueryResult[i]) for i in list(
            range(1, len(clusQueryResult), 2))]

    # Create an array for the highest peaks.
    highestPeakZArray = [0]*len(clusterIndices)
    highestPeakLocations = [0]*len(clusterIndices)
    for i in list(range(0, len(peakZstats))):
        if highestPeakZArray[clusterIndicesForPeaks[i]-1] < peakZstats[i]:
            highestPeakZArray[clusterIndicesForPeaks[i]-1] = peakZstats[i]
            highestPeakLocations[clusterIndicesForPeaks[i]-1] = locations[i]

    # Obtain permutation used to sort the results in order of descending
    # cluster index and then for each cluster by peak statistic size.
    clusterSortPermutation = sorted(range(len(clusterIndices)),
                                    reverse=True,
                                    key=lambda k: (clusterSizes[k], clusterIndices[k]))

    # Sorted cluster arrays
    sortedClusSizeArray = [clusterSizes[i] for i in clusterSortPermutation]
    sortedClusIndicesArray = [clusterIndices[i] for i in
            clusterSortPermutation]

    # Sort the highest peaks
    sortedMaxPeakZstats = [highestPeakZArray[
                                    sortedClusIndicesArray[i]-1] for i in
                                    list(range(0, len(clusterIndices)))]
    sortedMaxPeakLocations = [highestPeakLocations[
                                    sortedClusIndicesArray[i]-1] for i in
                                    list(range(0, len(clusterIndices)))]

    return({'clusSizes': sortedClusSizeArray,
            'clusIndices': sortedClusIndicesArray,
            'clusPeakZstats': sortedMaxPeakZstats,
            'clusPeakLocations': sortedMaxPeakLocations,
            'peakZstats': sortedPeaksZstatsArray,
            'peakClusIndices': sortedClusIndicesForPeaks,
            'peakLocations': sortedPeakLocations})