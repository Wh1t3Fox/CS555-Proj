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

g = Graph(directed=False)


def create_graph(filename):
    #open the file to read
    with open(filename, 'r') as fr:
        #See how many nodes we need
        size =  len(fr.readline().split())
        #generate the nodes
        g.add_vertex(size)
        #Seek back to beginning of the file
        fr.seek(0)
        #iterate each row with the line number
        for line,row in enumerate(fr):
            #Turn the row into a list/array
               row = row.split()
               #Iterate over each col in the row
               for pos,item  in enumerate(row):
                  #Create an edge if the item is 1 and don't add reverse edge
                   if item == str(1) and not g.edge(pos, line):
                       g.add_edge(line, pos)



if __name__ == '__main__':
    create_graph('g1.txt')
    graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(500, 500), output="nodes.png")
