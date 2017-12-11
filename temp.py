import os
import shutil
import sys
import rdflib
import zipfile
import glob
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr
import errno

def printQuery(query): #Generic function for printing the results of a query - used for testing
	i = 0
	for row in query: 

	#STARTFOR
		i = i+1
		if len(row) == 1:
			
			print("%s" % row)
		
		elif len(row) == 2:
		
			print("%s, %s" % row)
		
		elif len(row) == 3:
			
			print("%s, %s, %s" % row)
			
		else:
			
			print("Error, not a suitable length")

	print('length: ' + str(i))
	#ENDFOR

def formatPeakStats(g):

        #Query the graph to obtain the cluster index, equivalent Z stat and locations for each peak.
        query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_coordinateVector: <http://purl.org/nidash/nidm#NIDM_0000086>
               
               SELECT ?clus_index ?peakStat ?loc WHERE {?clus a nidm_SupraThresholdCluster: . ?clus nidm_clusterLabelID: ?clus_index . ?peak prov:wasDerivedFrom ?clus . ?peak nidm_equivalentZStatistic: ?peakStat . ?peak prov:atLocation ?locObj . ?locObj nidm_coordinateVector: ?loc}"""

        #Run the query
        queryResult = g.query(query)

        #Read in the cluster indices, peak values, x coordinates, y coordinates and z coordinates.
        clusterIndices = [int("%s %0.0s %0.0s" % row) for row in queryResult]
        peaksZstats = [float("%0.0s %s %0.0s" % row) for row in queryResult]
        locations = ["%0.0s %0.0s %s" % row for row in queryResult]

        #Create arrays for each coordinate of peaks locations.
        xLocations = [None]*len(locations)
        yLocations = [None]*len(locations)
        zLocations = [None]*len(locations)
        for i in list(range(0, len(locations))):
                formattedLoc = locations[i].replace(" ", "").replace("[", "").replace("]","").split(",")
                xLocations[i] = int(formattedLoc[0])
                yLocations[i] = int(formattedLoc[1])
                zLocations[i] = int(formattedLoc[2])
        
        #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
        peaksSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: (-clusterIndices[k], peaksZstats[k]))

        #Sort all peak data using this permutation.
        sortedPeaksZstatsArray = [peaksZstats[i] for i in peaksSortPermutation]
        sortedClusArray = [clusterIndices[i] for i in peaksSortPermutation]
        sortedxLocationsArray = [xLocations[i] for i in peaksSortPermutation]
        sortedyLocationsArray = [yLocations[i] for i in peaksSortPermutation]
        sortedzLocationsArray = [zLocations[i] for i in peaksSortPermutation]

        
        print(sortedPeaksZstatsArray)
        print(sortedClusArray)
        print(sortedxLocationsArray)
        print(sortedyLocationsArray)
        print(sortedzLocationsArray)

def formatClusterStats(g):

        peak_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix prov: <http://www.w3.org/ns/prov#>
               
               SELECT ?peakStat ?clus_index WHERE {?clus a nidm_SupraThresholdCluster: . ?clus nidm_clusterLabelID: ?clus_index . ?peak prov:wasDerivedFrom ?clus . ?peak nidm_equivalentZStatistic: ?peakStat}"""

        #Run the peak query
        peakQueryResult = g.query(peak_query)

        #Retrieve query results.
        clusterIndices = [int("%0.0s %s" % row) for row in peakQueryResult]
        peakZstats = [float("%s %0.0s" % row) for row in peakQueryResult]

        #Create an array for the highest peaks
        highestPeakArray = [0]*len(set(clusterIndices))
        for i in list(range(0, len(peakZstats))):
                if highestPeakArray[clusterIndices[i]-1] < peakZstats[i]:
                        highestPeakArray[clusterIndices[i]-1] = peakZstats[i]

        clus_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix prov: <http://www.w3.org/ns/prov#>
               
               SELECT ?clus_index ?clus_size WHERE {?clus a nidm_SupraThresholdCluster: . ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size}"""

        #Run the cluster query
        clusQueryResult = g.query(clus_query)

        #Retrieve query results.
        clusterIndices = [int("%s %0.0s" % row) for row in clusQueryResult]
        clusterSizes = [int("%0.0s %s" % row) for row in clusQueryResult]

        #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
        clusterSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: clusterSizes[k])

        #Sorted cluster arrays
        sortedClusSizeArray = [clusterSizes[i] for i in clusterSortPermutation]
        sortedClusIndicesArray = [clusterIndices[i] for i in clusterSortPermutation]

        #Sort the highest peaks
        sortedPeakZstats = [highestPeakArray[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
        
        print(sortedClusSizeArray)
        print(sortedClusIndicesArray)
        print(sortedPeakZstats)

        #Obtain cluster information and peaks from clusters
        #clusterSizes = [int("%s %0.0s %0.0s" % row) for row in queryResult]
        #clusterIndices = [int("%0.0s %s %0.0s" % row) for row in queryResult]
        #peaksZstats = [float("%0.0s %0.0s %s" % row) for row in queryResult]

        #Order by cluster size and peak value
        #peaksSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: (clusterSizes[k], peaksZstats[k]))

        #Sort all cluster data using this permutation.
        #sortedPeaksZstatsArray = [peaksZstats[i] for i in peaksSortPermutation]
        #sortedClusIndexArray = [clusterIndices[i] for i in peaksSortPermutation]
        #sortedClusSizeArray = [clusterSizes[i] for i in peaksSortPermutation]
        
        #We only want the highest peaks for the cluster table. Everything else can be discarded.
        #highestPeakIndexArray = [None]*len(set(clusterIndices))
        #previousIndex = -1
        #j = 0
        #for i in list(range(0, len(peaksZstats))):
        #        if previousIndex != sortedClusIndexArray[i]:
        #                highestPeakIndexArray[j] = i
        #                print(sortedClusIndexArray[i])
        #                j += 1
        #                previousIndex = sortedClusIndexArray[i]

        #Now we reduce to the values we only need.
        #sortedPeaksZstatsArray = [sortedPeaksZstatsArray[i] for i in highestPeakIndexArray]
        #sortedClusIndexArray = [sortedClusIndexArray[i] for i in highestPeakIndexArray]
        #sortedClusSizeArray = [sortedClusSizeArray[i] for i in highestPeakIndexArray]

        #print(sortedPeaksZstatsArray)
        #print(sortedClusIndexArray)
        #print(sortedClusSizeArray)
                



g = rdflib.Graph()
#turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_conjunction_test/nidm.ttl')
turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')

print(turtleFile)
g.parse(turtleFile[0], format = "turtle")



############################################################################################################################

query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               
               SELECT ?clus_index WHERE {?clus a nidm_SupraThresholdCluster: . ?clus nidm_clusterLabelID: ?clus_index}"""

############################################################################################################################

query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
        prefix prov: <http://www.w3.org/ns/prov#>
               
               SELECT ?clus_size ?clus_index ?peakStat WHERE {?clus a nidm_SupraThresholdCluster: . ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size . ?peak prov:wasDerivedFrom ?clus . ?peak nidm_equivalentZStatistic: ?peakStat}"""


queryResult = g.query(query)
printQuery(queryResult)
#formatClusterStats(queryResult)
print()
print()
#unsortedArray = convertToArray(queryResult, 'int')
#sortPermutation = sorted(range(len(unsortedArray)), reverse = True, key=lambda k: unsortedArray[k])
#print(sortPermutation)

formatClusterStats(g)

#sortedArray = [unsortedArray[i] for i in sortPermutation]
print()
print()
#print(sortedArray)
