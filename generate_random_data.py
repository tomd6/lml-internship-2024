
import random
import string  

example = 'a b c = triangle a b c; h = orthocenter a b c; h1 = foot a b c; h2 = foot b c a; h3 = foot c a b; g1 g2 g3 g = centroid g1 g2 g3 g a b c; o = circle b a c'
ex_2 = "a b c = triangle; h = on_tline b a c, on_tline c a b"
ex_3 = "a b c = triangle; d = on_tline d b a c, on_tline d c a b; e = on_line e a c, on_line e b d"
ex_4 = "a b c = triangle a b c; d1 d2 d3 d = incenter2 a b c; e1 e2 e3 e = excenter2 a b c"

'''
Generate a random geometric formula whith the maximum complexity passed in parameters
complexity : the maximum complexity of a given figure, which means it cannot have more than complexity shapes in it.
Returns a string of the form 'a b c = triangle a b c; d = foot a b c;' or similar
'''
def generate_two(complexity):
    points_list =  list(string.ascii_lowercase)   #List of the possible point names in the figure
    points_list.reverse()
    og_list = points_list.copy()
    points = [points_list.pop() for x in range(3)]
    comp = 0
    base = "{0} {1} {2} = triangle {0} {1} {2}; ".format(points[0],points[1],points[2])
    base = points[0] + ' ' + points[1] + ' ' + points[2] + ' = triangle ' + points[0] + ' ' + points[1] + ' ' + points[2] + '; ' #base of the figure
    type_list = [['eqdistance',1],['orthocenter',1],['circle',1],['excenter',1],['incenter',1],['centroid',2],['foot',3],['on_tline',3],['on_line',4],
                     ['on_bline',5],['on_circle',5],['mirror',5]] #List of all different types of shapes and their structure number.
    random.shuffle(type_list)
    while(len(type_list) > 0 and comp <= complexity): #While the list isn't empty and we didn't reach the maximum comp
        comp += 1
        type, func = type_list.pop()
        if(func == 1): #Select which function apply based on the structure of the shape. Each different structure is linked to a number.
            base, points_list = add_type_one(base,points_list, points, type)
        elif(func == 2):
            base, points_list = add_type_two(base,points_list, points, type)
        elif(func == 3):
            base, points_list = add_type_three(base,points_list, points, type)
        elif(func == 4):
            base, points_list = add_type_four(base,points_list, points, type)
        elif(func == 5):
            base, points_list = add_type_five(base,points_list, points, type)
    f_list = list(set(og_list).difference(points_list))
    return base[:-2],f_list


'''
Add a shape to the figure with the given base figure, points and text. the shape has the given structure : 
'x = name a b c'
'''
def add_type_one(base, points_list, points,text):
    if(random.randint(0,1) < 1):
        base+= "{0} = {1} {2} {3} {4}; ".format(points_list.pop(), text, points[0], points[1], points[2])
    return base,points_list

'''
Add a shape to the figure with the given base figure, points and text. the shape has the given structure : 
'w x y z = name a b c'
'''
def add_type_two(base,points_list,points, text):
    if(random.randint(0,1) < 1):
        base+= "{0} {1} {2} {3} = {4} {5} {6} {7}; ".format(points_list.pop(), points_list.pop(), points_list.pop(), 
                                               points_list.pop(), text, points[0], points[1], points[2])
    return base, points_list

'''
Add x random shapes to the figure with the given base figure, points and text. the shapes have the given structure : 
'x = name a b c'
'''
def add_type_three(base, points_list, points, text):
    if(random.randint(0,1) < 1):
        nb = random.randint(1,3)
        for x in range(nb):
            base+= "{0} = {1} {2} {3} {4}; ".format(points_list.pop(), text, points[(0+x)%3], points[(1+x)%3], points[(2+x)%3])
    return base, points_list


'''
Add x random shapes to the figure with the given base figure, points and text. the shapes have the given structure : 
'x = name a b'
'''
def add_type_four(base, points_list, points, text):
    if(random.randint(0,1) < 1):
        nb = random.randint(1,3) #We generate between 1 and 3 of these figures
        list_current = []
        for x in range(nb):
            list_current.append(frozenset(random.sample(points,2))) #take a random combination of 2 points
        list_current = set(list_current)
        for lists in list_current:
            base+= "{0} = {1} {2} {3}; ".format(points_list.pop(),text,list(lists)[0],list(lists)[1]) 
    return base, points_list

'''
Add a shape to the figure with the given base figure, points and text. the shape has the given structure : 
'x = name a b'
'''
def add_type_five(base, points_list, points,text):
    if(random.randint(0,1) < 1):
        base+= "{0} = {1} {2} {3}; ".format(points_list.pop(),text,points[0],points[1])
    return base,points_list


def generate_with_end(complexity):
    type_list = ['coll']
    random.shuffle(type_list)
    base, point_list = generate_two(complexity)
    #base += ' ? ' + type_list.pop() + ' ' + point_list.pop() + ' ' + point_list.pop()  + ' ' + point_list.pop()
    base += ' ? coll a b c'
    print(base)
    return base