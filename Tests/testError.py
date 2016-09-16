#!/usr/bin/env python3
import os
import unittest
import sys
import string
import viewer
import glob
import urllib.request
import json

class generalTests(unittest.TestCase):

	def test_error(self): #Run viewer.py on all turtle files in data folder - Checks for errors (program crashes)
	
		script = os.path.dirname(os.path.abspath(__file__))
		dataFolder = os.path.join(script, "data")
		globData = os.path.join(dataFolder,"*.ttl")
		data = glob.glob(globData)
		
		for i in data: #Loop over all turtle files in data
		
			viewer.main(i,i + "test") #Run viewer on turtle file
			
if __name__ == "__main__":
	
	scriptDir = os.path.dirname(os.path.abspath(__file__))
	dataDir = os.path.join(scriptDir, "data")
	dataNames = ["fsl_con_", "fsl_thr_clustfwep05","ex_spm_thr_voxelunct4","ex_spm_thr_clustunck10","ex_spm_thr_voxelfdrp05"]
	local = True
	for dataName in dataNames: #Checks if data is on local machine
	
		
		if os.path.isfile(os.path.join(dataDir, dataName + ".nidm.ttl")) == False: #Data not found on local machine
			print(dataName)
			local = False
			break
	
	if local == False:
		"""print("Downloading data")
		req = urllib.request.Request("http://neurovault.org/api/collections/1692/images")
		resp = urllib.request.urlopen(req)
		readResp = resp.read()
		data = json.loads(readResp.decode('utf-8'))
		print("Data")
		print(data.keys())
		turtList = []
		for nidmResult in data["results"]:
			
			turt = nidmResult["nidm_results_ttl"]
			turtList.append(turt)
			#print(turt)
		
		uniqueTurtList = list(set(turtList))
		print(uniqueTurtList)
		print(len(uniqueTurtList))
		for turtleFile in uniqueTurtList:
		
			url = urllib.request.urlopen(turtleFile)
			#print(url.read())
			#input("Enter")
		
	#unittest.main()"""
	
		