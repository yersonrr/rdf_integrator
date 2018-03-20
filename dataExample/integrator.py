import rdflib
from mFuhsionPerfect import MFuhsionPerfect
import configparser
import requests
import json
import os.path
import sys, getopt
import  fileinput
from difflib import SequenceMatcher
import random

allJoins = []
mergedMolecules = []

# When the Class use an URI as a Fusion Policy the Elements to Join will be
# joined by the predicate URI.
def uriPolicy(toJoin, g, g2, fusion_policy):
	gNew = rdflib.Graph()
	for elem in toJoin:
		subject1 = rdflib.URIRef(elem['uri1'])
		for node in g.predicate_objects(subject=subject1):
			gNew.add((subject1, node[0], node[1]))

		subject2 = rdflib.URIRef(elem['uri2'])
		for node in g2.predicate_objects(subject=subject2):
			gNew.add((subject2, node[0], node[1]))

		gNew.add((subject1, rdflib.URIRef(fusion_policy) ,subject2))

	return (gNew.serialize(format='nt'))[:-1]


def unionPolicy(fusion_policy, jsonToJoin):
	headers = {'content-type': "application/json"}
	url = "http://localhost:9001/fusion/"+fusion_policy
	data = jsonToJoin
	data = json.dumps(data)
	response = requests.post(url, data=data, headers=headers)
	return response.text


def getPredicateObject(subjects, graph, index, name_class, class_identifier):

	mergeDict = []

	for s in subjects:

		success = False
		for o in graph.objects(subject=s, predicate=class_identifier):
			if str(o)==name_class:
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


def similarityPart(config, g, g2, class_identifier, class1, n, threshold):
	predicate2compare = int(config.get('Class'+str(n), 'predicate_to_compare'))
	ratio = 0
	subjects_Graph2 = g2.subjects(predicate=rdflib.URIRef(class_identifier),object=rdflib.URIRef(class1))

	toJoin = []

	for subject2 in subjects_Graph2:
		sim_dicc = {}

		for k in range(predicate2compare):
			subjects_Graph = g.subjects(predicate=rdflib.URIRef(class_identifier),object=rdflib.URIRef(class1))
			for subject1 in subjects_Graph:

				predicate1 = config.get('Class'+str(n)+'_P'+str(k+1), 'predicate1')
				predicate2 = config.get('Class'+str(n)+'_P'+str(k+1), 'predicate2')
				objects1 = g.objects(subject=subject1, predicate=rdflib.URIRef(predicate1))
				objects2 = g2.objects(subject=subject2,predicate=rdflib.URIRef(predicate2))

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

		if maxi > 0:
			tupl = {}
			tupl['uri1'] = subject_maxim
			tupl['uri2'] = str(subject2)
			toJoin.append(tupl)
			maxi = 0			

	return toJoin


def getSubject(subjects, graph, toJoin, uri):

	belong = False
	newGraph = rdflib.Graph()
	for subject in subjects:
		for tj in toJoin:
			belong = False

			compare = tj[uri].replace('<','').replace('>','')
			if compare == str(subject):
				belong = True
				
			if belong: 
				break

		if not belong:
			for node in graph:
				if node[0] == subject:
					newGraph.add(node)

	return newGraph


def getUnusedNodes(subjects, subjects2, g, g2, toJoin, F):
	toSearch = getSubject(subjects, g, toJoin, 'uri1')
	toSearch2 = getSubject(subjects2, g2, toJoin, 'uri2')

	len_toSearch = toSearch.serialize(format='nt')
	len_toSearch2 = toSearch2.serialize(format='nt')

	if len(len_toSearch) > 1:
		for s,p,o in toSearch:
			elem = s.n3() + ' '
			elem += p.n3() + ' '
			obj = o.n3().replace('"', '\"')
			elem += obj + '.\n'
			F.write(elem)

	if len(len_toSearch2) > 1:
		for s,p,o in toSearch2:
			elem = s.n3() + ' '
			elem += p.n3() + ' '
			obj = o.n3().replace('"', '\"')
			elem += obj + '.\n'
			F.write(elem)

	return 0


def integratePerClass(g, g2, subjects, subjects2, n, F, config, class_identifier):
	mergeDict = []
	mergeDict2 = []
	index = 0

	n += 1

	threshold = float(config.get('Class'+str(n),'threshold'))
	simfunction = config.get('Class'+str(n),'similarity_metric')
	fusion_policy = config.get('Class'+str(n),'fusion_policy')
	name_class = config.get('Class'+str(n),'class')

	if(simfunction == 'part'):
		toJoin = similarityPart(config, g, g2, class_identifier, name_class, n, threshold)
	
	else:

		mergeDict = getPredicateObject(subjects, g, index, name_class, class_identifier)
		mergeDict2 = getPredicateObject(subjects2, g2, index, name_class, class_identifier)

		perfectOp = MFuhsionPerfect(threshold, simfunction)
		perfectOp.execute_new(mergeDict, mergeDict2)
		
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
			resp_object = resp_object.replace('http://vocab.lidakra.de/fuhsen/search/merged_entity/132131321','http://project-iasis.eu/')
			subject = (resp_object.split())[0]
			mergedUris['uri1'] = '<' + elemToJoin['uri1'] + '>'
			mergedUris['uri2'] = '<' + elemToJoin['uri2'] + '>'
			mergedUris['newUri'] = subject


			global mergedMolecules
			mergedMolecules.append(mergedUris)

		elif fusion_policy != '':
			resp_object = uriPolicy(toJoin, g, g2, fusion_policy)
		else:
			resp_object = []

		try:
			F.write(resp_object.decode("utf-8"))
		except:
			F.write(resp_object)


