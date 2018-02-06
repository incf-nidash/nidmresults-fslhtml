# ============================================================================
# This file contains a list of functions use to manipulate queries.
#
# Authors: Peter Williams, Tom Maullin, Camille Maumet (09/01/2018)
# ============================================================================
import os


# This function takes as input a query and returns a query list.
def addQueryToList(query):

    queryList = []

    for i in query:

        for j in i:

            queryList.append("%s" % j)

    return(queryList)


# Function for printing the results of a query.
def printQuery(query):

    # Print each row.
    for row in query:

        if len(row) == 1:

            print("%s" % row)

        elif len(row) == 2:

            print("%s, %s" % row)

        elif len(row) == 3:

            print("%s, %s, %s" % row)

        else:

            print("Error, not a suitable length")


# This function runs a query of either queryType 'Ask' or 'Select'. Filters
# can be added also.
def runQuery(graph, queryFile, queryType, filters={}):

    # Open the file and read it in.
    queryFile = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  queryFile + '.txt'))
    queryText = queryFile.read()
    queryFile.close()

    # If there are any filters specified add them to the query.
    for fil in filters:

        queryText = queryText.replace('{{{' + fil + '}}}', filters[fil])

    # Run the query.
    queryOutput = graph.query(queryText)

    # If we are asking we only want true if something was returned.
    if queryType == 'Ask':

        for row in queryOutput:

            queryResult = row

        if queryResult:

            return(True)

        else:

            return(False)

    # If we are selecting we want a list of outputs
    if queryType == 'Select':

        return(addQueryToList(queryOutput))
