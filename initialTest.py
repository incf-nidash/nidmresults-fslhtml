import os
import unittest
import sys

class fslTests(unittest.TestCase):
	htmlFile = ""
	def test_softwareName(self):
	
		file = open(self.htmlFile, "r")
		found = False
		for line in file:
			if "FSL" in line:
				found = True
				
		
		self.assertTrue(found)
		
	def test_versionNum(self):
	
		#x = open(testFileName, "r")
		y = 5
	
		
		
if __name__ == "__main__":

	if len(sys.argv) > 1:
	
		fslTests.htmlFile = sys.argv.pop()
		
	unittest.main()