def newData():
	node = {
      "data" : {
        "id" : "0",
        "selected" : False,
        "cytoscape_alias_list" : [ "Vacherin Haut-Rive" ],
        "canonicalName" : "Vacherin Haut-Rive",
        "SUID" : 0,
        "NodeType" : "WhiteWine",
        "name" : "Vacherin Haut-Rive",
        "shared_name" : "Vacherin Haut-Rive"
      },
      "position" : {
        "x" : 0,
        "y" : 3980.036865234375
      },
      "selected" : False
    }

	edge = {
      "data" : {
        "id" : "0",
        "source" : "0",
        "target" : "0",
        "selected" : False,
        "canonicalName" : "Aarauer Bierdeckel (cc) Bergues",
        "SUID" : 0,
        "name" : "Aarauer Bierdeckel (cc) Bergues",
        "interaction" : "cc",
        "shared_interaction" : "cc",
        "shared_name" : "Aarauer Bierdeckel (cc) Bergues"
      },
      "selected" : False
    }

	return (node, edge)


def integrator(config_file):
	config = configparser.ConfigParser()
	config.read(config_file)
	
	save_path = config.get('RDFData','pathToSave')
	completeName = os.path.join(save_path, "new_rdfGraph.nt")         

	F = open(completeName, "w")

	file_name1 = config.get('RDFData','rdf1')
	file_name2 = config.get('RDFData','rdf2')
	file_ontologies = config.get('RDFData','ontology')

	g=rdflib.Graph()
	result1 = g.parse(location=file_name1, format="nt")
	g2 = rdflib.Graph()
	result2 = g2.parse(location=file_name2, format="nt")
	subjects = []
	predicates = []
	objects = []
	subjects2 = []
	predicates2 = []
	objects2 = []

	for subject,predicate,obj in g:
	    subjects.append(subject)
	    predicates.append(predicate)
	    if 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' == str(predicate):
	    	class_identifier = predicate
	    objects.append(obj)

	for subject,predicate,obj in g2:
	    subjects2.append(subject)
	    predicates2.append(predicate)
	    objects2.append(obj)

	subjects = list(set(subjects))
	subjects2 = list(set(subjects2))

	number_classes = int(config.get('RDFData','number_classes'))

	FileAux = open('auxFile.nt', 'w+')

	f = open(file_ontologies, 'r')
	for line in f.readlines():
		FileAux.write(line)
	f.close()

	f = open(file_name1, 'r')
	for line in f.readlines():
		FileAux.write(line)
	f.close()

	f = open(file_name2, 'r')
	for line in f.readlines():
		FileAux.write(line)
	f.close()
	FileAux.close()

	ontology_path = os.path.realpath(FileAux.name)

	url = "http://localhost:9000/similarity/initialize?model_1="+ontology_path
	headers = {'content-type': "application/json"}
	response = requests.get(url, headers=headers)

	url = "http://localhost:9001/setlocation"
	data = {"location1":file_name1, 
		"location2":file_name2}
	data = json.dumps(data)
	response = requests.post(url, data=data, headers=headers)

	for n in range(number_classes):
		integratePerClass(g, g2, subjects, subjects2, n, F, config, class_identifier)

	getUnusedNodes(subjects, subjects2, g, g2, allJoins, F)

	F.close()

	for line in fileinput.input(completeName, inplace=True):
		global mergedMolecules
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

	g=rdflib.Graph()
	result1 = g.parse(location=file_name1, format="nt")
	g2 = rdflib.Graph()
	result2 = g2.parse(location=file_name2, format="nt")
	jsonData = {
		"format_version" : "1.0",
	 	"generated_by" : "cytoscape-3.2.0",
	  	"target_cytoscapejs_version" : "~2.1",
	  	"data" : {
		    "selected" : True,
		    "__Annotations" : [],
		    "shared_name" : "WineCheeseNetwork",
		    "SUID" : 52,
		    "name" : "WineCheeseNetwork"
	  	},
	  	"elements" : {
	  		"nodes":[],
	  		"edges":[],
	  	}
  	}

	idGraph = 53

	node, edge = newData()

    # Uri 1    1391 RedWine
    # Uri 2    6593 WhiteWine
	y = 2130

	for elem in allJoins:
		uri1 = elem['uri1']
		uri2 = elem['uri2']

		node["data"]["id"] = str(idGraph)
		node["SUID"] = idGraph
		node["data"]["NodeType"] = "RedWine"
		node["data"]["cytoscape_alias_list"] = [uri1]
		node["data"]["canonicalName"] = uri1
		node["data"]["name"] = uri1
		node["data"]["shared_name"] = uri1

		node["position"]["x"] = 1391
		node["position"]["y"] = y

		jsonData["elements"]["nodes"].append(node)
		idGraph += 1

		node, edge = newData()

		node["data"]["id"] = str(idGraph)
		node["SUID"] = idGraph
		node["data"]["NodeType"] = "WhiteWine"
		node["data"]["cytoscape_alias_list"] = [uri2]
		node["data"]["canonicalName"] = uri2
		node["data"]["name"] = uri2
		node["data"]["shared_name"] = uri2

		node["position"]["x"] = 6593
		node["position"]["y"] = y

		y += 49
		jsonData["elements"]["nodes"].append(node)
		idGraph += 1

		node, edge = newData()

		node["data"]["id"] = str(idGraph)
		node["SUID"] = idGraph
		node["data"]["NodeType"] = "Cheese"
		node["data"]["cytoscape_alias_list"] = ['Relation']
		node["data"]["canonicalName"] = 'Relation'
		node["data"]["name"] = 'Relation'
		node["data"]["shared_name"] = 'Relation'

		node["position"]["x"] = random.randint(1400, 6550)
		node["position"]["y"] = random.randint(2130, 6550)

		jsonData["elements"]["nodes"].append(node)
		
		idGraph += 1 

		source = idGraph - 3
		target = idGraph - 2

		connection = idGraph - 1

		node, edge = newData()

		edge['data']['id'] = str(idGraph)
		edge['data']['source'] = str(source)
		edge['data']['target'] = str(connection)
		edge['data']['cannonicalName'] = uri1 + ' (cc) Connection'
		edge['data']['SUID'] = idGraph
		edge['data']['name'] = uri1 + ' (cc) Connection'
		edge['data']['shared_name'] = uri1 + ' (cc) Connection'
		jsonData["elements"]["edges"].append(edge)
	
		idGraph += 1

		node, edge = newData()

		edge['data']['id'] = str(idGraph)
		edge['data']['source'] = str(target)
		edge['data']['target'] = str(connection)
		edge['data']['cannonicalName'] = uri2 + ' (cc) Connection'
		edge['data']['SUID'] = idGraph
		edge['data']['name'] = uri2 + ' (cc) Connection'
		edge['data']['shared_name'] = uri2 + ' (cc) Connection'
		jsonData["elements"]["edges"].append(edge)

		idGraph += 1

		#Connections Uri1
		subject = rdflib.URIRef(uri1)
		subject2 = rdflib.URIRef(uri2)

		for data in g.predicate_objects(subject=subject):
			node, edge = newData()

			node["data"]["id"] = str(idGraph)
			node["SUID"] = idGraph
			node["data"]["NodeType"] = "Cheese"
			node["data"]["cytoscape_alias_list"] = [data[1].n3()]
			node["data"]["canonicalName"] = data[1].n3()
			node["data"]["name"] = data[1].n3()
			node["data"]["shared_name"] = data[1].n3()

			node["position"]["x"] = random.randint(1400, 6550)
			node["position"]["y"] = random.randint(2130, 6550)
			jsonData["elements"]["nodes"].append(node)
			idGraph += 1

			connection = idGraph - 1

			edge['data']['id'] = str(idGraph)
			edge['data']['source'] = str(source)
			edge['data']['target'] = str(connection)
			edge['data']['cannonicalName'] = data[1].n3() + ' (cc) Connection'
			edge['data']['SUID'] = idGraph
			edge['data']['name'] = data[1].n3() + ' (cc) Connection'
			edge['data']['shared_name'] = data[1].n3() + ' (cc) Connection'
			jsonData["elements"]["edges"].append(edge)

			idGraph += 1

		for data in g2.predicate_objects(subject=subject2):
			node, edge = newData()

			node["data"]["id"] = str(idGraph)
			node["SUID"] = idGraph
			node["data"]["NodeType"] = "Cheese"
			node["data"]["cytoscape_alias_list"] = [data[1].n3()]
			node["data"]["canonicalName"] = data[1].n3()
			node["data"]["name"] = data[1].n3()
			node["data"]["shared_name"] = data[1].n3()

			node["position"]["x"] = random.randint(1400, 6550)
			node["position"]["y"] = random.randint(2130, 6550)
			jsonData["elements"]["nodes"].append(node)
			idGraph += 1

			connection = idGraph - 1

			edge['data']['id'] = str(idGraph)
			edge['data']['source'] = str(target)
			edge['data']['target'] = str(connection)
			edge['data']['cannonicalName'] = data[1].n3() + ' (cc) Connection'
			edge['data']['SUID'] = idGraph
			edge['data']['name'] = data[1].n3() + ' (cc) Connection'
			edge['data']['shared_name'] = data[1].n3() + ' (cc) Connection'
			jsonData["elements"]["edges"].append(edge)

			idGraph += 1

	with open('result.json', 'w') as fp:
		json.dump(jsonData, fp)


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
	integrator(config_file)


if __name__ == "__main__":
    main()