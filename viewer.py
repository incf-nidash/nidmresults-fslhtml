import rdflib
import markup
from markup import oneliner as e
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
	
def askSpm(graph): #Checks if SPM was used

	querySpm = graph.query("""prefix nidm_NeuroimagingAnalysisSoftware: <http://purl.org/nidash/nidm#NIDM_0000164>
                              prefix prov: <http://www.w3.org/ns/prov#>
                              prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                              prefix src_SPM: <http://scicrunch.org/resolver/SCR_007037>

                              ASK {?a a src_SPM:}""")
				  
	for row in querySpm:
		querySpmResult = row
	
	if querySpmResult == True:
		
		return(True)
	
	else:
		
		return(False)
		
def askFsl(graph): #Checks is FSL was used

	queryFsl = graph.query("""prefix nidm_NeuroimagingAnalysisSoftware: <http://purl.org/nidash/nidm#NIDM_0000164>
                              prefix prov: <http://www.w3.org/ns/prov#>
                              prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                              prefix src_FSL: <http://scicrunch.org/resolver/SCR_002823>

                              ASK {?a a src_FSL:}""")
				  
	for row in queryFsl:
		queryFslResult = row
	
	if queryFslResult == True:
		
		return(True)
	
	else:
		
		return(False)	
	
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

def queryFslFeatVersion(graph): #Selects FSL FEAT Version Number

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

def queryDesignMatrixLocation(graph): #Selects location of design matrix

	query = """prefix nidm_DesignMatrix:<http://purl.org/nidash/nidm#NIDM_0000019>
               prefix dc: <http://purl.org/dc/elements/1.1/>
               prefix prov: <http://www.w3.org/ns/prov#>
			   prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

               SELECT ?csv ?location WHERE {?x a nidm_DesignMatrix: . ?x dc:description ?y . ?y prov:atLocation ?location . ?x prov:atLocation ?csv .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def queryStatisticType(graph): #Checks Statistic Map Type

	query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_statisticType: <http://purl.org/nidash/nidm#NIDM_0000123>
			   prefix nidm_statisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               prefix obo_tstatistic: <http://purl.obolibrary.org/obo/STATO_0000176>
               prefix obo_Fstatistic: <http://purl.obolibrary.org/obo/STATO_0000282>
               prefix obo_Zstatistic: <http://purl.obolibrary.org/obo/STATO_0000376>

               SELECT ?statType WHERE {?y a nidm_Inference: . ?y prov:used ?x . ?x a nidm_statisticMap: . ?x nidm_statisticType: ?statType .}"""
			   
	queryResult = graph.query(query)
	for i in queryResult:
		print(i)
	return(addQueryToList(queryResult))

def statisticImage(stat): #Returns type of statistic image

	if stat == "http://purl.obolibrary.org/obo/STATO_0000176":
	
		return("Z")
	
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000282":
	
		return("F")
		
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000376":
	
		return("T")
		
	else:
		
		return(None)
def checkHeightThreshold(graph): #checks for corrected height threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               ASK {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_HeightThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_HeightThreshold: . ?x a obo_FWERadjustedpvalue: .}}"""
			   
	queryResult = graph.query(query)
	for row in queryResult:
		
		answer = row
		
	return(answer)

def checkExtentThreshold(graph): #checks for corrected extent threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               ASK {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_ExtentThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_ExtentThreshold: . ?x a obo_FWERadjustedpvalue: .}}"""
			   
	queryResult = graph.query(query)
	for row in queryResult:
		
		answer = row
		
	return(answer)
	
