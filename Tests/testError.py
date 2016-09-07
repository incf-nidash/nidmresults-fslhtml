import os
import unittest
import sys
import string
import viewer
import glob

class generalTests(unittest.TestCase):

	def test_error(self):
	
		data = glob.glob("*.ttl")
		print(data)
		for i in data:
		
			viewer.main(i,i + "test")
			
if __name__ == "__main__":

	unittest.main()
	
		