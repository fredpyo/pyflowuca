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
        '''
        Crea una instancia del grafo en memoria, listo para ser rendereado
        '''
        self.grafico = pydot.Dot('rdf', graph_type='digraph')
        self.grafico.set_fontname("Arial")
        self.grafico.set_rankdir("LR") # esto es para que vaya de izquierda a derecha!!!
        # agregar cada nodo
        for nodo in self.red.nodos:
            ng = pydot.Node(nodo.nombre, style="filled", fillcolor="#f6f6f6", color="#000000", fontsize="12", shape="circle", fontname="Arial")
            self.grafico.add_node(ng)
        # crear los arcos entre los nodos
        for a in self.red.obtener_arcos():
            edge = pydot.Edge(a[0], a[1], color="#004365", labelfontcolor="#004365", fontsize="10.0", fontname="Arial", label="%d" % (a[2]))
            self.grafico.add_edge(edge)
            
    def resaltar_activos(self, a, b):
        '''
        Resalta los nodos a y b, cambiando su color y creando (o modificando)
        el arco existente entre estos dos dandole otro color
        '''
        # resaltar destino
        nodo = self.grafico.get_node(b)
        nodo.set_fillcolor("#e6ecff")
        nodo.set_color("#4e73ff")
        # resaltar origen
        nodo = self.grafico.get_node(a)
        nodo.set_fillcolor("#bac9ff")
        nodo.set_color("#4e73ff")
        # modificar o agregar arco
        e = self.grafico.get_edge(a, b)
        if e:
            e.set_color("#4e73ff")
        else:
            edge = pydot.Edge(a, b, color="#4e73ff")
            self.grafico.add_edge(edge)
    
    def marcar_origen_y_destino(self, origen, destino):
        '''
        Marca en el grafo los nodos de origen y destino
        '''
        try:
#            e = pydot.Edge("", origen, color="#004365")
#            self.grafico.add_edge(e)
            nodo = self.grafico.get_node(origen)
            nodo.set_shape("diamond")
            nodo = self.grafico.get_node(destino)
            nodo.set_shape("doublecircle")
        except:
            pass
    
    def get_wx_image(self):
        '''
        Genera una imagen temporal y retorna una instancia de un object wx.Image
        '''
        print os.path.join(self.temp, "grafico.png")
        self.grafico.write_png(os.path.join(self.temp, "grafico.png"))
        return wx.Image(os.path.join(self.temp, "grafico.png"), wx.BITMAP_TYPE_ANY)
    
    def __del__(self):
        '''
        Limpiar los archivos temporales
        '''
        print "LIMPIEZA"
        try:
            os.remove(os.path.join(self.temp, "grafico.png"))
        except:
            pass
        try:
            os.rmdir(self.temp)
        except:
            pass