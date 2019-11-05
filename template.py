# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:12:38 2019

@author: alexis
"""
#!/usr/bin/env python
#%%
from rdflib import Graph, Namespace, XSD, RDF, URIRef
from typing import Optional
import requests
import rdflib
import sys




input_URI = str(sys.argv[1:])
print(input_URI)
#downloads data
def fetch_uri(uri: str) -> Optional[str]:
    print(f"\n...Downloading graph from: {uri}...", end="")
    req = requests.get(uri)
    if not req.ok:
        print(req.text)
        return None
    print("Done")
    return req.text


input_URI = input('\nInput the URL for the turtle file: ' )
turtle = fetch_uri(str(input_URI))


## generates a list of unique properties and classes in the datafile
g = rdflib.Graph()
g.load(input_URI, format='turtle')
prop_list = []

for prop in g.predicates(subject=None, object=None):
    prop_list.append(prop)
prop_list = sorted(list(set(prop_list)))
prop
class_list = []
for s,p,o in g.triples( (None,  RDF.type, None) ):
   class_list.append(o)
class_list = sorted(list(set(class_list)))

## pulls out prefixes to be bound with the shape graph below   
prefixes = [line for line in turtle.split('\n') if "@prefix" in line]

pre_binds = []
## processsing to pull out namespaces and URIs
for x in prefixes:
    x = x.replace('@prefix', '')
    x = x.replace('>', "")
    x = x.replace('<', "")
    x = x.replace(': ', " ")
    x = x.split(' .')
    x = x[0].split(" ")
    pre_binds.append(x)

## formats the above to be sent to bind method
args = []
for x in pre_binds:
    args.append((x[1], x[-1]))
    

## Creates template shapes that are either NodeShapes or PropertyShapes. 
## Classes and properties are handled differently depending on whether they are # or / 
triples = ""
print(f'\nGenerated: {len(class_list)} node shapes and {len(prop_list)} property shapes')
## node shapes
for x in class_list:
    if '#' in x:
        triples = triples + (f"""
<http://example.org/{x.split("#")[-1]}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
<http://example.org/{x.split("#")[-1]}Shape> <http://www.w3.org/ns/shacl#targetClass> <{x}> .

""")
    else:
        triples = triples + (f"""
<http://example.org/{x.split("/")[-1]}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
<http://example.org/{x.split("/")[-1]}Shape> <http://www.w3.org/ns/shacl#targetClass> <{x}> .

""")

## property shapes
for x in prop_list:
    if '#' in x:
        triples = triples +(f"""
<http://example.org/{x.split("#")[-1]}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#PropertyShape> .
<http://example.org/{x.split("#")[-1]}Shape> <http://www.w3.org/ns/shacl#path> <{x}> .

""")
    else:
        triples = triples +(f"""
<http://example.org/{x.split("/")[-1]}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#PropertyShape> .
<http://example.org/{x.split("/")[-1]}Shape> <http://www.w3.org/ns/shacl#path> <{x}> .

""")

## Create shapes graph
g = rdflib.Graph()

## bind namespaces to graph, adding in example for default shape namespaces and shacl for shacl props/classes.
for key, uri in args:
    g.bind(key, URIRef(uri))
g.bind('ex', URIRef('http://example.org/'))
g.bind('sh', URIRef('http://www.w3.org/ns/shacl#'))

g.parse(data= triples, format='nt')
shapes = g.serialize(format='turtle')
shapes = shapes.decode("utf-8") 
filename = input('\nFilename for template? (Will save as ttl file) ')

with open(filename+'.ttl','w') as f:
    f.write(shapes)
print(f'\nSaved {filename}.ttl')
