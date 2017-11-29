import subprocess
import os
import shutil
import random

def nifDim(niftiFilename, k):
    #Retrieve the k dimension of a nifti given it's filename using FSL.
    
    if k == 'x':
        arg = 'dim1'
    elif k == 'y':
        arg = 'dim2'
    elif k == 'z':
        arg = 'dim3'
    elif k == 'pix':
        arg = 'pixdim1'
    else:
        error('Enter a valid dimension... x, y, z or pix')

    #Make the command
    getDimString = "fslhd " + niftiFilename + " | cat -v | grep ^" + arg
    print(getDimString)
    #Run the command
    process = subprocess.Popen(getDimString, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()
    print(output[0].decode('utf-8').rstrip('\r|\n').replace(arg, '').replace(' ', ''))
    dimension = int(float(output[0].decode('utf-8').rstrip('\r|\n').replace(arg, '').replace(' ', '')))
    
    return(dimension)

def createResizeMatrix(niftiFilename1, niftiFilename2, scalefactor, tempDir):
    #This creates the resize matrix for the resizing of the niftis and saves it as resizeMatrix.mat

    xShift = abs(nifDim(niftiFilename1, 'x') - nifDim(niftiFilename2, 'x'))
    yShift = abs(nifDim(niftiFilename1, 'y') - nifDim(niftiFilename2, 'y'))

    #Open the matrix file.
    matrixFile = open(os.path.join(tempDir, 'resizeMatrix.mat'), 'w')

    #Write the matrix file
    matrixFile.write('1 0 0 ' + str(scalefactor*xShift) + ' \n')
    matrixFile.write('0 1 0 ' + str(scalefactor*yShift) + ' \n')
    matrixFile.write('0 0 1 0 \n')
    matrixFile.write('0 0 0 1 \n')

    #Close the matrix file.
    matrixFile.close()

def resize(exc_set, template, scalefactor, tempDir):
    #This function resizes a nifti to a template if necessary, assuming the volume of the
    #brain in both the template and excursion set are the same and they are correctly aligned.

    #Create necessary tranformation.
    createResizeMatrix(exc_set, template, scalefactor, tempDir)
    
    #Run the command  if necessary.
    resizeCommand = "flirt -init " + os.path.join(tempDir, "resizeMatrix.mat") + " -in " + exc_set + " -ref " + template + " -out " + os.path.join(tempDir, "resizedNifti.nii.gz") + " -applyxfm"
    process = subprocess.Popen(resizeCommand, shell=True)
    process.wait()
    

def getVal(niftiFilename, minOrMax):
    #Retrieve the min or max values of the image.
    
    if minOrMax == 'min':
        getValString = "fslstats '" + niftiFilename + "' -l 0.01 -R | awk '{print $1}'"
    elif minOrMax == 'max':
        getValString = 'fslstats ' + niftiFilename + " -l 0.01 -R | awk '{print $2}'"
    else:
        error('Please enter "min" or "max"')

    #Process the command to obtain the value
    process = subprocess.Popen(getValString, shell=True, stdout=subprocess.PIPE)
    output = process.communicate()

    #Return value.
    return(output[0].decode('utf-8').rstrip('\r|\n'))

def overlay(exc_set, template, tempDir):
    #Overlay exc_set onto template. The output is saved as outputTemp

    #Get min and max values of the excursion set.
    minZ = getVal(exc_set, 'min')
    maxZ = getVal(exc_set, 'max')
    
    #Place the template onto the excursion set using overlay
    overlayCommand = "overlay 1 1 " + template + " -a " + exc_set + " " + minZ + " " + maxZ + " " + os.path.join(tempDir, "outputTemp.nii.gz")
    process = subprocess.Popen(overlayCommand, shell=True)
    process.wait()

def getSliceImageFromNifti(tempDir, outputName):
    #Get Slices. Slices are saved as slices.png.
    
    slicerCommand = "slicer '" + os.path.join(tempDir, "outputTemp.nii.gz") + "' -S 2 900 '"+ outputName + "'"
    process = subprocess.Popen(slicerCommand, shell=True)
    process.wait()
    
def generateSliceImage(exc_set):
    
    tempFolder = 'temp_NIDM_viewer' + str(random.randint(0, 999999))
    os.mkdir(tempFolder)
    
    #Find the template. If we can't find an appropriate template scaling will be required later.
    if nifDim(exc_set, 'pix') == 1:
        template = '${FSLDIR}/data/standard/MNI152_T1_1mm_brain.nii.gz'
        scalefactor = 1
    elif nifDim(exc_set, 'pix') == 2:
        template = '${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz'
        scalefactor = 1
    else:
        template = '${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz'
        scalefactor = 1/nifDim(exc_set, 'pix')

    #Check which is bigger and resize if necessary
    resize(exc_set, template, scalefactor, tempFolder)
    resized_exc_set = os.path.join(tempFolder, 'resizedNifti.nii.gz')

    #Overlay niftis
    overlay(resized_exc_set, template, tempFolder)

    #Get the slices image
    getSliceImageFromNifti(tempFolder, exc_set.replace('.nii', '').replace('.gz','')+'.png')

    shutil.rmtree(tempFolder)

    return(exc_set.replace('.nii', '').replace('.gz','')+'.png')

generateSliceImage('/home/tom/Documents/Repos/nidmresults-fslhtml/Tests/data/ex_spm_conjunction_test/ExcursionSet.nii.gz')

