import os
import shutil
import sys
import rdflib
import zipfile
import glob
from dominate import document
from dominate.tags import p, a, h1, h2, h3, img, ul, li, hr, link, style, br
from dominate.util import raw
import errno
import time
import math

def addQueryToList(query): #Adds the query results to a list 

	queryList = []
	for i in query:
		
		for j in i:
		
			queryList.append("%s" % j)
		
	return(queryList)

def printQuery(query): #Generic function for printing the results of a query - used for testing
	i = 0
	for row in query: 

	#STARTFOR
		i = i+1
		#if len(row) == 1:
			
		print("%s" % row)
		
		#elif len(row) == 2:
		
		#	print("%s, %s" % row)
		
		#elif len(row) == 3:
			
		#	print("%s, %s, %s" % row)
			
		#else:
			
		#	print("Error, not a suitable length")

	print('length: ' + str(i))
	#ENDFOR     

def askCExtentThreshold(graph): #checks for FWE corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
                    prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
                    prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
                    prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
                    prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

                    ASK {?thresh a nidm_ExtentThreshold: . ?thresh a 
                             obo_FWERadjustedpvalue: . ?thresh prov:value ?val

                             FILTER(STR(?val) != "1.0"^^xsd:string)}"""
			   
	queryResult = graph.query(query)
		
	return(queryResult)

def selectCExtentThreshold(graph): #checks for FWE corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
                    prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
                    prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
                    prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

                    SELECT ?val 

                    WHERE {{?thresh a nidm_ExtentThreshold: . ?thresh a obo_FWERadjustedpvalue: .} 
                           ?thresh prov:value ?val .

                           FILTER(STR(?val) != "1.0"^^xsd:string)}"""
			   
	queryResult = graph.query(query)
		
	return(queryResult)

##################################################################################################################################################
outdir = '/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_thr_clustunck10_test/'

g = rdflib.Graph()
turtleFile = glob.glob(os.path.join(outdir, 'nidm.ttl'))
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')
g.parse(turtleFile[0], format = "turtle")
##################################################################################################################################################

printQuery(askCExtentThreshold(g))
printQuery(selectCExtentThreshold(g))
#t2 = time.time() - t
#print(t2)
