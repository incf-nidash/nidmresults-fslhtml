#!/usr/bin/env python3
from nidmviewerfsl import viewer
import unittest
import sys
import os
import glob
import urllib.request
import json
from ddt import ddt, data

# This is the class of tests for testing specific features of datasets.
@ddt
class testDatasetFeatures(unittest.TestCase):

    # Create a structure for each test datapack.
    fsl_con_f = {'Name': 'fsl_con_f_130',
                 'softwareName': 'FSL',
                 'version': '6.00',
                 'hThresh': 'P = 0.001 (uncorrected)',
                 'lowSliceVal': '3.09',
                 'highSliceVal': '7.4',
                 'numExc': 2}

    fsl_contrast_mask = {'Name': 'fsl_contrast_mask_130',
                         'softwareName': 'FSL',
                         'matchConName': 'tone counting probe vs baseline',
                         'matchSliceImExtract': '5+fu++fQX//M9CiIsXL165cm'
                                                'VoaAhPDA5aVlY2MTGRz+f/8I'
                                                'c/nDlz5qabbvrZz35WVVWFxA'
                                                '5VOXhanH1FElpdXWUmpMvlKi'
                                                '0tfeONN4CIFB9csR80A30YI2'
                                                'C6dpATSgF2u3337t3MmvL5fG'
                                                'NjY8rvapoGY4Y0AARiY2Ojqq'
                                                'qKk4gNtEh9kY2NjVQqVVpayr'}

    fsl_thr_clustfwep05 = {'Name': 'fsl_thr_clustfwep05_130',
                           'softwareName': 'FSL',
                           'version': '6.00',
                           'hThresh': 'determined by Z > 2.3',
                           'eThresh': 'cluster significance of P = 0.05',
                           'sliceImExtract': 'gU0F7EeKZImaLEbUAZ1Qq9KGm'
                                             'htwBlMDvMPlMcUpI5pkA7Ho5A'
                                             'E0fVzeWacqEBEzHbtK9IqEAI/'
                                             'iSY46wGloNUrSfWUikMokAbh6'
                                             'Dtc5ay5JOQtK9Ba/acMa5CeA+'
                                             'Kyt5CC8DliNGGAzb/mgp/oenI'
                                             'M7keUZVG4arsDJ36YZn8Am1N4',
                           'lowSliceVal': '2.3',
                           'highSliceVal': '7.49',
                           'contrastName': 'tone counting vs baseline'}

    ex_spm_contrast_mask = {'Name': 'ex_spm_contrast_mask',
                            'softwareName': 'SPM',
                            'version': '12.6906',
                            'hThresh': 'P = 0.001 (uncorrected)',
                            'sliceImExtract': 'VTGdaW0UiEeInYDOSRTqngIJ'
                                              'KT3piwYmJiZPSf5LxyCOPjIy'
                                              'MXHrppbAFoRFArJbc3obdnh8'
                                              'eDk1NpSIRWkBzmHF+sCNTlKH'
                                              'Fl0EzfSfYoloBr1ZqmHfs2HE'
                                              'Smf+FQuHrX//6j370ozVr1pA',
                            'lowSliceVal': '3.18',
                            'highSliceVal': '7.92',
                            'contrastName': 'tone counting vs baseline'}

    fsl_gamma_basis = {'Name': 'fsl_gamma_basis_130',
                       'softwareName': 'FSL',
                       'numExc': 8,
                       'matchConName': 'tone counting vs baseline (1)',
                       'matchSliceImExtract': 'eDwb17966trQUCgaWlpcOHD7'
                                              'uue+TIkXA4jF6cjuOgyHz9N3'
                                              '9T07RarTY9Pf3CCy+k02lUxK'
                                              'BTny17unDYqt+oyX7VQsJXru'
                                              'uiJ16lUkmn05/85CenpqZ6en'
                                              'oWFxfRtdZxnD179gghLl68eP'
                                              '369TfeeOPcuXM+n+++++6bmZ'
                                              'lhI6kTJ04sLy+je+bx48e//u'}

    ex_spm_default = {'Name': 'ex_spm_default',
                      'softwareName': 'SPM',
                      'version': '12.6906',
                      'hThresh': 'P = 0.001 (uncorrected)',
                      'lowSliceVal': '3.18',
                      'highSliceVal': '7.92',
                      'numExc': 1}

    ex_spm_conjunction = {'Name': 'ex_spm_conjunction',
                          'softwareName': 'SPM',
                          'version': '12.6906',
                          'sliceImExtract': 'eau3d3dr7766pNPPvnqq6+O5/hbW'
                                            '1uRQuR0OuUDC3JVUPwxGo2+9dZbc'
                                            'jJmT09PfX29HCZnhtv/wtlACAkEA'
                                            'q+++up//Md/jIP+IISEw+G2trapU'
                                            '6ci1o6MZtkTTgiBkoBFPH/+/PHjx'
                                            '4PBYH19PerdyefbEY3CsWoELyKRy'
                                            'HPPPffss8+OenX5D3LixAmn01lUV'
                                            'IQuBFBycu0WRCqxBceR+4sXL1osl'
                                            'oKCAphqOeSUG25Wxwx3Wkmn0xcuX',
                          'lowSliceVal': '3.18',
                          'highSliceVal': '5.65',
                          'contrastName': ['tone counting probe vs baseline',
                                          'tone counting vs baseline'],
                          'numExc': 1}

    # Initiate a blank string.
    def setUp(self):
        self.testString = ""

    # Setup for individual data
    def getFilePath(self, structData):

        # Open the necessary file.
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "data",
                                     structData["Name"] + "_test")
        return(fileName)

    # Test to see if the software name has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction)
    def test_softwareName(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # Check for the software name.
        for line in postStatsFile:

            if "FMRI" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the software name is what we expected.
        self.assertIn(structData["softwareName"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to see if the software version has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction)
    def test_softwareNum(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # Check for the software version.
        for line in postStatsFile:

            if "Version" in line:

                self.testString = line
                break

        # Verify the software version is what we expected.
        self.assertIn(structData["version"], line,
                      msg='Test failed on ' + structData["Name"])

        # Close the file
        postStatsFile.close()

    # Test to see if the height threshold has been recorded correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default)
    def test_heightThreshold(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        for line in postStatsFile:

            if "statistic images were thresholded" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the height threshold is what we expected.
        self.assertIn(structData["hThresh"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to see if the extent threshold has been recorded correctly.
    @data(fsl_thr_clustfwep05)
    def test_extentThreshold(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # Check for the extent threshold.
        for line in postStatsFile:

            if "statistic images were thresholded using clusters determined by" in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the extent threshold is what we expected.
        self.assertIn(structData["eThresh"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the slice image had been embedded correctly
    @data(fsl_thr_clustfwep05, ex_spm_contrast_mask, ex_spm_conjunction)
    def test_sliceImageExtract(self, structData):

         # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<a href = './Cluster_Data/" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["sliceImExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the FSL logo had been embedded correctly.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction)
    def test_logo(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # This is an extract of the encoding for the FSL logo
        logoExtract = 'WriWP7OC0Zy6j7w4yMeoqnKL9NPivby0uILm1ZSwKEFh0NPvrlodWs' \
                      '7iI7DP+7YnoR1Gf1ouFiBtOspXAjPB5UHncMdv8OtY+qeGVCuUTlef' \
                      'l5yPWtaSN0nu7KL76kXUJP8JJ6fnkGp5L+VYLK4CExSsFcbcjaQf60' \
                      'aMRzGh61deHtQWyuXZ7R8EFuqg9x+ddddWCXMb3FtyCN4CnPNZF7ZC' \
                      '58RwW7IZYolLhtucjHTPfpVvS737Kiyw3J8iQbjC2CFB9OfpTQk7mX'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the logo.
            if '<a href="https://fsl.fmrib.ox.ac.uk/fsl/fslwiki">' in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(logoExtract, self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the lower slice value is given correctly correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default,ex_spm_conjunction)
    def test_LowerSliceVal(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # This is an extract of the encoding for the colorbar
        colorBarExtract = 'P+6AP+yAP+qAP+oAP+gAP+eAP+WAP+MAP+EAP+CAP98AP96AP9y' \
                          'AP9wAP9oAP9mAP9gAP9eAP9WAP9UAP9EAP9CAP86AP84AP8wAP8' \
                          'oAP8mAP8eAP8cAP8WAP8UAP8MAP8KAP/lAP/dAP/bAP/TAP/RAP' \
                          '/JAP/BAP+/AP+3AP+1AP+vAP+tAP+lAP+jAP+bAP+ZAP+TAP+RA' \
                          'P+JAP+HAP9/AP93AP91AP9tAP9rAP9jAP9bAP9ZAP9RAP9PAP9J'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the colorbar and limits.
            if colorBarExtract in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(structData["lowSliceVal"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the upper slice value is given correctly correctly.
    @data(fsl_con_f, fsl_thr_clustfwep05, ex_spm_contrast_mask,
          ex_spm_default, ex_spm_conjunction)
    def test_UpperSliceVal(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # This is an extract of the encoding for the colorbar
        colorBarExtract = 'P+6AP+yAP+qAP+oAP+gAP+eAP+WAP+MAP+EAP+CAP98AP96AP9y' \
                          'AP9wAP9oAP9mAP9gAP9eAP9WAP9UAP9EAP9CAP86AP84AP8wAP8' \
                          'oAP8mAP8eAP8cAP8WAP8UAP8MAP8KAP/lAP/dAP/bAP/TAP/RAP' \
                          '/JAP/BAP+/AP+3AP+1AP+vAP+tAP+lAP+jAP+bAP+ZAP+TAP+RA' \
                          'P+JAP+HAP9/AP93AP91AP9tAP9rAP9jAP9bAP9ZAP9RAP9PAP9J'

        # Check for the FSL logo.
        for line in postStatsFile:

            # If we see this the next line contains the colorbar and limits.
            if colorBarExtract in line:

                self.testString = line
                break

        # Close the file
        postStatsFile.close()

        # Verify the FSL logo contained the extract.
        self.assertIn(structData["highSliceVal"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the contrast name is correctly in postStats.
    @data(fsl_thr_clustfwep05, ex_spm_contrast_mask)
    def test_contrastName(self, structData):

         # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            # We need this line.
            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<h3>Thresholded Activation Images</h3>" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["contrastName"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Check if the contrast name is correctly in postStats in conjunction
    # datasets.
    @data(ex_spm_conjunction)
    def test_contrastName_conjunction(self, structData):

         # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")
        nextLine = False

        # Check for the slice image.
        for line in postStatsFile:

            # We need this line.
            if nextLine:

                self.testString = line
                break

            # If we see this the next line contains the slice image.
            if "<h3>Thresholded Activation Images</h3>" in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertTrue(structData["contrastName"][0] in self.testString and
                        structData["contrastName"][1] in self.testString,
                        msg='Test failed on ' + structData["Name"])

    # Checks if the correct number of pages have been generated.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction, fsl_gamma_basis)
    def test_multiplePageGen(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        clusDir = os.path.join(filePath, 'Cluster_Data')

        # Count the number of files in the cluster data directory.
        numExc = len([name for name in os.listdir(clusDir) if os.path.isfile(
                                                    os.path.join(clusDir, name))])

        # Assert if the number of excursions is correct.
        self.assertTrue(numExc == structData["numExc"],
                        msg='Test failed on ' + structData["Name"])


    # Checks if the correct number of slice images have been generated.
    @data(fsl_con_f, ex_spm_default, ex_spm_conjunction, fsl_gamma_basis)
    def test_multipleConGen(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # Count the number of slice images.
        numSliceIm = 0
        for line in postStatsFile:

            if "a href = './Cluster_Data/" in line:

                numSliceIm = numSliceIm + 1


        # Close the file
        postStatsFile.close()

        # Assert if the number of slice images is correct.
        self.assertTrue(numSliceIm == structData["numExc"],
                        msg='Test failed on ' + structData["Name"])


    # Test to check the correct contrast name matches the correct slice image.
    @data(fsl_contrast_mask, fsl_gamma_basis)
    def test_matchingConName(self, structData):

        # Setup
        filePath = self.getFilePath(structData)
        postStatsFile = open(os.path.join(filePath, 'postStats.html'), "r")

        # Look for the contrast name of interest.
        nextLine = False
        for line in postStatsFile:

            # If this is the line containing the slice image check for the extract
            if nextLine:

                self.testString = line
                break

            # If this line contains the contrast name the next line is the image.
            if structData['matchConName'] in line:

                nextLine = True

        # Close the file
        postStatsFile.close()

        # Verify the slice image contained the extract.
        self.assertIn(structData["matchSliceImExtract"], self.testString,
                      msg='Test failed on ' + structData["Name"])

    # Test to check whether the design matrix is being displayed correctly.
    # def test_designMatrix(self, structData):
# ===============================================================================

if __name__ == "__main__":

    scriptPath = os.path.dirname(os.path.abspath(__file__)) # Get path of script
    dataDir = os.path.join(scriptPath, "data")

    if not os.path.isdir(dataDir): # Data folder does not exist

        os.makedirs(dataDir)


    dataNames = ["fsl_con_f_130",
                 "fsl_thr_clustfwep05_130",
                 "ex_spm_contrast_mask"]
                 # "ex_spm_thr_voxelunct4",
                 # "ex_spm_thr_clustunck10",
                 # "ex_spm_thr_voxelfdrp05"]

    local = True

    for dataName in dataNames: # Check if data is on local machine

        # Data not found on local machine
        if not os.path.isfile(os.path.join(dataDir, dataName + ".nidm.zip")):

            local = False
            break

    if not local:

        # Request from neurovault api
        req = urllib.request.Request(
              "http://neurovault.org/api/collections/2210/nidm_results")
        resp = urllib.request.urlopen(req)
        readResp = resp.read()
        data = json.loads(readResp.decode('utf-8'))

        for nidmResult in data["results"]:

            print(nidmResult["zip_file"])

            zipUrl = nidmResult["zip_file"] # Url of zip file
            dataName = nidmResult["name"] # Name of data (e.g. fsl_con_f.nidm)
            dataNameFile = os.path.join(dataDir, dataName + ".zip")

            if not os.path.isfile(dataNameFile):

                # copy zip file to local machine
                zipFileRequest = urllib.request.urlretrieve(zipUrl,
                                                            dataNameFile)

    globData = os.path.join(dataDir,"*.zip")
    data = glob.glob(globData) # Get names of all zip files in data folder

    for i in data: # Loop over all zip files in data folder and create html

        viewer.main(i, i.replace(".nidm.zip", "") + "_test", overwrite=True)

    unittest.main() # Tests
