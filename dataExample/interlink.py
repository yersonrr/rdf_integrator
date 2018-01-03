import rdflib
import requests
import sys, getopt
from SPARQLWrapper import SPARQLWrapper, JSON
import ConfigParser


def interlink_old(completeName):
	g = rdflib.Graph()
	graph = g.parse(location=completeName, format="nt")

	predicate_type = rdflib.URIRef('https://www.w3.org/1999/02/22-rdf-syntax-ns#/type')
	object_drug = rdflib.URIRef('http://iasis/vocab/prescriptedDrug')

	predicate_id = rdflib.URIRef('http://iasis/vocab/id')
	predicate_seeAlso = rdflib.URIRef('https://www.w3.org/2000/01/rdf-schema#seeAlso')

	#Adding DRUG URIS 
	for subject in graph.subjects(predicate=predicate_type,object=object_drug):
		for object_drug in graph.objects(subject=subject, predicate=predicate_id):
			drugUri = rdflib.URI('https://www.drugbank.ca/drugs/'+ object_drug)
			graph.add((subject, predicate_seeAlso, drugUri))

	#Adding Annotation URIS
	annotations = []
	annotations.append(rdflib.URIRef('http://iasis/vocab/Condannotationtation'))
	annotations.append(rdflib.URIRef('http://iasis/vocab/annotation'))
	annotations.append(rdflib.URIRef('http://iasis/vocab/Interannotation'))
	annotations.append(rdflib.URIRef('http://iasis/vocab/LCannotation'))
	annotations.append(rdflib.URIRef('http://iasis/vocab/ADannotation'))

	label = rdflib.URIRef('http://iasis/vocab/annLabel')

	for annotation in annotations:
		for subject in graph.subjects(predicate=predicate_type,object=annotation):
			for object_annotation in graph.predicate_objects(subject=subject):
				
				if object_annotation[0] != rdflib.URIRef('http://iasis/vocab/annLabel'):
					continue

				# DBPedia Annotations
				label = object_annotation[1].split()
				dbpedia_label = label[0].lower().capitalize()
				for elem in label[1:]:
					dbpedia_label += '_' + elem.lower()

				request = requests.get('http://dbpedia.org/resource/'+dbpedia_label)

				if request.status_code == 200:
					dbpediaAnnotation = rdflib.URIRef('http://dbpedia.org/resource/'+dbpedia_label)
					graph.add((subject, predicate_seeAlso, dbpediaAnnotation))
				else:
					for word in object_annotation[1].split():
						dbpedia_label = word.lower().capitalize()
						request = requests.get('http://dbpedia.org/resource/'+dbpedia_label)
						if request.status_code == 200:
							dbpediaAnnotation = rdflib.URIRef('http://dbpedia.org/resource/'+dbpedia_label)
							graph.add((subject, predicate_seeAlso, dbpediaAnnotation))
	

	file = open(completeName, "w")
	file.write(g.serialize(format='nt'))
	file.close()

def searchByEndpoint(graph, n, config):

	n += 1
	endpoint = config.get('KG'+str(n),'endpoint')
	sim_metric = config.get('KG'+str(n),'similary_metric')
	treshold = float(config.get('KG'+str(n),'treshold'))
	fusion = config.get('KG'+str(n),'fusion_policy')

	class1 = config.get('KG'+str(n),'class1')
	class2 = config.get('KG'+str(n),'class2')

	ontology = config.get('KG'+str(n),'ontologyKG')
	mapping = config.get('KG'+str(n),'mapping')

	sparql = SPARQLWrapper(endpoint)
	query = """select * where {?s rdf:type <"""+class2+""">.
			filter (!isBlank(?s))}"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	subjects_query = []
	for result in results["results"]["bindings"]:
		subjects_query.append(result['s']['value'])

	#for subject in subjects_query:
	query = """select * where {<"""+ subjects_query[0] +"""> ?p ?o.
		filter (!isBlank(?s))}"""

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	for result in results['results']['bindings']:
		print "Data example -------------------"
		print result['p']['value']
		print result['o']['value']
	
	"""graph = rdflib.Graph()
	elem = graph.parse(format='n3', data=results)
	
	for s,p,o in elem:
		print s
		print p 
		print o


	F = open('exampledata.nt', "w")
	F.write(elem.serialize(format='nt'))
	F.close()"""


def interlinking(config_file):
	config = ConfigParser.ConfigParser()
	config.read(config_file)
	
	file_name1 = config.get('RDFData','rdf')
	file_ontologies = config.get('RDFData','ontology')
	number_kg = int(config.get('RDFData','number_kg'))
	
	g=rdflib.Graph()
	result1 = g.parse(location=file_name1, format="nt")

	for n in range(number_kg):
		searchByEndpoint(g, n, config)


def readConfig():
	argv = sys.argv[1:]
	try:
		opts, args = getopt.getopt(argv, 'hc:', 'configFile=')
	except getopt.GetoptError:
		print('python integrator.py -c <configFile>')
		sys.exit(1)

	if len(opts) == 0:
		print('Error: python integrator.py -c <configFile>')
		sys.exit(1)

	for opt, arg in opts:
		if opt == '-h':
			print('python integrator.py -c <configFile>')
			sys.exit()
		elif opt == '-c' or opt == '--configFile':
			config_file = arg

	return config_file


def main():

	config_file = readConfig()
	interlinking(config_file)


if __name__ == "__main__":
    main()