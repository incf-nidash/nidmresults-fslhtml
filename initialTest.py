import os
import unittest

class statsPageTests(unittest.TestCase):

	def test_softwareName(self):
	
		x = open(testFileName, "r")
		found = False
		for line in x:
			if "SPM" in line:
				found = True
				
		
		self.assertTrue(found)
	
		
		
