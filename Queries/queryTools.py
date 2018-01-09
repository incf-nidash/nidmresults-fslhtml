#==============================================================================
# This function takes as input a query and returns a query list.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet (09/01/2018)
#==============================================================================

def addQueryToList(query):
    
    queryList = []

    for i in query:

        for j in i:

            queryList.append("%s" % j)

    return(queryList)