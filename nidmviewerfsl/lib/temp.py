import os
import glob
import rdflib
from queries.queryTools import runQuery, printQuery
from scipy.misc import toimage

turtleFile = glob.glob('/home/tom/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_conjunction_test/nidm.ttl')
#turtleFile = glob.glob('C:/Users/owner/Documents/NISOx/Peters_Viewer/nidmresults-fslhtml/Tests/data/ex_spm_partial_conjunction_test/nidm.ttl')

print(turtleFile)
g = rdflib.Graph()
g.parse(turtleFile[0], format = "turtle")

t = runQuery(g, 'selectContrastVector', 'Select')
print(runQuery(g, 'selectContrastVector', 'Select'))

conVec = t[1].replace('[', '').replace(']', '').replace(',', '').split()
conVec = [float(conVec[i]) for i in range(0, len(conVec))]
print(conVec)
