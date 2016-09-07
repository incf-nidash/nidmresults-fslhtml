import os
import unittest
import sys
import string

class fslStatsTests(unittest.TestCase):
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
				print(myString.split())
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
		
	def test_compare(self):
		actualString = ""
		myString = ""
		testFile = open(self.testHtml, "r")
		resultFile = open(self.htmlFile, "r")
		
		for line in testFile:
		
			if "Version" in line: 
			
				actualString = line
				print(actualString.split())
				break
				
		for line in resultFile:
		
			if "Version" in line:
			
				myString = line
				break
		
		print("Below")
		print(myString)
		print(actualString)		
		testFile.close()
		resultFile.close()
if __name__ == "__main__":

	if len(sys.argv) > 1:
		
		fslStatsTests.testHtml = sys.argv.pop()
		fslStatsTests.htmlFile = sys.argv.pop()
		
		
	unittest.main()