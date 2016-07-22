import rdflib
import markup

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

def addQueryToList(query): #Adds the query results to a list 

	queryList = []
	for i in query:
		
		for j in i:
		
			queryList.append("%s" % j)
		
	return(queryList)
	
def queryVersionNum(graph): #Selects Neuroimaging software version number and name

	query = """prefix nidm: <http://purl.org/nidash/nidm#>
			   prefix prov: <http://www.w3.org/ns/prov#>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               prefix src: <http://scicrunch.org/resolver/>

               SELECT ?label ?versionNum WHERE {?a nidm:NIDM_0000122 ?versionNum . {?a a src:SCR_007037} UNION {?a a src:SCR_002823} OPTIONAL {?a rdfs:label ?label}}"""
			   
	queryResult = graph.query(query)
	
	return(queryResult)

def queryNidmVersionNum(graph): #Selects NIDM exporter version number and name

	query = """prefix nidm: <http://purl.org/nidash/nidm#>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               prefix src: <http://scicrunch.org/resolver/>

               SELECT ?label ?versionNum WHERE { {?a a nidm:NIDM_0000167 .} UNION {?a a nidm:NIDM_0000168 .} ?a nidm:NIDM_0000122 ?versionNum . OPTIONAL {?a rdfs:label ?label .}} """
			   
	queryResult = graph.query(query)
	return(queryResult)

def queryFslFeatVersion(graph):

	query = """prefix fsl_featVersion: <http://purl.org/nidash/fsl#FSL_0000005>
               prefix src_FSL: <http://scicrunch.org/resolver/SCR_002823>

               SELECT ?featVersion WHERE {?x a src_FSL: . ?x fsl_featVersion: ?featVersion .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))
	
def queryExtentThreshold(graph): #Selects Extent Threshold cluster size values

	query = """prefix nidm: <http://purl.org/nidash/nidm#>
			   prefix prov: <http://www.w3.org/ns/prov#>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               prefix src: <http://scicrunch.org/resolver/>

               SELECT ?clusterSize WHERE {?extentThreshold a nidm:NIDM_0000026 . OPTIONAL {?extentThreshold nidm:NIDM_0000084 ?clusterSize}} ORDER BY ?clusterSize"""
			   
	queryResult = graph.query(query)
	return(queryResult)

def generateMainHTML(): #Generates the main HTML page

	mainPage = markup.page()
	mainPage.init(title = "FSL Viewer", css = "viewerStyles.css")
	mainPage.h1("Sample FSL Viewer")
	

def generateStatsHTML(graph): #Generates the Stats HTML section

	softwareLabelNum = queryVersionNum(graph)
	softwareLabelNumList = addQueryToList(softwareLabelNum)
	print(softwareLabelNumList)
	statsPage = markup.page()
	statsPage.init(title = "FSL Viewer")
	statsPage.h2("Stats")
	statsPage.hr()

	statsPage.h3("Analysis methods")
	if softwareLabelNumList[0] == "SPM":
	
		statsPage.p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." % softwareLabelNumList[1])
	
	elif softwareLabelNumList[0] == "FSL":
		
		statsPage.p("FMRI data processing was carried out using...")
		
	
	statsFile = open("stats.html", "w")
	print(statsPage, file = statsFile)
	statsFile.close()
	

	
g = rdflib.Graph()
filepath = input("Please enter NIDM file name")
g.parse(filepath, format = rdflib.util.guess_format(filepath))
x = queryFslFeatVersion(g)
printQuery(x)
page = markup.page()
page.init(title = "Analysis Test", css = "viewerStyles.css")
page.h1("Sample FSL Viewer")
"""for i in y:
	page.p("%s %s" % i)

#fh = open("testhtml.html", "w")
#print(page)	
#print(page, file = fh)
#fh.close()"""


generateStatsHTML(g)


