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
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#nodeKind> <http://www.w3.org/ns/shacl#BlankNodeOrIRI> .
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
print(tripe)
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
         
         
#%%
from rdflib import Graph, RDF, RDFS, OWL, Namespace
from rdflib.util import guess_format
from rdflib.namespace import SKOS, DC, DCTERMS, FOAF, DOAP, Namespace, XSD
from rdflib.term import URIRef, Literal, BNode
import collections

class schema():
    def __init__(self, graph=None,):
        self.G = Graph()
        self.G.load(graph,format=guess_format(graph))
        self.CLASSES = collections.OrderedDict()
        self.PROPS = collections.OrderedDict()    
        self.REST = collections.OrderedDict()    
        self.datatypes = [XSD.string, XSD.boolean, XSD.time, XSD.date, XSD.dateTime, XSD.integer, XSD.decimal, 
                          XSD.nonNegativeInteger, XSD.negativeInteger, RDFS.Literal, XSD.positiveInteger, XSD.nonPositiveInteger]
            
   
    def extract_props(self):    
        properties = []
        
        #gather properties
        for s,p,o in self.G.triples((None,RDF.type,OWL.DatatypeProperty)):
            properties.append(s)
        
        for s,p,o in self.G.triples((None,RDF.type,OWL.ObjectProperty)):
            properties.append(s)
        for s,p,o in self.G.triples((None,RDF.type,OWL.AnnotationProperty)):
            properties.append(s)
        for s,p,o in self.G.triples((None,RDF.type,OWL.TransitiveProperty)):
            properties.append(s)
       
        for s,p,o in self.G.triples((None,RDF.type,RDF.Property)):
            properties.append(s)
        
        for p in sorted(properties):
            self.PROPS[p] = {}
       
        
        #gather property values
        for prop in self.PROPS.keys():
            s = URIRef(prop)           
            self.PROPS[prop]['domain']= None
            self.PROPS[prop]['range']= None
            self.PROPS[prop]['e_prop'] = None

            for o in self.G.objects(subject=s, predicate=RDFS.domain):
                if type(o) != BNode:
                    self.PROPS[prop]['domain'] = o
               
            for o in self.G.objects(subject=s, predicate=RDFS.range):
                if type(o) != BNode:
                    self.PROPS[prop]['range'] = o

            for o in self.G.objects(subject=s, predicate=OWL.equivalentProperty):
                self.PROPS[prop]['e_prop'] = o
            
            for o in self.G.objects(subject=s, predicate=RDFS.label):
                self.PROPS[prop]['label'] = o
            
    
    
    
    def extract_classes(self):    
        classes = []
        for s,p,o in self.G.triples((None,RDF.type,OWL.Class)):
            if type(s) != BNode:
                classes.append(s)
            else:
                pass
        for s,p,o in self.G.triples((None,RDF.type,RDFS.Class)):
            if type(s) != BNode:

                classes.append(s)
            else:
                pass
            
        for c in sorted(classes):
            self.CLASSES[c] = {}
            for c in self.CLASSES.keys():
                self.CLASSES[c]['label'] = self.gen_shape_labels(c)
            
    def extract_restrictions(self):
        # does not handle nested restrictions within other class descriptions
        
        restrictions = []
        for s,p,o in self.G.triples((None, OWL.onProperty, None)):
            restriction = s
            for s in self.G.subjects(object=restriction, predicate=None):
                if type(s) != BNode:
                    for o in self.G.objects(subject=restriction, predicate=OWL.onProperty): 
                        if type(o) != BNode:    
                            restrictions.append(restriction)
        for r in sorted(restrictions):
            self.REST[r] = {}
        
        for rest in self.REST.keys():  
            for o in self.G.objects(subject=rest, predicate=OWL.onProperty):
                self.REST[rest]['onProp']= o
           
            for s in self.G.subjects(object=rest, predicate=None):
                self.REST[rest]['onClass']= s
                
            rest_type = []
            rest_val =[]
            for s,p,o in self.G.triples((rest,OWL.maxCardinality,None)):
                rest_type.append(p)
                rest_val.append(o)
            for p in self.G.triples((rest,OWL.minCardinality, None)):
                rest_type.append(p)
                rest_val.append(o)
            for s,p,o in self.G.triples((rest, OWL.cardinality, None)):
                rest_type.append(p)
                rest_val.append(o)        
            for s,p,o in self.G.triples((rest,OWL.allValuesFrom,None)):
                rest_type.append(p)
                rest_val.append(o)
            for s,p,o in self.G.triples((rest,OWL.someValuesFrom, None)):
                rest_type.append(p)
                rest_val.append(o)            
            for s,p,o in self.G.triples((rest,OWL.hasValue, None)):
                rest_type.append(p)
                rest_val.append(o)                
            self.REST[rest]['type'] = rest_type[0]
            self.REST[rest]['value'] = rest_val[0]
                
                
            
    def gen_shape_labels(self, URI):
        if '#' in URI:
            label = URI.split("#")[-1]
        else:
            label = URI.split("/")[-1]
        return label
            
    def gen_graph(self):
        self.extract_props()
        self.extract_classes()
        self.extract_restrictions()
        ng = Graph()
        SH = Namespace('http://www.w3.org/ns/shacl#')
        ng.bind('SH', SH) 
        
        EX = Namespace('http://www.example.org/')
        ng.bind('EX', EX)
        
        # add class Node Shapes
        for c in self.CLASSES.keys():
            label = self.gen_shape_labels(c)+'_ClassShape'
            ng.add((EX[label], RDF.type, SH.NodeShape))
            ng.add((EX[label], SH.targetClass, c))
        for p in self.PROPS.keys():
            if self.PROPS[p]['domain'] is not None:
                blank = BNode()
                if self.PROPS[p]['domain'] in self.CLASSES.keys():
                    label = self.gen_shape_labels(self.PROPS[p]['domain'])+'_ClassShape'
                    ng.add((EX[label], SH.property, blank))
                    ng.add((blank, SH.path, p))
                    if self.PROPS[p]['range'] is not None:
                        rang = self.PROPS[p]['range']
                        if rang in self.datatypes:
                            ng.add((blank, SH.datatype, rang))
                        else:
                            ng.add((blank, SH['class'], rang ))
                    for r in self.REST.keys():
                        if self.REST[r]['onProp'] == p and self.REST[r]['onClass'] == self.PROPS[p]['domain']:
                            if self.REST[r]['type'] in (OWL.cardinality):
                                ng.add((blank, SH.minCount, Literal(self.REST[r]['value'], datatype=XSD.integer)))
                                ng.add((blank, SH.maxCount, Literal(self.REST[r]['value'], datatype=XSD.integer)))
                            elif self.REST[r]['type'] in (OWL.minCardinality):
                                ng.add((blank, SH.minCount, Literal(self.REST[r]['value'], datatype=XSD.integer)))
                            elif self.REST[r]['type'] in (OWL.maxCardinality):
                                ng.add((blank, SH.maxCount, Literal(self.REST[r]['value'], datatype=XSD.integer)))
                            else:
                                pass
                        else:
                            pass
                else:
                    label = self.gen_shape_labels(self.PROPS[p])+'_PropShape'
                    ng.add((EX[label], RDF.type, SH.NodeShape))
                    ng.add((EX[label], SH.targetSubjectsOf, p))
                    ng.add((EX[label], SH.nodeKind, SH.BlankNodeOrIRI))
                    ng.add((EX[label], SH.property, blank))
                    ng.add((blank, SH.path, p))
                    if self.PROPS[p]['range'] is not None:
                            rang = self.PROPS[p]['range']
                            if rang in self.datatypes:
                                ng.add((blank, SH.datatype, rang))
                            else:
                                ng.add((blank, SH['class'], rang ))
            else:
                blank = BNode()
                label = self.gen_shape_labels(p)+'_PropShape'
                ng.add((EX[label], RDF.type, SH.NodeShape))
                ng.add((EX[label], SH.targetSubjectsOf, p))
                ng.add((EX[label], SH.nodeKind, SH.BlankNodeOrIRI))
                ng.add((EX[label], SH.property, blank))
                ng.add((blank, SH.path, p))
                if self.PROPS[p]['range'] is not None:
                        rang = self.PROPS[p]['range']
                        if rang in self.datatypes:
                            ng.add((blank, SH.datatype, rang))
                        else:
                            ng.add((blank, SH['class'], rang ))
        
        print(ng.serialize(format='turtle').decode())        
        return ng        



    def save(self, path):
        ng = self.gen_graph()
        ng.serialize(path, format='turtle')    

