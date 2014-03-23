#!/usr/bin/env python

from graph_tool.all import *


def create_graph():
    with open('matrix.txt', 'r') as fr:
        size =  len(fr.readline().split())
        g.add_vertex(size)
        fr.seek(0)
        for line,row in enumerate(fr):
               row = row.split()
               for pos,item  in enumerate(row):
                   if item == str(1):
                       g.add_edge(line, pos)



if __name__ == '__main__':
    g = Graph(directed=False)
    create_graph()
    graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18, output_size=(500, 500), output="nodes.png")
