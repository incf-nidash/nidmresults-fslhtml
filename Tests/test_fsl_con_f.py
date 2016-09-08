import unittest
import viewer
import sys
import os

class fsl_con_f(unittest.TestCase):

	def setUp(self): #Open necessary file
	
		self.data = "fsl_con_f.nidm.ttl"
		#self.file = open(self.data, "r")
		self.folder = viewer.main(self.data, "fsl_con_f_testHTML")
		self.direc = os.getcwd()
		self.dest = os.path.join(self.direc, self.folder)
		self.stats = os.path.join(self.dest, "stats.html")
		self.file = open(self.stats, "r")
		

	def test_softwareName(self): #Test to see if FSL is in html file
	
		for line in self.file:
		
			if "FSL" in line:
			
				myString = line
				break
				
		self.assertIn("FSL", myString)
	
	def test_softwareNum(self):
	
		for line in self.file:
		
			if "Version" in line:
			
				myString = line
				break
				
		self.assertIn("6.00", line)
	
	def tearDown(self):
	
		self.file.close()