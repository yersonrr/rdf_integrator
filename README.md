# RDF INTEGRATOR

## Dependencies

First you need to clone this repositorie and run the following lines inside the folder

```
git clone https://github.com/RDF-Molecules/sim_service
git clone https://github.com/RDF-Molecules/merge_service
```

## For sim_service you need to install

* JDK 1.8
* Play Web Framework 2.5.12 "Streamy" and Activator 1.3.12

### For Activator 1.3.12 run the following lines

### Install Scala
```
sudo apt-get remove scala-library scala
wget http://www.scala-lang.org/files/archive/scala-2.11.6.deb
sudo dpkg -i scala-2.11.6.deb
sudo apt-get update
sudo apt-get install scala
```

### Download and Install Play (the folder should have permission to write)

```
cd /opt
wget http://downloads.typesafe.com/typesafe-activator/1.3.2/typesafe-activator-1.3.2-minimal.zip
unzip typesafe-activator-1.3.2-minimal.zip
mv activator-1.3.2-minimal activator
```

### Add the activator script to your PATH and execute Activator

```
cd /opt/activator
export PATH=$PATH:/opt/activator
source ~/.bashrc
chmod a+x activator
./activator
```

Depending on your operating system or linux distribution, you may need to adapt the command above. 
For example, on Linux Mint 18.x, the path environment variable is configured in /etc/environment. 
Hence, you can append ```:/opt/activator``` within ```PATH=""``` line.

### For merge_service you will need to run
```
echo "deb https://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823
sudo apt-get update
sudo apt-get install sbt 
```

Change the current directory to your cloned sim_service directory.

Second you need to run sim_service and merge_service using:

For sim_service
```
activator run
```

For merge service

Set the rdf path in **merge_service/conf/application.conf**

* fusion.model_1.location = "<path_to_folder>/rdf_integrator/dataExample/test1.nt"

* fusion.model_2.location = "<path_to_folder>/rdf_integrator/dataExample/test2.nt"

```
sbt 'run 9001'
```

Also the models can be set using a POST request e.g., http://localhost:9001/setlocation

A dicctionary of paths should be send in the POST body

```
{ 
  "location1": "/path/to/file.nt",
  "location2": "/path/to/file2.nt"
}
``` 

### Running the example

* Install the python requirements

```
pip3 install -r requirements.txt
```

* Set the RDF Graphs to merge, the ontologies and the path to save the result in **dataExample/config.ini** and run the following command in the same folder.

```
python3 integrator.py -c config.ini
```

The example write the result in the path specified in config.ini with the name "new_rdfGraph.nt".

The config.ini must have the following structure, and must be in the same directory as the integrator.py script:

```

[RDFData]
rdf1 = /Absolute/path/to/file.nt
rdf2 = /Absolute/path/to/file2.nt
ontology = /Absolute/path/to/file3.nt
pathToSave = /Path/to/save/the/output
number_classes = N

[Class1]
class = http://iasis/vocab/Publication
similarity_metric = gades
threshold = 0.8
fusion_policy = sameAs

[Class2]
class = http://iasis/vocab/LCannotationtation
similarity_metric = jaccard
threshold = 0.8
fusion_policy = union

...

[ClassN]
class = http://iasis/vocab/Test
similarity_metric = gades
threshold = 0.5
fusion_policy = sameAs

```

# RDF Interlinking

* Set the RDF Graph to interlink with the endpoints, the ontology and the path to save the result in **dataExample/config2.ini** and run the following command in the same folder.

```
python3 interlinking.py -c config2.ini
```

The example write the result in the path specified in config2.ini with the name "new_rdfGraph2.nt".

The config2.ini must have the following structure, and must be in the same directory as the interlinking.py script:

```

[RDFData]
rdf = /Absolute/path/to/file.nt-
ontology = /Absolute/path/to/file3.nt
pathToSave = /Path/to/save/the/output
number_kg = N

[KG1]
endpoint = https://dbpedia.org/sparql
similary_metric = part
threshold = 0.8
fusion_policy = https://www.w3.org/2000/01/rdf-schema#sameAs
class1 = http://project-iasis.eu/vocab/ADAnnotation
class2 = http://dbpedia.org/class/yago/BrainDisorder114085708
ontologyKG = /home/roa/internship/rdf_integrator/dataExample/dataSamples/dbpediaOntologies.nt
mapping = /home/roa/internship/rdf_integrator/dataExample/dataSamples/mappings.nt
predicate_to_compare = M

[KG1_P1]
predicate1 = http://project-iasis.eu/vocab/annLabel
predicate2 = http://www.w3.org/2000/01/rdf-schema#label

...

[KG1_PM]
predicate1 = http://project-iasis.eu/vocab/PREDICATE_EXAMPLE
predicate2 = http://www.w3.org/2000/01/rdf-schema#PREDICATE_EXAMPLE

...

[KGN]
endpoint = https://dbpedia.org/sparql
similary_metric = part
threshold = 0.8
fusion_policy = https://www.w3.org/2000/01/rdf-schema#sameAs
class1 = http://project-iasis.eu/vocab/ADAnnotation
class2 = http://dbpedia.org/class/yago/BrainDisorder114085708
ontologyKG = /home/roa/internship/rdf_integrator/dataExample/dataSamples/dbpediaOntologies.nt
mapping = /home/roa/internship/rdf_integrator/dataExample/dataSamples/mappings.nt
predicate_to_compare = 1

[KGN_P1]
predicate1 = http://project-iasis.eu/vocab/annLabel
predicate2 = http://www.w3.org/2000/01/rdf-schema#label

```
