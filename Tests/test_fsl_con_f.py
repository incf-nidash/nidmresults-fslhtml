import unittest
import viewer
import sys
import os

class fsl_con_f(unittest.TestCase): #Class for fsl_con_f tests

	def setUp(self): #Open necessary file
	
		self.data = "fsl_con_f.nidm.ttl"
		#self.file = open(self.data, "r")
		self.folder = viewer.main(self.data, "fsl_con_f_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
		

	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line:
			
				myString = line
				break
				
		self.assertIn("FSL", myString)
	
	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				myString = line
				break
				
		self.assertIn("6.00", line)
		
	def test_statImage(self):
	
		for line in self.postStatsFile:
		
			if "statistic images" in line:
			
				myString = line
				break
		
		self.assertIn("Z (Gaussianised T/F)", myString)
		
	def test_threshold(self):
	
		for line in self.postStatsFile:
		
			if "statistic images were thresholded at" in line:
			
				myString = line
				break
				
		self.assertIn("P = 0.001 (uncorrected)", myString)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
class fsl_thr_clustfwep05(unittest.TestCase): #Class for fsl_thr_clustfwep05 tests

	def setUp(self): #Open necessary file
	
		self.data = "fsl_thr_clustfwep05.nidm.ttl"
		#self.file = open(self.data, "r")
		self.folder = viewer.main(self.data, "fsl_thr_clustfwep05testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
	
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "FSL" in line:
			
				myString = line
				break
				
		self.assertIn("FSL", myString)
	
	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				myString = line
				break
				
		self.assertIn("6.00", line)
	
	def test_clustThreshold(self): #Test for Z > 2.3
	
		for line in self.postStatsFile:
		
			if "statistic images were thresholded using clusters determined by" in line:
			
				myString = line
				break
				
		self.assertIn("Z > 2.3", myString)
	
	def test_threshold(self):
	
		for line in self.postStatsFile:
		
			if "(corrected) cluster significance threshold" in line:
			
				myString = line
				break
				
		self.assertIn("P = 0.05", myString)
	
	def tearDown(self):
	
		self.postStatsFile.close()
	