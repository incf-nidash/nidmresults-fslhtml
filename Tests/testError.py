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
	
	scriptDir = os.path.dirname(os.path.abspath(__file__))
	dataDir = os.path.join(scriptDir, "data")
	dataNames = ["fsl_con_f", "fsl_thr_clustfwep05","ex_spm_thr_voxelunct4","ex_spm_thr_clustunck10","ex_spm_thr_voxelfdrp05"]
	
	for dataName in dataNames: #Checks if data is on local machine
	
		local = True
		if os.path.isfile(os.path.join(dataName, ".nidm.ttl")) == False: #Data not found on local machine
		
			local = False
			break
	
	unittest.main()
	
		