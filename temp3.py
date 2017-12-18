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

g = rdflib.Graph()
turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_130_test/nidm.ttl')
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')

g.parse(turtleFile[0], format = "turtle")

query = """prefix nidm_SupraThresholdCluster: <http://purl.org/nidash/nidm#NIDM_0000070>
               prefix nidm_clusterLabelID: <http://purl.org/nidash/nidm#NIDM_0000082>
               
               SELECT ?clus WHERE {?clus a nidm_SupraThresholdCluster: }"""

queryResult = g.query(query)
printQuery(queryResult)
