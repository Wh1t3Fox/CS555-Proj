#!/usr/bin/env python

from graph_tool.all import *
from matrix import Matrix
from random import randint

g1 = Graph()
g2 = Graph()

#Create a permutation matrix file
def create_permutation(filename, size):
    s = set()
    tmp = []
    while len(set(tmp)) != size:
        tmp.append(randint(0, size-1))
    order = [x for x in tmp if x not in s and not s.add(x)]
    with open(filename, 'w') as fw:
        for  i in range(size):
            for j in range(size):
                if order[i] == j:
                    fw.write('1 ')
                else:
                    fw.write('0 ')
            fw.write('\n')

#Create a matrix file from a graph
def create_matrix(filename, graph):
    with open(filename, 'w') as fw:
        for i in range(graph.num_vertices()):
            for j in range(graph.num_vertices()):
                if graph.edge(i, j):
                    fw.write('1 ')
                else:
                    fw.write('0 ')
            fw.write('\n')

#Create a graph from a matrix
def create_graph(matrix, graph):
    graph.add_vertex(len(matrix))
    for line, row in enumerate(matrix):
        for pos, item in enumerate(row):
            if item == str(1) and not graph.edge(pos, line):
                graph.add_edge(line, pos)

#Create an image of a graph
def draw_graph(filename, graph):
    graph_draw(graph, vertex_text=graph.vertex_index, vertex_font_size=18,\
            output_size=(500, 500), output=filename)

if __name__ == '__main__':
    g1_matrix = Matrix('g1.txt')
    g2_matrix = Matrix('g2.txt')
    create_graph(g1_matrix, g1)
    create_graph(g2_matrix, g2)
    
    q = Graph(g2)
    random_rewire(q, model='uncorrelated')
    
    ####Testing to prove the graphs will work for the proj#####    
    vm, em = subgraph_isomorphism(g1, q)
    print len(vm)
    for i in range(len(vm)):
        q.set_vertex_filter(None)
        q.set_edge_filter(None)
        vmask, emask = mark_subgraph(q, g1, vm[i], em[i]) 
        q.set_vertex_filter(vmask)
        q.set_edge_filter(emask)
        assert(isomorphism(q,g1))
    ewidth = q.copy_property(emask, value_type="double")
    ewidth.a += 0.5
    ewidth.a *= 2 
    graph_draw(q, vertex_fill_color=vmask, edge_color=emask, edge_pen_width=ewidth, output_size=(500,500), output = "g2_sub.png")
    ####END######
    
    
    
    
    draw_graph('g1.png', g1)
    draw_graph('g2.png', g2)
    draw_graph('q.png', q)
