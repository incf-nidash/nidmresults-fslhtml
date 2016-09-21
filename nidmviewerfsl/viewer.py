#!/usr/bin/env python3
import os
import sys
import rdflib
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
	prefix nidm_ConjunctionInference: <http://purl.org/nidash/nidm#NIDM_0000011>
               prefix nidm_statisticType: <http://purl.org/nidash/nidm#NIDM_0000123>
			   prefix nidm_statisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
               prefix prov: <http://www.w3.org/ns/prov#>
               prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               prefix obo_tstatistic: <http://purl.obolibrary.org/obo/STATO_0000176>
               prefix obo_Fstatistic: <http://purl.obolibrary.org/obo/STATO_0000282>
               prefix obo_Zstatistic: <http://purl.obolibrary.org/obo/STATO_0000376>

               SELECT ?statType WHERE { {?y a nidm_ConjunctionInference: .} UNION { ?y a nidm_Inference: .} ?y prov:used ?x . ?x a nidm_statisticMap: . ?x nidm_statisticType: ?statType .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def statisticImage(stat): #Returns type of statistic image

	if stat == "http://purl.obolibrary.org/obo/STATO_0000376":
	
		return("Z")
	
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000282":
	
		return("F")
		
	elif stat == "http://purl.obolibrary.org/obo/STATO_0000176":
	
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

def queryHeightThresholdValue(graph): #Selects the value of the main threshold if voxel-wise

	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_qvalue: <http://purl.obolibrary.org/obo/OBI_0001442>
               prefix obo_FWERadjustedpvalue: <http://purl.obolibrary.org/obo/OBI_0001265>

               SELECT ?value WHERE {?y a nidm_Inference: . ?y prov:used ?x . {?x a nidm_HeightThreshold: . ?x a obo_qvalue: .} UNION {?x a nidm_HeightThreshold: . ?x a obo_FWERadjustedpvalue: .} ?x prov:value ?value .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def queryUHeightThresholdValue(graph): #Select value of uncorrected height threshold

	query = """prefix prov: <http://www.w3.org/ns/prov#>
			   prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
			   prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
			   prefix nidm_PValueUncorrected: <http://purl.org/nidash/nidm#NIDM_0000160>
			   prefix obo_statistic: <http://purl.obolibrary.org/obo/STATO_0000039>

			   SELECT ?thresholdValue WHERE {?y a nidm_Inference: . ?y prov:used ?x . ?x a nidm_HeightThreshold: . {?x a obo_statistic: . } UNION {?x a nidm_PValueUncorrected: .} ?x prov:value ?thresholdValue}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))
	
def queryContrastName(graph): #Selects contrast name of statistic map

	query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>

               SELECT ?contrastName WHERE {?x a nidm_Inference: . ?x prov:used ?y . ?y a nidm_StatisticMap: . ?y nidm_contrastName: ?contrastName .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def queryStatisticImage(graph): #Selects statistic map image URI

	query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
			   prefix dc: <http://purl.org/dc/elements/1.1/>

               SELECT ?image WHERE {?x a nidm_Inference: . ?x prov:used ?y . ?y a nidm_ExcursionSetMap: . ?y prov:atLocation ?image .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))

def queryExcursionSetMap(graph): #Selects excursion images

	query = """prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_StatisticMap: <http://purl.org/nidash/nidm#NIDM_0000076>
			   prefix nidm_ExcursionSetMap: <http://purl.org/nidash/nidm#NIDM_0000025>
               prefix nidm_contrastName: <http://purl.org/nidash/nidm#NIDM_0000085>
               prefix prov: <http://www.w3.org/ns/prov#>
			   prefix dc: <http://purl.org/dc/elements/1.1/>

               SELECT ?image WHERE {?x a nidm_Inference: . ?y prov:wasGeneratedBy ?x . ?y a nidm_ExcursionSetMap: . ?y dc:description ?z . ?z prov:atLocation ?image .}"""
			   
	queryResult = graph.query(query)
	return(addQueryToList(queryResult))
	
def checkVoxelOrClusterThreshold(graph):

	print("Test")

def askIfOboStatistic(graph): #Checks if threshold is an obo_statistic
	answer = False
	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix obo_statistic: <http://purl.obolibrary.org/obo/STATO_0000039>

               ASK {?y a nidm_Inference: . ?y prov:used ?x . ?x a nidm_HeightThreshold: . ?x a obo_statistic: .}"""
			   
	queryResult = graph.query(query)
	for row in queryResult:
	
		answer = row
	
	return(answer)

def askIfPValueUncorrected(graph): #Checks if threshold is a PValueUncorrected
	answer = False
	query = """prefix prov: <http://www.w3.org/ns/prov#>
               prefix nidm_HeightThreshold: <http://purl.org/nidash/nidm#NIDM_0000034>
               prefix nidm_Inference: <http://purl.org/nidash/nidm#NIDM_0000049>
               prefix nidm_PValueUncorrected: <http://purl.org/nidash/nidm#NIDM_0000160>

               ASK {?y a nidm_Inference: . ?y prov:used ?x . ?x a nidm_HeightThreshold: . ?x a nidm_PValueUncorrected: .}"""
			   
	queryResult = graph.query(query)
	for row in queryResult:
	
		answer = row
		
	return(answer)

def clusterFormingThreshType(graph, image):

	if askIfOboStatistic(graph) == True:
	
		return(image)
		
	elif askIfPValueUncorrected(graph) == True:
	
		return("P")
			   
	
def statisticImageString(statImage):

	if statImage == "T":
	
		return("T")
		
	elif statImage == "F":
	
		return("F")
		
	elif statImage == "Z":
	
		return("Z (Gaussianised T/F)")

	
def generateMainHTML(graph,mainFilePath = "Main.html", statsFilePath = "stats.html", postStatsFilePath = "postStats.html"): #Generates the main HTML page

	main = document(title="FSL Viewer")
	main += h1("Sample FSL Viewer")
	main += ul(li(a("Stats", href="stats.html")), li("-"),li(a("Post Stats", href = "postStats.html")))
	mainFile = open(mainFilePath, "x")
	print(main, file = mainFile)
	mainFile.close()
		
	
def generateStatsHTML(graph,statsFilePath = "stats.html",postStatsFilePath = "postStats.html"): #Generates the Stats HTML section

	firstLevel = checkFirstLevel(graph)
	softwareLabelNum = queryVersionNum(graph)
	softwareLabelNumList = addQueryToList(softwareLabelNum)
	
	stats = document(title="FSL Viewer") #Creates initial html page (stats)
	stats += h1("Sample FSL Viewer")
	stats += ul(li(a("Stats", href="stats.html")), li("-"),li(a("Post Stats", href = "postStats.html")))
	stats += h2("Stats")
	stats += hr()
	stats += h3("Analysis Methods")
	
	if askSpm(graph) == True: #Checks if SPM was used
		
		stats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/)." % softwareLabelNumList[1])
		
	elif askFsl(graph) == True: #Checks if FSL was used
		
		fslFeatVersion = queryFslFeatVersion(graph)
		stats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)." % (fslFeatVersion[0], softwareLabelNumList[1]))
		
	stats += hr()
	stats += h3("Design Matrix")
	
	designMatrixLocation = queryDesignMatrixLocation(graph)
	stats += a(img(src = designMatrixLocation[1], style = "border:5px solid black", border = 0), href = designMatrixLocation[0]) #Adds design matrix image (as a link) to html page
	
	statsFile = open(statsFilePath, "x")
	print(stats, file = statsFile) #Prints html page to a file
	statsFile.close()
		
	
		
	
