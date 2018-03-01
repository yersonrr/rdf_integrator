import rdflib
import requests
import sys, getopt
from SPARQLWrapper import SPARQLWrapper, JSON
import configparser
import os
import json
from mFuhsionPerfect import MFuhsionPerfect
import urllib
from difflib import SequenceMatcher
import sys, getopt
import  fileinput

allJoins = []
mergedMolecules = []

def fuhsionPolicy(toJoin, g, molecule, predicate):
	gNew = rdflib.Graph()
	for elem in toJoin:
		subject1 = rdflib.URIRef(elem['uri1'])
		for node in g.predicate_objects(subject=subject1):
			gNew.add((subject1, node[0], node[1]))

		subject2 = rdflib.URIRef(molecule['head']['uri'])

		gNew.add((subject1, rdflib.URIRef(predicate) ,subject2))

	return gNew.serialize(format='nt')


def unionPolicy(fusion_policy, jsonToJoin):
	headers = {'content-type': "application/json"}
	url = "http://localhost:9001/fusion/"+fusion_policy
	data = jsonToJoin
	data = json.dumps(data)
	response = requests.post(url, data=data, headers=headers)
	return response.text


def getPredicateObject(subjects, graph, name_class, class_identifier):

	# Name_class is used for create a graph with diferent predicates class, for example the RDF:TYPE.
	# Class_identifier: Needed to add the nodes to be integrated in the graph.

	mergeDict = []
	index = 0

	for s in subjects:

		success = False
		for o in graph.objects(subject=s, predicate=name_class):
			if str(o)==class_identifier:
				success = True

		if not success:
			continue
		
		dict_new = {}
		dict_new['head'] = {}
		dict_new['head']['index'] = index
		index += 1
		dict_new['head']['uri'] = s.n3()

		dict_new['head']['row'] = True
		dict_new['tail'] = []
		for i in graph.predicate_objects(subject=s):
			dict_predicateObject = {}
			# PREDICATE = PROP
			dict_predicateObject['prop'] = i[0].n3()
			# OBJECT = VALUE
			dict_predicateObject['value'] = i[1].n3()
			dict_new['tail'].append(dict_predicateObject)

		mergeDict.append(dict_new)

	return mergeDict


def similarValue(a,b):
	return SequenceMatcher(None, a, b).ratio()


def similarityPart(config, graph, gNew, subject, class_identifier, class1, n, threshold):
	predicate2compare = int(config.get('KG'+str(n), 'predicate_to_compare'))
	ratio = 0
	subjects_Graph = graph.subjects(predicate=rdflib.URIRef(class_identifier),object=rdflib.URIRef(class1))

	sim_dicc = {}
	for k in range(predicate2compare):
		for subject1 in subjects_Graph:
			predicate1 = config.get('KG'+str(n)+'_P'+str(k+1), 'predicate1')
			predicate2 = config.get('KG'+str(n)+'_P'+str(k+1), 'predicate2')
			objects1 = graph.objects(subject=subject1, predicate=rdflib.URIRef(predicate1))
			objects2 = gNew.objects(subject=rdflib.URIRef(subject),predicate=rdflib.URIRef(predicate2))
			maxim = 0
			for obj1 in objects1:
				for obj2 in objects2:
					val = similarValue(obj1, obj2)
					if (val > maxim and val > threshold):
						maxim = val

			if(maxim > 0):
				try:
					sim_dicc[subject1] += maxim*1.0/predicate2compare
				except:
					sim_dicc[subject1] = maxim*1.0/predicate2compare

	maxi = 0
	subject_maxim = ''
	for elem in sim_dicc:
		if (maxi < sim_dicc[elem] and sim_dicc[elem] > threshold):
			maxi = sim_dicc[elem]
			subject_maxim = elem

	toJoin = []
	if maxi > 0:
		tupl = {}
		tupl['uri1'] = subject_maxim
		tupl['uri2'] = str(subject)
		toJoin.append(tupl)

	return toJoin