#        ng.serialize(path, format='turtle')
#%%
vgms = schema('VGMS.ttl')
vgms.gen_graph()                
                #%%
              <http://example.org/{pname}Shape> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/shacl#NodeShape> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#nodeKind> <http://www.w3.org/ns/shacl#BlankNodeOrIRI> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#targetSubjectsOf> <{prop['URI']}> .
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#name> "{prop['label']} property shape" . 
        <http://example.org/{pname}Shape> <http://www.w3.org/ns/shacl#property> _:{counter} .
_:{counter} <http://www.w3.org/ns/shacl#path> <{prop['URI']}> . 
_:{counter} <http://www.w3.org/ns/shacl#name> "{prop['label']} property shape" .                      
        print(ng.serialize(format='turtle').decode())             
                



#%%
edm = schema('https://raw.githubusercontent.com/europeana/corelib/master/corelib-edm-definitions/src/main/resources/eu/rdf/edm.ttl')
bf = schema('http://id.loc.gov/ontologies/bibframe.nt')
bf.gen_graph()
#%%
#%%
bf.save_graph('bf_shapes.ttl')
#%%

for x inr estirctions:
    clas
    prop
    resttriction if clause for cardinality v value
        if cardinality:
            minCount = value
            MaxCount = value
        if minCadinality :
            minCount = value
            
        if maxCardinality:
            maxCount = value
    
    if 
    
    value
    
sh:or (sh:value)
        sh:value
        sh:value
        
        or 




