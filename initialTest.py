import os
import unittest
import sys

class fslTests(unittest.TestCase):
	htmlFile = ""
	testHtml = ""
	def test_softwareName(self):
	
		resultFile = open(self.htmlFile, "r")
		found = False
		for line in resultFile:
			
			if "FSL" in line:
				found = True
				
		
		self.assertTrue(found)
		
	def test_versionNum(self):
	
		file = open(self.htmlFile, "r")
		
	
		
		
if __name__ == "__main__":

	if len(sys.argv) > 1:
		
		fslTests.testHtml = sys.argv.pop()
		fslTests.htmlFile = sys.argv.pop()
		
	unittest.main()