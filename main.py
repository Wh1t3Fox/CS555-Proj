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

g1 = Graph(directed=False)
g2 = Graph(directed=False)

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

#Create a graph from a matrix file
def create_graph(filename, graph):
    #open the file to read
    with open(filename, 'r') as fr:
        #See how many nodes we need
        size =  len(fr.readline().split())
        #generate the nodes
        graph.add_vertex(size)
        #Seek back to beginning of the file
        fr.seek(0)
        #iterate each row with the line number
        for line,row in enumerate(fr):
            #Turn the row into a list/array
               row = row.split()
               #Iterate over each col in the row
               for pos,item  in enumerate(row):
                  #Create an edge if the item is 1 and don't add reverse edge
                   if item == str(1) and not graph.edge(pos, line):
                       graph.add_edge(line, pos)

#Create an image of a graph
def draw_graph(graph):
    graph_draw(graph, vertex_text=graph.vertex_index, vertex_font_size=18,\
            output_size=(500, 500), output="nodes.png")

if __name__ == '__main__':
    create_graph('g1.txt', g1)
    draw_graph(g1)
