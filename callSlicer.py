import subprocess

exc_set = 'ExcursionSet.nii.gz'
template = 'MNI152_T1_2mm_brain.nii.gz'

#Write bash commands to retrieve min and max values using fslstats.
calcMinZ = "fslstats '" + exc_set + "' -l 0.01 -R | awk '{print $1}'"
calcMaxZ = 'fslstats ' + exc_set + " -l 0.01 -R | awk '{print $2}'"

#Process the min command to obtain the minimum value
process = subprocess.Popen(calcMinZ, shell=True, stdout=subprocess.PIPE)
output = process.communicate()
minZ = output[0].decode('utf-8').rstrip('\r|\n')

#Process the max command to obtain the maximum value
process = subprocess.Popen(calcMaxZ, shell=True, stdout=subprocess.PIPE)
output = process.communicate()
maxZ = output[0].decode('utf-8').rstrip('\r|\n')

#Place the template onto the excursion set using overlay
overlayCommand = "overlay 1 1 " + template + " -a " + exc_set + " " + minZ + " " + maxZ + " outputTemp"
process = subprocess.Popen(overlayCommand, shell=True)
process.wait()

#Get Slices
slicerCommand = "slicer 'outputTemp.nii.gz' -S 2 900 'slices.png'"
subprocess.Popen(slicerCommand, shell=True)


#Bash command for next bit
flirt -init matrix.mat -in ExcursionSet.nii.gz -ref MNI152_T1_2mm_brain.nii.gz -out resampledTemplate -applyxfm
#Matrix
1 0 0 halfxoff
0 1 0 halfyoff
0 0 1 0
0 0 0 1
