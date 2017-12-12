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
#turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_conjunction_test/nidm.ttl')
turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/fsl_gamma_basis_test/nidm.ttl')

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
			   prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
			   prefix spm_PartialConjunctionInference: <http://purl.org/nidash/spm#SPM_0000005>
               SELECT ?image WHERE {{?x a nidm_Inference:} UNION {?x a nidm_ConjunctionInference:} UNION {?x a spm_PartialConjunctionInference:}. ?y prov:wasGeneratedBy ?x . ?y a nidm_ExcursionSetMap: . ?y prov:atLocation ?image}"""
			   
queryResult = g.query(query)
printQuery(queryResult)

for row in queryResult:
	contrastMapName = "%s" % row
	query2 = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
			   prefix dc: <http://purl.org/dc/elements/1.1/>
               SELECT ?image
               
               WHERE {{?infer a nidm_Inference: . ?exc prov:wasGeneratedBy ?infer . ?exc a nidm_ExcursionSetMap: .
                       ?exc dc:description ?z . ?exc prov:atLocation ?conMap . ?z prov:atLocation ?image}
                       
               FILTER(STR(?conMap) = '""" + contrastMapName + """'^^xsd:string)}"""
	   
	queryResult2 = g.query(query2)
	printQuery(queryResult2)

