#!/usr/bin/env python
'''
CS555 Project
Zero-Knowledge Subgraph Isomorphism
Members:
    Craig West
    Max DeWees
    David Hersh
    Michael Kouremetis
'''
from graph_tool.all import *
from matrix import Matrix

g1 = Graph(directed=False)
g2 = Graph(directed=False)
q = Graph(directed=False)
q_sub = Graph(directed=False)

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
    
    q_matrix = Matrix('g2.txt')
    create_graph(q_matrix, q)
    random_rewire(q, model='uncorrelated')
    
    
    draw_graph('g1.png', g1)
    draw_graph('g2.png', g2)
    draw_graph('q.png', q)
