import rdflib
import markup

g = rdflib.Graph()
g.parse("pain_15.nidm.ttl", format = rdflib.util.guess_format("pain_15.nidm.ttl"))

query = """prefix nidm: <http://purl.org/nidash/nidm#>
prefix prov: <http://www.w3.org/ns/prov#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?versionNum WHERE {?a nidm:NIDM_0000122 ?versionNum . OPTIONAL {?a rdfs:label ?label} }"""

queryResult = g.query(query)
for row in queryResult:

	print("%s, %s" %row)