def generatePostStatsHTML(graph,statsFilePath = "stats.html",postStatsFilePath = "postStats.html"): #Generates Post-Stats page
	voxelWise = checkHeightThreshold(graph)
	clusterWise = checkExtentThreshold(graph)
	softwareLabelNum = queryVersionNum(graph)
	softwareLabelNumList = addQueryToList(softwareLabelNum)
	statisticType = queryStatisticType(graph)
	statisticType = statisticImage(statisticType[0])
	statisticTypeString = statisticImageString(statisticType)
	contrastName = queryContrastName(graph)
	statisticMapImage = queryExcursionSetMap(graph)
	
	postStats = document(title="FSL Viewer") #Creates initial HTML page (Post Stats)
	postStats += h1("Sample FSL Viewer")
	postStats += ul(li(a("Stats", href="stats.html")), li("-"),li(a("Post Stats", href = "postStats.html")))
	postStats += h2("Post-stats")
	postStats += hr()
	postStats += h3("Analysis Methods")
	
	if voxelWise == True: #If main threshold is Height Threshold
		mainThreshValue = queryHeightThresholdValue(graph)
		if askSpm(graph) == True:
			
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at P = %s (corrected)" % (softwareLabelNumList[1], statisticTypeString, mainThreshValue[0]))
	
		elif askFsl(graph) == True:
			fslFeatVersion = queryFslFeatVersion(graph)
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at P = %s (corrected)" 
			%(fslFeatVersion[0], softwareLabelNumList[1], statisticTypeString, mainThreshValue[0]))
	
	elif clusterWise == True: #If main threshold is extent threshold
		
		mainThreshValue = queryClusterThresholdValue(graph)
		heightThreshValue = queryUHeightThresholdValue(graph)
		clusterThreshType = clusterFormingThreshType(graph, statisticType)
		
		if askSpm(graph) == True:
			
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded using clusters determined by %s > %s and a (corrected) "
			"cluster significance of P = %s " 
			% (softwareLabelNumList[1], statisticTypeString, clusterThreshType, heightThreshValue[0], mainThreshValue[0]))
	
		elif askFsl(graph) == True:
			fslFeatVersion = queryFslFeatVersion(graph)
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl). %s statistic images were thresholded "
			"using clusters determined by %s > %s and a (corrected) cluster significance of P = %s" 
			%(fslFeatVersion[0], softwareLabelNumList[1], statisticTypeString, clusterThreshType, heightThreshValue[0], mainThreshValue[0]))
		
	
	else: #If there is no corrected threshold - assume voxel wise
		mainThreshValue = queryUHeightThresholdValue(graph)
		if askSpm(graph) == True and askIfPValueUncorrected(graph) == True: #SPM used and threshold type is nidm_PValueUncorrected
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at P = %s (uncorrected)" % (softwareLabelNumList[1], statisticTypeString, mainThreshValue[0]))
			
		
		elif askSpm(graph) == True and askIfOboStatistic(graph) == True: #SPM used and threshold type is obo_statistic
			postStats += p("FMRI data processing was carried out using SPM Version %s (SPM, http://www.fil.ion.ucl.ac.uk/spm/). %s statistic images were thresholded at %s = %s (uncorrected)" % (softwareLabelNumList[1], statisticTypeString, statisticType, mainThreshValue[0]))
			
		
		elif askFsl(graph) == True and askIfPValueUncorrected(graph) == True:
			
			fslFeatVersion = queryFslFeatVersion(graph)
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at P = %s (uncorrected)." % (fslFeatVersion[0], softwareLabelNumList[1], statisticTypeString, mainThreshValue[0]))
			
			
		elif askFsl(graph) == True and askIfOboStatistic(graph) == True:
			
			fslFeatVersion = queryFslFeatVersion(graph)
			postStats += p("FMRI data processing was carried out using FEAT (FMRI Expert Analysis Tool) Version %s, part of FSL %s (FMRIB's Software Library, www.fmrib.ox.ac.uk/fsl)."
			"%s statistic images were thresholded at %s = %s (uncorrected)." % (fslFeatVersion[0], softwareLabelNumList[1], statisticTypeString, statisticType, mainThreshValue[0]))
			
		
	
	postStats += hr()
	postStats += h3("Thresholded Activation Images")
	postStats += hr()
	i = 0
	
	if askFsl(graph) == True:
	
		while i < len(contrastName):
		
			postStats += p("%s" % contrastName[i])
			postStats += img(src = statisticMapImage[i])
			i = i + 1
	
	postStatsFile = open(postStatsFilePath, "x")
	print(postStats, file = postStatsFile)
	postStatsFile.close()
	
		
def createOutputDirectory(outputFolder): #Attempts to create folder for HTML files, quits program if folder already exists
	"""print("starting input")
	reply = input("y/n")
	print("finishing input")
	print("the reply is " + str(reply))"""
	try:
	
		os.makedirs(outputFolder)
		
	except OSError:
	
		print("Error - %s directory already exists" % outputFolder)
		exit()

def main(nidmFile, htmlFolder): #Main program
	
	g = rdflib.Graph()
	
	
	filepath = nidmFile
	g.parse(filepath, format = rdflib.util.guess_format(filepath))
	destinationFolder = htmlFolder
			
	createOutputDirectory(htmlFolder)
				
	currentDir = os.getcwd()
	dirLocation = os.path.join(currentDir, destinationFolder)
	mainFileName = os.path.join(dirLocation, "main.html")
	statsFileName = os.path.join(dirLocation, "stats.html")
	postStatsFileName = os.path.join(dirLocation, "postStats.html")
	generateStatsHTML(g,statsFileName,postStatsFileName)
	generatePostStatsHTML(g,statsFileName,postStatsFileName)
	generateMainHTML(g,mainFileName,statsFileName,postStatsFileName)
	return(destinationFolder)	

	

		
	