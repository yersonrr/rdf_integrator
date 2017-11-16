import rdflib
from mFuhsionPerfect import MFuhsionPerfect
import ConfigParser
import requests
import json
import os.path
import sys, getopt

def integrator(config_file):
	config = ConfigParser.ConfigParser()
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
	    objects.append(obj)

	for subject,predicate,obj in g2:
	    subjects2.append(subject)
	    predicates2.append(predicate)
	    objects2.append(obj)

	subjects = list(set(subjects))
	subjects2 = list(set(subjects2))

	mergeDict = []
	mergeDict2 = []
	index = 0

	threshold = float(config.get('Class','threshold'))
	simfunction = config.get('Class','similarity_metric')
	fusion_policy = config.get('Class','fusion_policy')

	for s in subjects:
		dict_new = {}
		dict_new['head'] = {}
		dict_new['head']['index'] = index
		index += 1
		dict_new['head']['uri'] = s.n3()
		dict_new['head']['row'] = True
		dict_new['tail'] = []
		for i in g.predicate_objects(subject=s):
			dict_predicateObject = {}
			# PREDICATE = PROP
			dict_predicateObject['prop'] = i[0].n3()
			# OBJECT = VALUE
			dict_predicateObject['value'] = i[1].n3()
			dict_new['tail'].append(dict_predicateObject)

		mergeDict.append(dict_new)

	for s in subjects2:
		dict_new = {}
		dict_new['head'] = {}
		dict_new['head']['index'] = index
		index += 1
		dict_new['head']['uri'] = s.n3()
		dict_new['head']['row'] = True
		dict_new['tail'] = []
		for i in g2.predicate_objects(subject=s):
			dict_predicateObject = {}
			# PREDICATE = PROP
			dict_predicateObject['prop'] = i[0].n3()
			# OBJECT = VALUE
			dict_predicateObject['value'] = i[1].n3()
			dict_new['tail'].append(dict_predicateObject)

		mergeDict2.append(dict_new)

	url = "http://localhost:9000/similarity/initialize?model_1="+file_ontologies
	headers = {'content-type': "application/json"}
	response = requests.get(url, headers=headers)\

	perfectOp = MFuhsionPerfect(threshold, simfunction)

	perfectOp.execute_new(mergeDict, mergeDict2)
	toJoin = []
	for tpl in perfectOp.toBeJoined:
		tupl = {}
		tupl['uri1'] = str(tpl[0])
		tupl['uri2'] = str(tpl[1])
		toJoin.append(tupl)

	for elem in toJoin:
		elem['uri1'] = elem['uri1'].replace('<','').replace('>','')
		elem['uri2'] = elem['uri2'].replace('<','').replace('>','')

	jsonToJoin = {}
	jsonToJoin["tasks"] = toJoin

	url = "http://localhost:9001/setlocation"
	headers = {'content-type': "application/json"}
	data = {"location1":file_name1, 
		"location2":file_name2}
	data = json.dumps(data)
	response = requests.post(url, data=data, headers=headers)
	print response

	url = "http://localhost:9001/fusion/"+fusion_policy
	data = jsonToJoin
	data = json.dumps(data)
	response = requests.post(url, data=data, headers=headers)
	resp_object = response.text
	F.write(resp_object)
	F.close()


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