#!/usr/bin/env python3
import os
import unittest
import sys
import string
import viewer
import glob

class generalTests(unittest.TestCase):

	def test_error(self): #Run viewer.py on all turtle files in data folder - Checks for errors (program crashes)
	
		script = os.path.dirname(os.path.abspath(__file__))
		dataFolder = os.path.join(script, "data")
		globData = os.path.join(dataFolder,"*.ttl")
		data = glob.glob(globData)
		
		for i in data: #Loop over all turtle files in data
		
			viewer.main(i,i + "test") #Run viewer on turtle file
			
if __name__ == "__main__":

	unittest.main()
	
		