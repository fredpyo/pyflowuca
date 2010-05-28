# -*- coding: utf-8 -*-
'''
Created on 28/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

class RedDeFlujo(object):
    def __init__(self):
        self.nodos = []
        self.arcos = {}
    
    def __nuevo_nodo(self, nodo):
        self.arcos[nodo.nombre] = {}
    
    def agregar_nuevo_nodo(self, nombre):
        print "agregar", nombre
        nodo = Nodo(nombre)
        self.nodos.append(nodo)
        self.__nuevo_nodo(nodo)
        
    def agregar_nodo(self, nodo):
        if (type(nodo) == Nodo):
            self.nodos.append(nodo)
            self.__nuevo_nodo(nodo)
            
    def quitar_nodo(self, nodo):
        print "BORRAR", nodo, "(%d)" % len(self.nodos)
        if type(nodo) == Nodo:
            nombre = nodo.nombre
        elif type(nodo) == str:
            # borrar de los arcos
            for i in self.arcos:
                for j in self.arcos[i]:
                    try:
                        self.arcos[j].pop(j)
                    except KeyError:
                        pass
            # borrar el nodo en cuestion
            n = None
            for i in self.nodos:
                if i.nombre == nodo:
                    n = i
                    break
            if n != None:
                self.nodos.remove(n)
        print "BORRADO", nodo, "(%d)" % len(self.nodos)
            
    def conectar_nodos(self, nodo1, nodo2, capacidad, bidireccional):
        if (type(nodo1) == type(nodo2) == Nodo):
            self.arcos[nodo1.nombre][nodo2.nombre] = capacidad
            if bidireccional == True:
                self.arcos[nodo2.nombre][nodo1.nombre] = capacidad
        if (type(nodo1) == type(nodo2) == str):
            self.arcos[nodo1][nodo2] = capacidad
            if bidireccional == True:
                self.arcos[nodo2][nodo1] = capacidad
    
    def desconectar_nodos(self, nodo1, nodo2, bidireccional):
        if (type(nodo1) == type(nodo2) == Nodo):
            self.arcos[nodo1.nombre].pop(nodo2.nombre)
            if bidireccional == True:
                self.arcos[nodo2.nombre].pop(nodo1.nombre)
        if (type(nodo1) == type(nodo2) == str):
            self.arcos[nodo1].pop(nodo2)
            if bidireccional == True:
                self.arcos[nodo2].pop(nodo1)
    
    def obtener_arco(self, nodo1, nodo2):
        try:
            return self.arcos[nodo1][nodo2]
        except KeyError:
            return 0
                
    def __str__(self):
        #print [x.nombre for x in self.nodos]
        #print [x for x in self.arcos.iteritems()]
        for x in self.arcos.iteritems():
            for y in x[1].iteritems():
                print x[0], y[0], y[1]
        #return ""
        return "%s" % (",".join([str(x) for x in self.nodos]))    
    
class Nodo(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = {}
    
    def __str__(self):
        return "<Nodo: %s>" % self.nombre
    
if __name__ == "__main__":
    r = RedDeFlujo()
    r.agregar_nuevo_nodo("a")
    r.agregar_nuevo_nodo("b")
    r.agregar_nuevo_nodo("c")
    r.agregar_nuevo_nodo("d")
    r.agregar_nuevo_nodo("e")
    
    r.conectar_nodos("a", "b", 12, True)
    r.conectar_nodos("a", "c", 5, True)
    r.conectar_nodos("b", "c", 8, True)
    r.conectar_nodos("b", "d", 8, True)
    r.conectar_nodos("c", "e", 7, True)
    r.conectar_nodos("d", "e", 20, True)
    print r
        
