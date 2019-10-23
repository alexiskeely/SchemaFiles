# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:49:42 2019

@author: alexi
"""
#%%

from rdflib import Graph, Namespace, XSD, RDF
import rdflib
from owlready2 import *

#%%
def fetch_uri(uri: str) -> Optional[str]:
    print(f"Fetching: {uri}...", end="")
    req = requests.get(uri)
    if not req.ok:
        print(req.text)
        return None
    print("Done")
    return req.text


#%%
    

agents = "https://www.lib.washington.edu/static/public/cams/data/datasets/uwSemWebParts/agent-1-0-2.ttl"
places = 'https://raw.githubusercontent.com/russianArchitecture-uwLibraries/brumfield/master/uwDataset/places.ttl'
subjects = 'https://raw.githubusercontent.com/russianArchitecture-uwLibraries/brumfield/master/uwDataset/subjects.ttl'
works = 'https://raw.githubusercontent.com/russianArchitecture-uwLibraries/brumfield/master/uwDataset/works.ttl'
worktypes = 'https://raw.githubusercontent.com/russianArchitecture-uwLibraries/brumfield/master/uwDataset/worktypes.ttl'


#%%
g = rdflib.Graph()
g.load(places, format='turtle')
prop_list = []

for prop in g.predicates(subject=None, object=None):
    prop_list.append(prop)
prop_list = sorted(list(set(prop_list)))

class_list = []
for s,p,o in g.triples( (None,  RDF.type, None) ):
   class_list.append(o)
class_list = sorted(list(set(class_list)))



#%%
for x in prop_list:
    print(x)
print('...')
for x in class_list:
    print(x)
    
#%%
vra_onto = get_ontology('https://raw.githubusercontent.com/escowles/VRA-RDF-Project/owl/VRA_Ontology.owl')
vra_onto.load()

#%%



