import os
import shutil
import sys
import rdflib
import zipfile
import glob
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style
from dominate.util import raw
import errno
import time

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

def formatPeakStats(g, conName):
        #TO BE DELETED EVENTUALLY - WILL BE PART OF formatClusterStats!!
        
        #Query the graph to obtain the cluster index, equivalent Z stat and locations for each peak.
        query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix nidm_coordinateVector: <http://purl.org/nidash/nidm#NIDM_0000086>
               
               SELECT ?clus_index ?peakStat ?loc

               WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                       ?exc prov:atLocation ?conMap . ?clus nidm_clusterLabelID: ?clus_index . ?peak prov:wasDerivedFrom ?clus .
                       ?peak nidm_equivalentZStatistic: ?peakStat . ?peak prov:atLocation ?locObj . ?locObj nidm_coordinateVector: ?loc}
                       
               FILTER(STR(?conMap) = '""" + conName + """'^^xsd:string)}"""

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
                xLocations[i] = float(formattedLoc[0])
                yLocations[i] = float(formattedLoc[1])
                zLocations[i] = float(formattedLoc[2])
        
        #Obtain permutation used to sort the results in order of descending cluster index and then for each cluster by peak statistic size.
        peaksSortPermutation = sorted(range(len(clusterIndices)), reverse = True, key=lambda k: (clusterIndices[k], peaksZstats[k]))

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

def formatClusterStats(g, conName):

        peak_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix prov: <http://www.w3.org/ns/prov#>
               
               SELECT ?peakStat ?clus_index ?loc

               WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                       ?exc prov:atLocation ?conMap . ?clus nidm_clusterLabelID: ?clus_index .
                       ?peak prov:wasDerivedFrom ?clus . ?peak nidm_equivalentZStatistic: ?peakStat .
                       ?peak prov:atLocation ?locObj . ?locObj nidm_coordinateVector: ?loc}

               FILTER(STR(?conMap) = '""" + conName + """'^^xsd:string)}"""

        #Run the peak query
        peakQueryResult = g.query(peak_query)

        #Retrieve query results.
        clusterIndices = [int("%0.0s %s %0.0s" % row) for row in peakQueryResult]
        peakZstats = [float("%s %0.0s %0.0s" % row) for row in peakQueryResult]
        locations = ["%0.0s %0.0s %s" % row for row in peakQueryResult]

        #Create an array for the highest peaks
        highestPeakZArray = [0]*len(set(clusterIndices))
        highestPeakLocations = [0]*len(set(clusterIndices))
        for i in list(range(0, len(peakZstats))):
                if highestPeakZArray[clusterIndices[i]-1] < peakZstats[i]:
                        highestPeakZArray[clusterIndices[i]-1] = peakZstats[i]
                        highestPeakLocations[clusterIndices[i]-1] = locations[i]

        clus_query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix prov: <http://www.w3.org/ns/prov#>
               
               SELECT ?clus_index ?clus_size

               WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                       ?exc prov:atLocation ?conMap . ?clus a nidm_SupraThresholdCluster: .
                       ?clus nidm_clusterLabelID: ?clus_index . ?clus nidm_clusterSizeInVoxels: ?clus_size}

               FILTER(STR(?conMap) = '""" + conName + """'^^xsd:string)}"""

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
        sortedPeakZstats = [highestPeakZArray[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
        sortedPeakLocations = [highestPeakLocations[sortedClusIndicesArray[i]-1] for i in list(range(0, len(clusterIndices)))]
        
        print(sortedClusSizeArray)
        print(sortedClusIndicesArray)
        print(sortedPeakZstats)
        print(sortedPeakLocations)

        return({'clusSizes':sortedClusSizeArray,
                'clusIndices':sortedClusIndicesArray,
                'peakZstats':sortedPeakZstats,
                'peakLocations':sortedPeakLocations})

def createConPage(conName, conData):
        
        print(conData['clusSizes'])
        print(conData['clusIndices'])
        print(conData['peakZstats'])
        print(conData['peakLocations'])

        #Create new document.
        conPage = document(title=conName) #Creates initial HTML page (Post Stats)

        

        

t = time.time()

g = rdflib.Graph()
turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_130_test/nidm.ttl')
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')

g.parse(turtleFile[0], format = "turtle")

#For now using nifti name... want to use proper contrast name field.
conName = "ExcursionSet_T004.nii.gz"
formatPeakStats(g, conName)
print('')
print('')
print('Cluster')
print('')
print('')

t1 = time.time() - t

conData = formatClusterStats(g, conName)

t2 = time.time() - t -  t1

print(t1)
print(t2)

os.mkdir('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_130_test/Contrast_Displays')

createConPage("ExcursionSet_T004", conData)

#shutil.rmtree('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_130_test/Contrast_Displays')
