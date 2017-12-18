#!/usr/bin/env python3
from nidmviewerfsl import viewer
import unittest
import sys
import os
import glob
import urllib.request
import json

class fsl_con_f(unittest.TestCase): #Class for fsl_con_f tests
	
	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "fsl_con_f_130_test")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
		

	def test_softwareName(self): #Test to see if FSL is in html file
		
		for line in self.postStatsFile:
			
			if "FSL" in line and "FMRI" in line:
			
				self.myString = line
				break
				
		self.assertIn("FSL", self.myString)
	
	def test_softwareNum(self):
	
		for line in self.postStatsFile:
			
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("6.00", line)
		
	def test_statImage(self):
	
		for line in self.postStatsFile:
		
			if "statistic images" in line:
			
				self.myString = line
				break
		
		self.assertIn("Z (Gaussianised T/F)", self.myString)
		
	def test_threshold(self):
	
		for line in self.postStatsFile:
		
			if "statistic images were thresholded at" in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.001 (uncorrected)", self.myString)
	
	def tearDown(self):
		
		self.postStatsFile.close()
		
		
class fsl_thr_clustfwep05(unittest.TestCase): #Class for fsl_thr_clustfwep05 tests

	def setUp(self): #Open necessary file
		self.myString = ""
		self.found = False
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "fsl_thr_clustfwep05_130_test")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
	
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line and "FMRI" in line:
			
				self.myString = line
				break
				
		self.assertIn("FSL", self.myString)
	
	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("6.00", line)
	
	def test_clustThreshold(self): #Test for Z > 2.3
	
		for line in self.postStatsFile:
		
			if "statistic images were thresholded using clusters determined by" in line:
			
				self.myString = line
				break
				
		self.assertIn("Z &gt; 2.3", self.myString)
	
	def test_threshold(self):
	
		for line in self.postStatsFile:
		
			if "(corrected)" in line:
			
				self.found = True
				break
				
		self.assertTrue(self.found)
	
	def test_thresholdValue(self):
	
		for line in self.postStatsFile:
		
			if "P = 0.05" in line:
			
				self.found = True
				
		self.assertTrue(self.found)
	
	def tearDown(self):
	
		self.postStatsFile.close()
"""
class fsl_thr_voxelfwep05(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "fsl_thr_voxelfwep05_130.nidm.ttlTestResults")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
	
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line and "FMRI" in line:
			
				self.myString = line
				break
				
		self.assertIn("FSL", self.myString)
	
	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("6.00", line)
	
	def test_voxelThreshold(self): #Test voxel wise P = 0.05
	
		for line in self.postStatsFile:
		
			if "(corrected) significance threshold" in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.05", self.myString)
	
	def tearDown(self):
	
		self.postStatsFile.close()"""
		
class spm_thr_clustunck10(unittest.TestCase):
	
	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_clustunck10_test")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
		
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "SPM" in line:
			
				self.myString = line
				break
				
		self.assertIn("SPM", self.myString)

	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("12.6906", line)
	
	def test_pThresh(self):
	
		for line in self.postStatsFile:
		
			if "P = " in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.001", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
class spm_thr_voxelfdrp05(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_voxelfdrp05_test")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
		
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "SPM" in line:
			
				self.myString = line
				break
				
		self.assertIn("SPM", self.myString)

	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("12.6906", line)
	
	def test_pThresh(self):
	
		for line in self.postStatsFile:
		
			if "P = " in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.05", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
class spm_thr_voxelunct4(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_voxelunct4_test")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
		
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "SPM" in line:
			
				self.myString = line
				break
				
		self.assertIn("SPM", self.myString)

	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("12.6906", line)
	
	def test_tThresh(self):
	
		for line in self.postStatsFile:
		
			if "T statistic images" in line:
			
				self.myString = line
				break
				
		self.assertIn("T = 4.0 (uncorrected)", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
if __name__ == "__main__":

	scriptPath = os.path.dirname(os.path.abspath(__file__)) #Get path of script
	dataDir = os.path.join(scriptPath, "data")
	
	if os.path.isdir(dataDir) == False: #Data folder does not exist
		
		os.makedirs(dataDir)
		
		
	dataNames = ["fsl_con_f_130", "fsl_thr_clustfwep05_130","ex_spm_thr_voxelunct4","ex_spm_thr_clustunck10","ex_spm_thr_voxelfdrp05"]
	local = True
	
	for dataName in dataNames: #Check if data is on local machine
	
		if os.path.isfile(os.path.join(dataDir, dataName + ".nidm.zip")) == False: #Data not found on local machine
		
			local = False
			break
			
	if local == False:
	
		req = urllib.request.Request("http://neurovault.org/api/collections/2210/nidm_results") #Request from neurovault api
		resp = urllib.request.urlopen(req)
		readResp = resp.read()
		data = json.loads(readResp.decode('utf-8'))
		
		for nidmResult in data["results"]:
		
			print(nidmResult["zip_file"])
			
			zipUrl = nidmResult["zip_file"] #Url of zip file
			dataName = nidmResult["name"] #Name of data (e.g. fsl_con_f.nidm)
			dataNameFile = os.path.join(dataDir, dataName + ".zip")
			
			if os.path.isfile(dataNameFile) == False:
			
				zipFileRequest = urllib.request.urlretrieve(zipUrl, dataNameFile) #copy zip file to local machine
		
						
	globData = os.path.join(dataDir,"*.zip") 
	data = glob.glob(globData) #Get names of all zip files in data folder
	
	for i in data: #Loop over all zip files in data folder and create html
	
		viewer.main(i, i.replace(".nidm.zip", "") + "_test", overwrite=True)
		
	unittest.main() #Tests
