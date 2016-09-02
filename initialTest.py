import os
import unittest
import sys

class fslTests(unittest.TestCase):
	htmlFile = ""
	testHtml = ""
	def test_softwareName(self):
		testFile = open(self.testHtml, "r")
		resultFile = open(self.htmlFile, "r")
		found = False
		for line in resultFile:
			
			if "FSL" in line:
				found = True
				
		
		self.assertTrue(found)
		testFile.close()
		resultFile.close()
	def test_featVersionNum(self):
	
		testFile = open(self.testHtml, "r")
		resultFile = open(self.htmlFile, "r")
		for line in testFile:
		
			if "Version" in line:
			
				stringToCompare = line
				break
		
	
		for line in resultFile:
		
			if "Version" in line:
			
				myString = line
				break
				
		self.assertIn("Version 6.00", myString)
		testFile.close()
		resultFile.close()
		
	def testStatImageType(self):
	
		testFile = open(self.testHtml, "r")
		resultFile = open(self.htmlFile, "r")
		
		for line in resultFile:
		
			if "statistic images" in line:
			
				myString = line
				break
				
		self.assertIn("Z (Gaussianised T/F)", myString)
		testFile.close()
		resultFile.close()
		
		
if __name__ == "__main__":

	if len(sys.argv) > 1:
		
		fslTests.testHtml = sys.argv.pop()
		fslTests.htmlFile = sys.argv.pop()
		
	unittest.main()