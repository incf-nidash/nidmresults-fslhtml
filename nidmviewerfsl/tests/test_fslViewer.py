#!/usr/bin/env python3
from nidmviewerfsl import viewer
import unittest
import sys
import os
import glob
import urllib.request
import json

#This is the class of tests run on the data pack 'fsl_con_f_130'
class fsl_con_f(unittest.TestCase): 
    
    #Open the necessary file and initiate a blank string.
    def setUp(self): 
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "fsl_con_f_130_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")
        
    #Test to see if the software name has been recorded correctly.
    def test_softwareName(self): 
        
        for line in self.postStatsFile:
            
            if "FSL" in line and "FMRI" in line:
            
                self.testString = line
                break
                
        self.assertIn("FSL", self.testString)

    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
            
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("6.00", line)
    
    #Test to see if the statistic image has been recorded correctly.
    def test_statImage(self):
    
        for line in self.postStatsFile:
        
            if "statistic images" in line:
            
                self.testString = line
                break
        
        self.assertIn("Z (Gaussianised T/F)", self.testString)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self):
    
        for line in self.postStatsFile:
        
            if "statistic images were thresholded at" in line:
            
                self.testString = line
                break
                
        self.assertIn("P = 0.001 (uncorrected)", self.testString)
    
    #Close the test
    def tearDown(self):
        
        self.postStatsFile.close()
        
#This is the class of tests run on the data pack 'fsl_thr_clustfwep05'
class fsl_thr_clustfwep05(unittest.TestCase): 

    #Open the necessary file and initiate a blank string.
    def setUp(self): 
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "fsl_thr_clustfwep05_130_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")
    
    #Test to see if the software name has been recorded correctly.
    def test_softwareName(self): 
    
        for line in self.postStatsFile:
        
            if "FSL" in line and "FMRI" in line:
            
                self.testString = line
                break
                
        self.assertIn("FSL", self.testString)
    
    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
        
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("6.00", line)
    
    #Test to see if the cluster threshold has been recorded correctly.
    def test_clustThreshold(self): 
    
        for line in self.postStatsFile:
        
            if "statistic images were thresholded using clusters determined by" in line:
            
                self.testString = line
                break
                
        self.assertIn("Z > 2.3", self.testString)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self):
    
        for line in self.postStatsFile:
        
            if "P = 0.05" in line:
            
                self.found = True
                
        self.assertTrue(self.found)
    
    #Close the test
    def tearDown(self):
    
        self.postStatsFile.close()

#This is the class of tests run on the data pack 'fsl_thr_voxelfwep05'
class fsl_thr_voxelfwep05(unittest.TestCase):

    #Open the necessary file and initiate a blank string.
    def setUp(self): 
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "fsl_thr_voxelfwep05_130_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")
    
    #Test to see if the software name has been recorded correctly.
    def test_softwareName(self): 
    
        for line in self.postStatsFile:
        
            if "FSL" in line and "FMRI" in line:
            
                self.testString = line
                break
                
        self.assertIn("FSL", self.testString)
    
    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
        
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("6.00", line)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self): 
    
        for line in self.postStatsFile:
        
            if "(corrected)" in line:
            
                self.testString = line
                break
                
        self.assertIn("P = 0.05", self.testString)
    
    #Close the test
    def tearDown(self):
    
        self.postStatsFile.close()

#This is the class of tests run on the data pack 'spm_thr_clustunck10'      
class spm_thr_clustunck10(unittest.TestCase):
    
    #Open the necessary file and initiate a blank string.
    def setUp(self): 
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "ex_spm_thr_clustunck10_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")
    
    #Test to see if the software name has been recorded correctly.
    def test_softwareName(self):
    
        for line in self.postStatsFile:
        
            if "SPM" in line:
            
                self.testString = line
                break
                
        self.assertIn("SPM", self.testString)

    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
        
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("12.6906", line)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self):
    
        for line in self.postStatsFile:
        
            if "P = " in line:
            
                self.testString = line
                break
                
        self.assertIn("P = 0.001", line)

    #Close the test
    def tearDown(self):
    
        self.postStatsFile.close()

