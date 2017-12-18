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
	
def formatPeakStats(g, conName):

        #Query the graph to obtain the cluster index, equivalent Z stat and locations for each peak.
        query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_clusterSizeInVoxels: <http://purl.org/nidash/nidm#NIDM_0000084>
               prefix nidm_equivalentZStatistic: <http://purl.org/nidash/nidm#NIDM_0000092>
               prefix nidm_coordinateVector: <http://purl.org/nidash/nidm#NIDM_0000086>
               
               SELECT ?clus_index ?peakStat ?loc

               WHERE {{?exc a nidm_ExcursionSetMap: . ?clus prov:wasDerivedFrom ?exc . ?clus a nidm_SupraThresholdCluster: .
                       ?exc dc:description ?z . ?exc prov:atLocation ?conMap . ?z prov:atLocation ?image .
                       ?clus nidm_clusterLabelID: ?clus_index . ?peak prov:wasDerivedFrom ?clus .
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
        
g = rdflib.Graph()
turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_130_test/nidm.ttl')
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')

g.parse(turtleFile[0], format = "turtle")

conName = "ExcursionSet_T004.nii.gz"
formatPeakStats(g, conName)