def searchByEndpoint(graph, n, config):

	file_ontologies = config.get('RDFData','ontology')

	n += 1
	index = 0
	endpoint = config.get('KG'+str(n),'endpoint')
	simfunction = config.get('KG'+str(n),'similary_metric')
	threshold = float(config.get('KG'+str(n),'threshold'))
	fusion_policy = config.get('KG'+str(n),'fusion_policy')

	class1 = config.get('KG'+str(n),'class1')
	class2 = config.get('KG'+str(n),'class2')

	ontology = config.get('KG'+str(n),'ontologyKG')
	mapping = config.get('KG'+str(n),'mapping')

	subjects = []
	predicates = []
	objects = []

	for subject,predicate,obj in graph:
	    subjects.append(subject)
	    predicates.append(predicate)
	    if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' == str(predicate):
	    	class_identifier = predicate
	    objects.append(obj)

	sparql = SPARQLWrapper(endpoint)
	query = """select * where {?s rdf:type <"""+class2+""">.
			filter (!isBlank(?s))}"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	subjects_query = []
	for result in results["results"]["bindings"]:
		subjects_query.append(result['s']['value'])

	number_aux = 0
	ntriples = ''

	Finterlink = open('interlink_prueba.nt','w+')

	for subject in subjects_query:
		gNew = rdflib.Graph()

		query = """select * where {<"""+ subject +"""> ?p ?o.}"""

		if number_aux > 0:
			os.remove('aux'+str(number_aux-1)+'.nt')

		FileAux = open('aux'+str(number_aux)+'.nt', "w+")
		number_aux += 1

		sparql.setQuery(query)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		molecule_endpoint = {}
		molecule_endpoint['head'] = {}
		molecule_endpoint['head']['index'] = index
		index += 1
		molecule_endpoint['head']['uri'] = subject
		molecule_endpoint['head']['row'] = True
		molecule_endpoint['tail'] = []

		for result in results['results']['bindings']:
			predicate = rdflib.URIRef(result['p']['value'])
			try:
				object_rdf = float(result['o']['value'])
				object_rdf = rdflib.Literal(result['o']['value'])
			except:
				try:
					# If URI
					object_rdf = rdflib.URIRef(result['o']['value'])
					object_rdf.n3()
				except:
					# If Literal
					object_rdf = rdflib.Literal((result['o']['value']))

			
			gNew.add((rdflib.URIRef(subject), predicate, object_rdf))

			dict_predicateObject = {}
			# PREDICATE = PROP
			dict_predicateObject['prop'] = predicate.n3()
			# OBJECT = VALUE
			dict_predicateObject['value'] = object_rdf.n3()
			molecule_endpoint['tail'].append(dict_predicateObject)

		'''for o in gNew.objects(subject=rdflib.URIRef(subject),predicate=rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#label')):
			print('OBJETO')
			print(o)
		'''
		if(simfunction == 'part'):
			toJoin = similarityPart(config, graph, gNew, subject, class_identifier, class1, n, threshold)
		else:
			f = open(ontology)
			for line in f.readlines():
				FileAux.write(line)

			f.close()

			f = open(file_ontologies)
			for line in f.readlines():
				FileAux.write(line)

			f.close()

			f = open(mapping)
			for line in f.readlines():
				FileAux.write(line)

			f.close()

			for s,p,o in gNew:
				elem = s.n3() + ' '
				elem += p.n3() + ' '
				obj = o.n3().replace('"', '\"')
				elem += obj + ' .\n'
				FileAux.write(elem)

			for s,p,o in graph:
				elem = s.n3() + ' '
				elem += p.n3() + ' '
				obj = o.n3().replace('"', '\"')
				elem += obj + ' .\n'
				FileAux.write(elem)

			FileAux.close()

			ontology_path = os.path.realpath(FileAux.name)


			url = "http://localhost:9000/similarity/initialize?model_1="+ontology_path
			headers = {'content-type': "application/json"}
			response = requests.get(url, headers=headers)

			"""url = "http://localhost:9001/setlocation"
			data = {"location1":ontology_path, "location2":''}
			data = json.dumps(data)
			response = requests.post(url, data=data, headers=headers)
			"""
			mergeDict = getPredicateObject(subjects, graph, class_identifier, class1)

			perfectOp = MFuhsionPerfect(threshold, simfunction)

			array_molecule = []
			array_molecule.append(molecule_endpoint)
			perfectOp.execute_new(mergeDict, array_molecule)

			toJoin = []
			for tpl in perfectOp.toBeJoined:
				tupl = {}
				tupl['uri1'] = str(tpl[0])
				tupl['uri2'] = str(tpl[1])
				toJoin.append(tupl)

		global allJoins
		allJoins += toJoin

		for elem in toJoin:
			elem['uri1'] = elem['uri1'].replace('<','').replace('>','')
			elem['uri2'] = elem['uri2'].replace('<','').replace('>','')


		for elemToJoin in toJoin:
			jsonToJoin = {}
			jsonToJoin["tasks"] = [elemToJoin]

			if fusion_policy == 'union':
				mergedUris = {}
				resp_object = unionPolicy(fusion_policy, jsonToJoin)
				resp_object = resp_object.replace('http://vocab.lidakra.de/fuhsen/search/merged_entity','http://project-iasis.eu/vocab/')
				subject = (resp_object.split())[0]
				mergedUris['uri1'] = '<' + elemToJoin['uri1'] + '>'
				mergedUris['uri2'] = '<' + elemToJoin['uri2'] + '>'
				mergedUris['newUri'] = subject

				mergedMolecules.append(mergedUris)

			elif fusion_policy != '':
				resp_object = fuhsionPolicy(toJoin, graph, molecule_endpoint, fusion_policy)
			else:
				resp_object = ''

			Finterlink.write(resp_object.decode("utf-8"))

	Finterlink.close()

	save_path = config.get('RDFData','pathToSave')
	completeName = os.path.join(save_path, "new_rdfGraph2.nt")

	file = open(completeName, "w")
	for s,p,o in graph:
			elem = s.n3() + ' '
			elem += p.n3() + ' '
			obj = o.n3().replace('"', '\"')
			elem += obj + '.\n'
			file.write(elem)

	g=rdflib.Graph()
	g.parse(location='interlink_prueba.nt', format="nt")

	for s,p,o in g:
			elem = s.n3() + ' '
			elem += p.n3() + ' '
			obj = o.n3().replace('"', '\"')
			elem += obj + '.\n'
			file.write(elem)
	file.close()

	for line in fileinput.input(completeName, inplace=True):
		replace = False
		for elem in mergedMolecules:
			if (line.find(elem['uri1']) > 0):
				print(line.replace(elem['uri1'],elem['newUri'])[:-1])
				replace = True
			elif (line.find(elem['uri2']) > 0):
				print(line.replace(elem['uri2'],elem['newUri'])[:-1])
				replace = True
		if not (replace):
			print(line[:-1])
	
	g = rdflib.Graph()
	result = g.parse(location=completeName, format="nt")

	file = open(completeName, "w")
	for s,p,o in g:
			elem = s.n3() + ' '
			elem += p.n3() + ' '
			obj = o.n3().replace('"', '\"')
			elem += obj + '.\n'
			file.write(elem)
	file.close()
	return

def interlinking(config_file):
	config = configparser.ConfigParser()
	config.read(config_file)
	
	file_name1 = config.get('RDFData','rdf')
	number_kg = int(config.get('RDFData','number_kg'))
	save_path = config.get('RDFData','pathToSave')
	completeName = os.path.join(save_path, "new_rdfGraph.nt")

	g=rdflib.Graph()
	g.parse(location=file_name1, format="nt")

	global mergedMolecules

	for n in range(number_kg):
		if n > 0:		
			completeName = os.path.join(save_path, "new_rdfGraph2.nt")
			g=rdflib.Graph()
			g.parse(location=completeName, format="nt")
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