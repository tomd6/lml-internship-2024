import graph as gh
import numericals as nm
import problem as pr
from pathlib import Path
import matplotlib.pyplot as plt
import generate_random_data
import os
import time
import json
import proof_step_to_txt
defs = pr.Definition.from_txt_file('defs.txt', to_dict=True)
rules = pr.Theorem.from_txt_file('rules.txt', to_dict=True)


"""
Build a graph from the given textual problem and returns it
"""
def build_graph_points(txt):
    p = pr.Problem.from_txt(txt, translate=True)
    g, _ = gh.Graph.build_problem(p, defs)
    return g

"""
Draw and save the given graph
"""
def save_graph(path, graph):
    gh.nm.draw(
    graph.type2nodes[gh.Point],
    graph.type2nodes[gh.Line],
    graph.type2nodes[gh.Circle],
    graph.type2nodes[gh.Segment],save_to=path)
    plt.close()

"""
 Build a graph and then save its picture representation
"""
def build_and_save_graph(txt,path):
    graph = build_graph_points(txt)
    save_graph(path,graph)

"""
Build and sav the same graph multiple times
"""
def build_multiple_times(txt, folder,name,len,comp):
    for x in range(len):
        build_and_save_graph(txt,folder+'/'+str(name) + "_" + str(x)+'_'+str(comp)+'.png')

"""
Generat nb_create random graphs with a comp max complexity.. Save them nb_it times.
The textuel data is stored in order to generate a fitting dataset for a LLaVA model.
"""
def generate_multiplie_random(folder,nb_create,nb_it,comp):
    data = []
    os.makedirs(folder, exist_ok=True)
    output_file = os.path.join(folder, 'data.txt')
    for x in range(nb_create):
        text,li = generate_random_data.generate_two(comp)
        build_multiple_times(text,folder,x,nb_it,comp)
        for i in range(nb_it):
            json_data = {
                        "id": str(x) +'_' + str(i)+'_'+str(comp),
                        "image": str(x) +'_' + str(i)+'_'+str(comp)+".png",
                        "conversations": [
                            {
                                "from": "human",
                                "value": "<image>give the formula of this geometric figure\n"
                            },
                            {
                            "from": "gpt",
                                "value": text
                            }
                        ]
                    }
            data.append(json_data)
    
        json_output_path = os.path.join(folder, 'dataset.json')
    with open(json_output_path, 'a') as json_file:
        json.dump(data, json_file, indent=4)


txt = 'a b c = triangle a b c; h = orthocenter a b c; h1 = foot a b c; h2 = foot b c a; h3 = foot c a b; g1 g2 g3 g = centroid g1 g2 g3 g a b c; o = circle a b c ? coll h g o'  # pylint: disable=line-too-long


generate_multiplie_random('test_figs',10,10,7)
#generate_multiplie_random('test_figs',10,10,4)