#This is the class of tests run on the data pack 'spm_thr_voxelfdrp05'        
class spm_thr_voxelfdrp05(unittest.TestCase):

    #Open the necessary file and initiate a blank string.
    def setUp(self):
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "ex_spm_thr_voxelfdrp05_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")
    
    #Test to see if the software name has been recorded correctly.
    def test_softwareName(self): 
    
        for line in self.postStatsFile:
        
            if "SPM" in line:
            
                self.testString = line
                break
                
        self.assertIn("SPM", self.testString)

    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
        
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("12.6906", line)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self):
    
        for line in self.postStatsFile:
        
            if "P = " in line:
            
                self.testString = line
                break
                
        self.assertIn("P = 0.05", line)

    #Close the test
    def tearDown(self):
    
        self.postStatsFile.close()

#This is the class of tests run on the data pack 'spm_thr_voxelunct4'
class spm_thr_voxelunct4(unittest.TestCase):

    #Open the necessary file and initiate a blank string.
    def setUp(self):
        self.testString = ""
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", "ex_spm_thr_voxelunct4_test",
                                     "postStats.html")
        self.postStatsFile = open(self.fileName, "r")

    #Test to see if the software name has been recorded correctly.        
    def test_softwareName(self): 
    
        for line in self.postStatsFile:
        
            if "SPM" in line:
            
                self.testString = line
                break
                
        self.assertIn("SPM", self.testString)

    #Test to see if the software version has been recorded correctly.
    def test_softwareNum(self):
    
        for line in self.postStatsFile:
        
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn("12.6906", line)
    
    #Test to see if the height threshold has been recorded correctly.
    def test_heightThreshold(self):
    
        for line in self.postStatsFile:
        
            if "T statistic images" in line:
            
                self.testString = line
                break
                
        self.assertIn("T = 4.0 (uncorrected)", line)
    
    #Close the test
    def tearDown(self):
    
        self.postStatsFile.close()
        
if __name__ == "__main__":

    scriptPath = os.path.dirname(os.path.abspath(__file__)) #Get path of script
    dataDir = os.path.join(scriptPath, "data")
    
    if os.path.isdir(dataDir) == False: #Data folder does not exist
        
        os.makedirs(dataDir)
        
        
    dataNames = ["fsl_con_f_130", 
                 "fsl_thr_clustfwep05_130",
                 "ex_spm_thr_voxelunct4",
                 "ex_spm_thr_clustunck10",
                 "ex_spm_thr_voxelfdrp05"]

    local = True
    
    for dataName in dataNames: #Check if data is on local machine
        
        #Data not found on local machine
        if not os.path.isfile(os.path.join(dataDir, dataName + ".nidm.zip")): 
        
            local = False
            break
            
    if local == False:
        
        #Request from neurovault api
        req = urllib.request.Request(
              "http://neurovault.org/api/collections/2210/nidm_results")
        resp = urllib.request.urlopen(req)
        readResp = resp.read()
        data = json.loads(readResp.decode('utf-8'))
        
        for nidmResult in data["results"]:
        
            print(nidmResult["zip_file"])
            
            zipUrl = nidmResult["zip_file"] #Url of zip file
            dataName = nidmResult["name"] #Name of data (e.g. fsl_con_f.nidm)
            dataNameFile = os.path.join(dataDir, dataName + ".zip")
            
            if os.path.isfile(dataNameFile) == False:

                #copy zip file to local machine
                zipFileRequest = urllib.request.urlretrieve(zipUrl,
                                                            dataNameFile) 
        
                        
    globData = os.path.join(dataDir,"*.zip") 
    data = glob.glob(globData) #Get names of all zip files in data folder
    
    for i in data: #Loop over all zip files in data folder and create html
    
        viewer.main(i, i.replace(".nidm.zip", "") + "_test", overwrite=True)
        
    unittest.main() #Tests
