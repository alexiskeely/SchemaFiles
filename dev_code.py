# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 11:23:56 2019

@author: alexi
"""

"""
shacl schema generator based on rdfs schemas

to do: better datatype handling for rdfs:range
- need to be able to handle 





"""
#%%
from rdflib import Graph, Namespace, XSD, RDF, URIRef
import rdflib
from collections import Counter

#%%
rdff = 'https://www.w3.org/1999/02/22-rdf-syntax-ns.ttl' 
dc = 'https://raw.githubusercontent.com/dcmi/vocabtool/master/build/dcterms.ttl'
mads = 'http://id.loc.gov/ontologies/madsrdf/v1.nt'
vra3 ='http://web.mit.edu/simile/2003/10/vraCore3'
g = rdflib.Graph()
g.load('http://id.loc.gov/ontologies/bibframe.nt', format='nt')

#%%
for s,p,o in g.triples((None, None, None)):
    print(s,p,o)
 #%%   
prop_list = []
for s,p,o in g.triples( (None,  RDF.type, rdflib.term.URIRef('http://www.w3.org/2002/07/owl#ObjectProperty')) ):
   prop_list.append(s)
for s,p,o in g.triples( (None,  RDF.type, rdflib.term.URIRef('http://www.w3.org/2002/07/owl#DatatypeProperty')) ):
   prop_list.append(s)
for s,p,o in g.triples( (None,  RDF.type, rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')) ):
   prop_list.append(s)
for s,p,o in g.triples( (None,  RDF.type, rdflib.term.URIRef('http://www.w3.org/2002/07/owl#AnnotationProperty')) ):
   prop_list.append(s)
prop_list = sorted(list(set(prop_list)))
#    
tupes = []
for k in prop_list:
    dummy ={'URI':None, 'label':None, 'domain':None, 'range':None, 'comment':None, 'subProp':None}
    dummy['URI'] = k
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label'), None)):       
        dummy['label'] = o
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#domain'), None)):       
        dummy['domain'] = o
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#range'), None)):       
        dummy['range'] = o
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#subPropertyOf'), None)):       
        dummy['subProp'] = o
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#comment'), None)):       
        dummy['comment'] = o
    for s,p,o in g.triples((k, rdflib.term.URIRef('http://www.w3.org/2002/07/owl#TransitiveProperty'), None)):       
        dummy['comment'] = o
    tupes.append(dummy)
    
    
class_list = []
for s,p,o in g.triples( (None,  RDF.type, rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#Class')) ):
   for s,e,r in g.triples((s,rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#label'), None)):
        class_list.append((s,r))
   
for x in class_list:
    print(x)
    
#%%
def generate_triples(classes, props):
    triples = ''
    counter = 0
    for statement in classes:
        if '#' in statement[0]:
            name =  statement[0].split("#")[-1]
        else:
            name =  statement[0].split("/")[-1]
            #gen node shape
        triples = triples + (f"""
<http://example.org/{name}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
        <http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#nodeKind> <http://www.w3.org/ns/shacl#BlankNodeOrIRI> .
<http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#targetClass> <{statement[0]}> .
<http://example.org/{name}Shape> <http://www.w3.org/ns/shacl#name> "{statement[1]} shape" .""") 
    for prop in props:
        counter = counter + 1
        if prop['domain'] is not None:
            if '#' in prop['domain']:
                dname =  prop['domain'].split("#")[-1]
            else:
                dname =  prop['domain'].split("/")[-1]
           
            triples = triples + (f"""
<http://example.org/{dname}Shape> <http://www.w3.org/ns/shacl#property> _:{counter} .
_:{counter} <http://www.w3.org/ns/shacl#path> <{prop['URI']}> . 
_:{counter} <http://www.w3.org/ns/shacl#name> "{prop['label']} property shape" . """)     
            if prop['range'] is not None:
                triples = triples + (f"""
                _:{counter} <http://www.w3.org/ns/shacl#class> <{prop['range']}> .""")
        else:
            if '#' in prop['URI']:
                pname =  prop['URI'].split("#")[-1]
            else:
                pname =  prop['URI'].split("/")[-1]
            triples = triples + (f"""
        <http://example.org/{pname}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#nodeKinf> <http://www.w3.org/ns/shacl#BlankNodeOrIRI> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#targetSubjectsOf> <{prop['URI']}> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#name> "{prop['label']} property shape" . 
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#property> _:{counter} .
_:{counter} <http://www.w3.org/ns/shacl#path> <{prop['URI']}> . 
_:{counter} <http://www.w3.org/ns/shacl#name> "{prop['label']} property shape" . """)   
            if prop['range'] is not None:
                 triples = triples + (f"""
                _:{counter} <http://www.w3.org/ns/shacl#class> <{prop['range']}> .""")
                
            
            


    return triples

