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
	
	if os.path.isdir(dataDir) == False:
	
		os.makedirs(dataDir)
		
		
	dataNames = ["fsl_con_f", "fsl_thr_clustfwep05","ex_spm_thr_voxelunct4","ex_spm_thr_clustunck10","ex_spm_thr_voxelfdrp05"]
	local = True
	for dataName in dataNames: #Checks if data is on local machine
	
		
		if os.path.isfile(os.path.join(dataDir, dataName + ".nidm.ttl")) == False: #Data not found on local machine
			
			local = False
			break
	
	if local == False: #Data not on local machine
	
		print("Downloading data")
		req = urllib.request.Request("http://neurovault.org/api/collections/1692/nidm_results") #Request from neurovault api
		resp = urllib.request.urlopen(req)
		readResp = resp.read()
		data = json.loads(readResp.decode('utf-8'))
		
		for nidmResult in data["results"]:
		
			
			turtUrl = nidmResult["ttl_file"] #Url of turtle file
			dataName = nidmResult["name"] #Name of data (e.g. fsl_con_f.nidm)
			
			if dataName in [d + ".nidm" for d in dataNames]: #Check if data is required for tests
			
				turtFile = urllib.request.urlopen(turtUrl)
				dataPath = os.path.join(dataDir, dataName + ".ttl") 
				dataFile = open(dataPath, "w") 
				decTurt = turtFile.read()
				dataFile.write(decTurt.decode('utf-8')) #Write turtle file to data directory
				dataFile.close()
		
				if os.path.isfile(dataPath) == False:
				
					dataFile = open(dataPath, "w") 
					decTurt = turtFile.read()
					dataFile.write(decTurt.decode('utf-8')) #Write turtle file to data directory
					dataFile.close()
				
				
				
	unittest.main() #Tests
	
		