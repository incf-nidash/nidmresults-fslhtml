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
turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_conjunction_test/nidm.ttl')
#turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_contrast_mask_test/nidm.ttl')

print(turtleFile)
g.parse(turtleFile[0], format = "turtle")
query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
               prefix spm_PartialConjunctionInference: <http://purl.org/nidash/spm#SPM_0000005>
			   prefix dc: <http://purl.org/dc/elements/1.1/>

               SELECT ?image WHERE {{?x a nidm_Inference:} UNION {?x a nidm_ConjunctionInference:} UNION {?x a spm_PartialConjunctionInference:}. ?y prov:wasGeneratedBy ?x . ?y a nidm_ExcursionSetMap: . ?y prov:atLocation ?image}"""

query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
               prefix spm_PartialConjunctionInference: <http://purl.org/nidash/spm#SPM_0000005>

               SELECT ?contrastName WHERE {{?x a nidm_Inference:} UNION {?x a nidm_ConjunctionInference:} UNION {?x a spm_PartialConjunctionInference:}. ?x prov:used ?y .?z prov:wasGeneratedBy ?x . ?z a nidm_ExcursionSetMap: . ?y a nidm_StatisticMap: . ?y nidm_contrastName: ?contrastName .}"""
		
queryResult = g.query(query)
printQuery(queryResult)
