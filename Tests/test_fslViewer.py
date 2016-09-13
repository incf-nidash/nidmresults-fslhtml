#!/usr/bin/env python3
import unittest
import viewer
import sys
import os
import shutil
import glob

class fsl_con_f(unittest.TestCase): #Class for fsl_con_f tests
	
	def setUp(self): #Open necessary file
		self.myString = ""
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "fsl_con_f.nidm.ttlTestResults")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
		

	def test_softwareName(self): #Test to see if FSL is in html file
		
		for line in self.postStatsFile:
			
			if "FSL" in line:
			
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
		#shutil.rmtree("fsl_con_f_testHTML")
		
class fsl_thr_clustfwep05(unittest.TestCase): #Class for fsl_thr_clustfwep05 tests

	def setUp(self): #Open necessary file
		self.myString = ""
		self.found = False
		self.scriptPath = os.path.dirname(os.path.abspath(__file__))
		self.dataPath = os.path.join(self.scriptPath, "data")
		self.dataPath = os.path.join(self.dataPath, "fsl_thr_clustfwep05.nidm.ttlTestResults")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
	
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line:
			
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
				
		self.assertIn("Z > 2.3", self.myString)
	
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
		self.dataPath = os.path.join(self.dataPath, "fsl_thr_voxelfwep05.nidm.ttlTestResults")
		self.fileName = os.path.join(self.dataPath, "postStats.html")
		self.postStatsFile = open(self.fileName, "r")
	
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line:
			
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
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_clustunck10.nidm.ttlTestResults")
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
				
		self.assertIn("12.6685", line)
	
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
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_voxelfdrp05.nidm.ttlTestResults")
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
				
		self.assertIn("12.6685", line)
	
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
		self.dataPath = os.path.join(self.dataPath, "ex_spm_thr_voxelunct4.nidm.ttlTestResults")
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
				
		self.assertIn("12.6685", line)
	
	def test_tThresh(self):
	
		for line in self.postStatsFile:
		
			if "T statistic images" in line:
			
				self.myString = line
				break
				
		self.assertIn("T = 4.0 (uncorrected)", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
if __name__ == "__main__":
	scriptPath = os.path.dirname(os.path.abspath(__file__))
	dataPath = os.path.join(scriptPath, "data")
	globData = os.path.join(dataPath,"*.ttl")
	data = glob.glob(globData)
	for i in data:
	
		viewer.main(i, i + "TestResults")
	unittest.main()