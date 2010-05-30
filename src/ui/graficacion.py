# -*- coding: utf-8 -*-
'''
Created on 30/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

import os.path
import pydot
import tempfile
import wx

class GraficoDeRed(object):
    '''
    Genera un gráfico en graphviz usando pydot del grafo
    '''


    def __init__(self, red):
        '''
        Constructor
        '''
        self.temp = tempfile.mkdtemp()
        self.red = red
        
    def graficar_red(self):
        self.grafico = pydot.Dot('rdf', graph_type='digraph')
        self.grafico.set_fontname("Arial")
        self.grafico.set_rankdir("LR") # esto es para que vaya de izquierda a derecha!!!
        print "GRAFICAR..."
        # agregar cada nodo
        for nodo in self.red.nodos:
            ng = pydot.Node(nodo.nombre, style="filled", fillcolor="#f6f6f6", color="#000000", fontsize="12", shape="circle", fontname="Arial")
            self.grafico.add_node(ng)
        # crear los arcos entre los nodos
        for a in self.red.nodos:
            for b in self.red.nodos:
                v = self.red.obtener_arco(a.nombre, b.nombre)
                # solo crear el arco si su peso es > 0
                if v > 0:
                    edge = pydot.Edge(a.nombre, b.nombre, color="#004365", labelfontcolor="#004365", fontsize="10.0", fontname="Arial", label="%d" % (v))
                    self.grafico.add_edge(edge)
    
    def get_wx_image(self):
        self.grafico.write_png(os.path.join(self.temp, "grafico.png"))
        print os.path.join(self.temp, "grafico.png")
        return wx.Image(os.path.join(self.temp, "grafico.png"), wx.BITMAP_TYPE_ANY)
        