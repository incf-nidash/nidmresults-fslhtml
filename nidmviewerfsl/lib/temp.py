#!/usr/bin/env python3
# ======================================================================
#
# This file contains functions used for formatting statistical data
# returned by SPARQL queries on NIDM-Results packs.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet (10/01/18)
#
# ======================================================================
from queries.querytools import runQuery
from style.pagestyling import encodeImage
import numpy as np
import random
import os
import math
import matplotlib
import rdflib
import glob
matplotlib.use('Agg')

def getFileName(g, excName):

    # For SPM data we can't work out the filename we want from just
    # the contrast name.
    if runQuery(g, 'askSPM', 'Ask'):
        
        # For SPM data we must look for the statistic map to
        # assert which statistic is associated to a contrast.
        statisticMap = runQuery(g, 'selectStatMap', 'Select',
                                {'EXC_NAME': excName})[0]

        # If it's T stat string is '', if it's F statstring
        # is 'f'
        if statisticMap[0] == 'T':
            statString = ''
        else:
            statString = statisticMap[0].lower()

        return('cluster_z' + statString + 'stat1_std.html')

    else:

        # In FSL the excursion set maps are always of the form
        # ExcursionSet_(stattype)00(number), unless only one T
        # statistic was computed. Then the excursion set map is
        # names ExcursionSet.
        if '_F' in excName:

            statString = 'f'

        else:

            statString = ''

        number = excName.replace('.nii.gz', '')[-1]

        if number == 't':

            number = '1'

        return('cluster_z' + statString + 'stat' + number + '_std.html')


g = rdflib.Graph()
turtleFile = glob.glob('/home/tommaullin/Documents/Repos/nidmresults-fslhtml/nidmviewerfsl/tests/data/ex_spm_temporal_derivative_test_err/nidm.ttl')

g.parse(turtleFile[0], format = "turtle")

#For now using nifti name... want to use proper contrast name field.
conName = "ExcursionSet.nii.gz"
print(getFileName(g, conName))
