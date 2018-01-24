#!/usr/bin/env python3
from nidmviewerfsl import viewer
import unittest
import sys
import os
import glob
import urllib.request
import json
from ddt import ddt, data

#This is the class of tests for testing specific features of datasets.
@ddt
class testDatasetFeatures(unittest.TestCase): 
    
    #Create a structure for data about each datapack.
    fsl_con_f = {'Name': 'fsl_con_f_130',
                 'softwareName': 'FSL',
                 'version': '6.00',
                 'hThresh': 'P = 0.001 (uncorrected)'}

    #Initiate a blank string.
    def setUp(self): 
        self.testString = ""
    
    #Setup for individual data
    def indvSetUp(self, structData):

        #Open the necessary file.
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data", 
                                     structData["Name"] + "_test",
                                     "postStats.html")

        postStatsFile = open(fileName, "r")
        return(postStatsFile)

    #Test to see if the software name has been recorded correctly.
    @data(fsl_con_f)
    def test_softwareName(self, structData): 

        #Setup
        postStatsFile = self.indvSetUp(structData)

        #Check for the software name.
        for line in postStatsFile:
            
            if "FMRI" in line:
            
                self.testString = line
                break
        
        #Close the file
        postStatsFile.close()
        
        self.assertIn(structData["softwareName"], self.testString,
                      msg = 'Test failed on ' + structData["Name"])

    #Test to see if the software version has been recorded correctly.
    @data(fsl_con_f)
    def test_softwareNum(self, structData):

        #Setup
        postStatsFile = self.indvSetUp(structData)

        #Check for the software version.
        for line in postStatsFile:
            
            if "Version" in line:
            
                self.testString = line
                break
                
        self.assertIn(structData["version"], line,
                      msg = 'Test failed on ' + structData["Name"])

        #Close the file
        postStatsFile.close()

    #Test to see if the height threshold has been recorded correctly.
    @data(fsl_con_f)
    def test_heightThreshold(self, structData):
     
        #Setup
        postStatsFile = self.indvSetUp(structData)

        for line in postStatsFile:
        
            if "statistic images were thresholded" in line:
            
                self.testString = line
                break

        #Close the file
        postStatsFile.close()
                
        self.assertIn(structData["hThresh"], self.testString,
                      msg = 'Test failed on ' + structData["Name"])

#===============================================================================

if __name__ == "__main__":

    scriptPath = os.path.dirname(os.path.abspath(__file__)) #Get path of script
    dataDir = os.path.join(scriptPath, "data")
    
    if os.path.isdir(dataDir) == False: #Data folder does not exist
        
        os.makedirs(dataDir)
        
        
    dataNames = ["fsl_con_f_130"] 
                 #"fsl_thr_clustfwep05_130",
                 #"ex_spm_thr_voxelunct4",
                 #"ex_spm_thr_clustunck10",
                 #"ex_spm_thr_voxelfdrp05"]

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
