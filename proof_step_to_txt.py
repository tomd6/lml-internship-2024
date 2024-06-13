import ddar
import graph as gh
import problem as pr

defs = pr.Definition.from_txt_file('defs.txt', to_dict=True)
rules = pr.Theorem.from_txt_file('rules.txt', to_dict=True)


#ddar.solve(g, rules, p, max_level=1000)
#goal_args = g.names2nodes(p.goal.args)
#for node in g.all_nodes():
#    print(node.to_txt())
'''
Convert a list of properties into a sting

'''
def prop_list_to_string(string,list):
    for a in list:
        string += '\n' + a.name
        for arg in a.args:
            string += ' ' + arg.name
    return string

'''
Take a textual alphageometry problem, run the solver on it and convert the restults into one string
'''
def proof_steps_to_string(txt,bool):
    p = pr.Problem.from_txt(txt)
    g, _ = gh.Graph.build_problem(p, defs)
    ddar.solve(g, rules, p, max_level=1000)
    setup, aux, log, refs = ddar.get_proof_steps(g, p.goal, bool)
    final_string = "==== SETUP ====\n" + txt + "\n==== AUX ===="
    print(aux)
    final_string = prop_list_to_string(final_string,aux[0][0])
    final_string += "\n==== LOG ===="
    for l in log:
        final_string = prop_list_to_string(final_string,l[0])
        final_string += '\n-----------'
    final_string += "\n==== REFS ====\n"
    for r in refs:
        final_string += ' '.join(r) + '\n'
    return final_string
txt = 'a b c = triangle a b c; d = on_tline d b a c, on_tline d c a b; e = on_line e a c, on_line e b d ? perp a d b c'  # pylint: disable=line-too-long
#string_test = proof_steps_to_string(txt,True)
#print(string_test)

    
    
