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

g = rdflib.Graph()
turtleFile = glob.glob('C:/Users/owner/Downloads/spm12/toolbox/NIDM_display/test/data/fsl_full_examples001_130.nidm/nidm.ttl')

print(turtleFile)
g.parse(turtleFile[0], format = "turtle")

query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
			   prefix dc: <http://purl.org/dc/elements/1.1/>

               SELECT ?image WHERE {?x a nidm_Inference: . ?y prov:wasGeneratedBy ?x . ?y a nidm_ExcursionSetMap: . ?y prov:atLocation ?image .}"""
			
queryResult = g.query(query)
printQuery(queryResult)