def selectExtentThreshValue(graph): #selects the value of the extent threshold used by nidm_Inference

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               SELECT ?thresholdValue WHERE {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_ExtentThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_ExtentThreshold: . ?x a obo_FWERadjustedpvalue: .} ?x prov:value ?thresholdValue .}"""
	
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def checkFirstLevel(graph): #Checks if first-level analysis
	answer = True
	query = """prefix nidm_DesignMatrix: <http://purl.org/nidash/nidm#NIDM_0000019>
               prefix nidm_regressorNames: <http://purl.org/nidash/nidm#NIDM_0000021>
               prefix nidm_hasDriftModel: <http://purl.org/nidash/nidm#NIDM_0000088>

               ASK {?x a nidm_DesignMatrix: . {?x nidm_regressorNames: ?y .} UNION {?x nidm_hasDriftModel: ?y .} }"""
			   
	queryResult = graph.query(query)
	for row in queryResult:
	
		answer = row

	return(answer)

def queryClusterThresholdValue(graph): #Selects the value of the main threshold if cluster-wise

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_ExtentThreshold: <http://purl.org/nidash/nidm#NIDM_0000026>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

              SELECT ?thresholdValue WHERE {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_ExtentThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_ExtentThreshold: . ?x a obo_FWERadjustedpvalue: .} ?x prov:value ?thresholdValue .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def queryHeightThresholdValue(graph):

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               SELECT ?value WHERE {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_HeightThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_HeightThreshold: . ?x a obo_FWERadjustedpvalue: .} ?x prov:value ?value .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))
	
def checkVoxelOrClusterThreshold(graph):

	print("Test")

def generateMainHTML(graph): #Generates the main HTML page

	mainPage = markup.page()
	mainPage.init(title = "FSL Viewer", css = "viewerStyles.css")
	mainPage.h1("Sample FSL Viewer")
	#mainPage.div(e.a("Stats", href = "stats.html"))
	#mainPage.div(e.a("Post Stats", href = "postStats.html"))
	mainPage.ul()
	mainPage.li(e.a("Stats", href = "stats.html"))
	mainPage.li("-")
	mainPage.li(e.a("Post Stats", href = "postStats.html"))
	mainPage.ul.close()
	mainFile = open("Main.html", "w")
	print(mainPage, file = mainFile)
	mainFile.close()

def generateStatsHTML(graph): #Generates the Stats HTML section
	firstLevel = checkFirstLevel(graph)
	softwareLabelNum = queryVersionNum(graph)
	softwareLabelNumList = addQueryToList(softwareLabelNum)
	statsPage = markup.page()
	statsPage.init(title = "FSL Viewer", css = "viewerStyles.css")
	statsPage.h1("Sample FSL Viewer")
	statsPage.ul()
	statsPage.li(e.a("Stats", href = "stats.html"))
	statsPage.li("-")
	statsPage.li(e.a("Post Stats", href = "postStats.html"))
	statsPage.ul.close()
	statsPage.h2("Stats")
	statsPage.hr()

	statsPage.h3("Analysis methods")
	if askSpm(graph) == True: #Checks if SPM was used
	
		statsPage.p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." % softwareLabelNumList[1])
	
	elif askFsl(graph) == True: #Checks if FSL was used
		
		fslFeatVersion = queryFslFeatVersion(graph)
		statsPage.p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)." % (fslFeatVersion[0], softwareLabelNumList[1]))
		
	statsPage.hr()
	statsPage.h3("Design Matrix")
	designMatrixLocation = queryDesignMatrixLocation(g)
	statsPage.a(e.img(src = designMatrixLocation[1], style = "border:5px solid black", border = 0), href = designMatrixLocation[0])
	statsFile = open("stats.html", "w")
	print(statsPage, file = statsFile)
	statsFile.close()
	
def generatePostStatsHTML(graph): #Generates Post-Stats page
	voxelWise = checkHeightThreshold(graph)
	clusterWise = checkExtentThreshold(graph)
	softwareLabelNum = queryVersionNum(graph)
	softwareLabelNumList = addQueryToList(softwareLabelNum)
	statisticType = queryStatisticType(graph)
	statisticType = statisticImage(statisticType[0])
	print("Stat type")
	print(statisticType)
	postStatsPage = markup.page()
	postStatsPage.init(title = "FSL Viewer", css = "viewerStyles.css")
	postStatsPage.h1("Sample FSL Viewer")
	#mainPage.div(e.a("Stats", href = "stats.html"))
	#mainPage.div(e.a("Post Stats", href = "postStats.html"))
	postStatsPage.ul()
	postStatsPage.li(e.a("Stats", href = "stats.html"))
	postStatsPage.li("-")
	postStatsPage.li(e.a("Post Stats", href = "postStats.html"))
	postStatsPage.ul.close()
	postStatsPage.h2("Post-stats")
	postStatsPage.hr()
	postStatsPage.h3("Analysis Methods")
	
	if voxelWise == True:
	
		if askSpm(graph) == True:
	
			postStatsPage.p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at" % (softwareLabelNumList[1], statisticType))
	
		elif askFsl(graph) == True:
			fslFeatVersion = queryFslFeatVersion(graph)
			postStatsPage.p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). %s statistic images were thresholded at" 
			%(fslFeatVersion[0], softwareLabelNumList[1], statisticType))
	
	elif clusterWise == True:
		print("Cluster thresh Value")
		mainThreshValue = queryClusterThresholdValue(graph)
		print(mainThreshValue)
		if askSpm(graph) == True:
	
			postStatsPage.p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded using clusters determined by ... and a (corrected) "
			"cluster significance of P = %s " 
			% (softwareLabelNumList[1], statisticType, mainThreshValue[0]))
	
		elif askFsl(graph) == True:
			fslFeatVersion = queryFslFeatVersion(graph)
			postStatsPage.p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). %s statistic images were thresholded "
			"using clusters determined by ... and a (corrected) cluster significance of P = %s" 
			%(fslFeatVersion[0], softwareLabelNumList[1], statisticType, mainThreshValue[0]))
		
	
	else:
	
		print("Not ready yet")
	
	postStatsPage.hr()
	postStatsPage.h3("Threshold Activation Images")
	postStatsFile = open("postStats.html", "w")
	print(postStatsPage, file = postStatsFile)
	postStatsFile.close()
	
g = rdflib.Graph()
filepath = input("Please enter NIDM file name")
g.parse(filepath, format = rdflib.util.guess_format(filepath))
x = queryFslFeatVersion(g)
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
generatePostStatsHTML(g)
generateMainHTML(g)
print("Testing checkHeightThreshold")
print(checkHeightThreshold(g))
print("Testing checkExtentThreshold")
print(checkExtentThreshold(g))