tripe = generate_triples(class_list, tupes)

#%%
def generate_shacl(triples):
    g = rdflib.Graph()
    
    ### bind namespaces to graph, adding in example for default shape namespaces and shacl for shacl props/classes.
    #for key, uri in args:
    #    g.bind(key, URIRef(uri))
    g.bind('ex', URIRef('http://example.org/'))
    g.bind('sh', URIRef('http://www.w3.org/ns/shacl#'))
    
    g.parse(data= triples, format='nt')
    shapes = g.serialize(format='turtle')
    shapes = shapes.decode("utf-8") 
    return shapes
    
sample = generate_shacl(tripe)
print(sample)
#%%
with open("bf_onto.ttl", "w") as text_file:
    text_file.write(sample)

#%%
ex:UserShape a sh:NodeShape;
 sh:targetSubjectsOf ex:teaches ;
 sh:property [
    sh:path ex:teaches ;
    sh:minCount 1;
    sh:maxCount 1;
    sh:nodeKind sh:IRI ;
 ] .    




ignore traversing property parent paths for the time being - those should be explicitly stated in a vocabulary 
##%%
#
#for x in tupes:
#    if x['subProp'] is not None and x['domain'] is None:
#        missing = True
#        while missing is True:
#                for y[] in tupes:
#                    if [y['domain'] for y[x['subProp']] in tupes] is not None:
#                        x['domain'] = y['domain']
#                        print(x['label'], x['domain'])
#                        missing = False
#                
##        print(x['label'],x['subProp'], x['domain'],x['range'])
#%%
for x in tupes:
    if x['range'] is not None:
        print(x)
#%%
http://id.loc.gov/ontologies/bibframe/videoCharacteristic
http://www.w3.org/2000/01/rdf-schema#domain http://id.loc.gov/ontologies/bibframe/Instance
http://www.w3.org/2000/01/rdf-schema#label Video characteristic
http://www.w3.org/1999/02/22-rdf-syntax-ns#type http://www.w3.org/2002/07/owl#ObjectProperty
http://www.w3.org/2000/01/rdf-schema#range http://id.loc.gov/ontologies/bibframe/VideoCharacteristic
http://www.w3.org/2004/02/skos/core#definition Technical specification relating to the encoding of video images in a resource
http://purl.org/dc/terms/modified 2016-04-21 (New)
#%%
class_set

labels - will need to get a set of potential label properties that people use in defining schema
definitions - same as above

(uri, label, definition)

property_set

(URI, domain, range, label, definition )

ex:name a sh:PropertyShape ;
    sh:path URI .
    sh:name "" ;
    sh:class range
    
        ex:ontologyIRIShape,
        ex:priorVersionShape,
        ex:versionIRIShape,
        ex:versionInfoShape ;
    sh:targetClass <http://www.w3.org/2002/07/owl#Ontology> .
    
    
#%%

to check for inheritance:
    - if prop is subprop and has no domain or range
    - navigate to parent prop definition and use parent domain / range
    - repeat until either domain or range has been added, or top property has been reached


    
for properties that have a domain:
    blank node construction
    
for properties without a domain:
    target subjects of shapenode construction
    
    
ex:UserShape a sh:NodeShape;
 sh:targetSubjectsOf ex:teaches ;
 sh:property [
    sh:path ex:teaches ;
    sh:minCount 1;
    sh:maxCount 1;
    sh:nodeKind sh:IRI ;
 ] .    
    