# RDF INTEGRATOR

## Dependencies

First you need to clone this repositories

```
https://github.com/RDF-Molecules/sim_service
https://github.com/RDF-Molecules/operators
https://github.com/RDF-Molecules/merge_service
```

Second you need to runing gades sim service and merge service using:

For gades
```
activator run
```

For merge service
```
sbt 'run 9001'
```

## Running the example

Set the RDF Graphs in dataExample folder and run the following command

```
python example.py
```
