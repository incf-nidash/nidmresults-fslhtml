import unittest
import viewer
import sys
import os

class fsl_con_f(unittest.TestCase): #Class for fsl_con_f tests

	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "fsl_con_f.nidm.ttl"
		self.folder = viewer.main(self.data, "fsl_con_f_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
		

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
		
class fsl_thr_clustfwep05(unittest.TestCase): #Class for fsl_thr_clustfwep05 tests

	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "fsl_thr_clustfwep05.nidm.ttl"
		self.folder = viewer.main(self.data, "fsl_thr_clustfwep05testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
	
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
		
			if "(corrected) cluster significance threshold" in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.05", self.myString)
	
	def tearDown(self):
	
		self.postStatsFile.close()

class fsl_thr_voxelfwep05(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "fsl_thr_voxelfwep05.nidm.ttl"
		self.folder = viewer.main(self.data, "fsl_thr_voxelfwep05testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
	
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
	
		self.postStatsFile.close()
		
class spm_thr_clustunck10(unittest.TestCase):
	
	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "ex_spm_thr_clustunck10.nidm.ttl"
		self.folder = viewer.main(self.data, "ex_spm_thr_clustunck10_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
		
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
		
			if "P" in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.001", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
class spm_thr_voxelfdrp05(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "ex_spm_thr_voxelfdrp05.nidm.ttl"
		self.folder = viewer.main(self.data, "ex_spm_thr_voxel05_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
		
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "SPM" in line:
			
				self.myString = line
				break
				
		self.assertIn("SPM", self.self.myString)

	def test_softwareNum(self):
	
		for line in self.postStatsFile:
		
			if "Version" in line:
			
				self.myString = line
				break
				
		self.assertIn("12.6685", line)
	
	def test_pThresh(self):
	
		for line in self.postStatsFile:
		
			if "P" in line:
			
				self.myString = line
				break
				
		self.assertIn("P = 0.05", line)
	
	def tearDown(self):
	
		self.postStatsFile.close()
		
class spm_thr_voxelunct4(unittest.TestCase):

	def setUp(self): #Open necessary file
		self.myString = ""
		self.data = "ex_spm_thr_voxelunct4.nidm.ttl"
		self.folder = viewer.main(self.data, "ex_spm_thr_voxelunct4_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.postStats = os.path.join(self.dest, "postStats.html")
		self.postStatsFile = open(self.postStats, "r")
		
	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.postStatsFile:
		
			if "SPM" in line:
			
				self.myString = line
				break
				
		self.assertIn("SPM", self.self.myString)

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