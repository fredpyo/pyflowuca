# -*- coding: utf-8 -*-
'''
Created on 28/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

class RedDeFlujo(object):
    def __init__(self):
        self.nodos = []
        self.arcos = {}
        self.profundidad_maxima = 0
        self.origen = None
        self.destino = None
    
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
            
    def conectar_nodos(self, nodo1, nodo2, capacidad, bidireccional = False):
        capacidad = int(capacidad)
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
        
    def obtener_arcos(self, nodo_origen = None):
        '''
        Retorna una lista de tuplas de arcos de todo el grafo o de un nodo en particular
        (nombre origen, nombre destino, capacidad)
        '''
        arcos = []
        if nodo_origen == None:
            for a in self.nodos:
                for b in self.nodos:
                    v = self.obtener_arco(a.nombre, b.nombre)
                    if v > 0:
                        arcos.append((a.nombre, b.nombre, v))
        else:
            for a in self.nodos:
                v = self.obtener_arco(nodo_origen, a.nombre)
                if v > 0:
                    arcos.append((nodo_origen, a.nombre, v))    
        return arcos
    
    def obtener_rutas(self, origen, destino):
        self.profundidad_maxima = len(self.nodos)
        arbol = []
        if origen in [n.nombre for n in self.nodos] and destino in [n.nombre for n in self.nodos]:
            arbol = self.__recorrer(origen)
        return self.__concatenar_arbol(arbol)
    
    def __recorrer(self, nodo, profundidad = 0):
        if profundidad == self.profundidad_maxima:
            return None
        x = []
        for a in self.obtener_arcos(nodo):
            x = x + self.__recorrer(a[1], profundidad + 1)
        #x = [self.__recorrer(a[1], profundidad + 1) for a in self.obtener_arcos(nodo)]
        if len(x) > 0:
            return [nodo, x]
        return [nodo]
        
    def __concatenar_arbol(self, arbol):
        '''
        Convierte una representación de arbol:
        ["A",["B","C",["D","E"]]]
        a:
        [["A","B"],["A","C","D"],["A","C","E"]]
        '''
        s = []
        for i in arbol:
            if type(i) != list:
                s.append([i])
            else:
                l = s.pop()
                for x in self.__concatenar_arbol(i):
                    s.append(l+x)
        return s
                
    def __str__(self):
        #print [x.nombre for x in self.nodos]
        #print [x for x in self.arcos.iteritems()]
        for x in self.arcos.iteritems():
            for y in x[1].iteritems():
                print x[0], y[0], y[1]
        #return ""
        return "%s" % (",".join([str(x) for x in self.nodos]))    

class RedResidual(object):
    def __init__(self, red):
        '''
        Crear una red residual a partir de la red normal
        '''
        self.red = red
        self.nodos = [n.nombre for n in red.nodos]
        # generar la matriz de arcos N x N
        self.arcos = {}
        for a in self.nodos:
            arcos = {}
            for b in self.nodos:
                arcos[b] = red.obtener_arco(a, b)
            
            self.arcos[a.nombre] = arcos

    def solucionar(self):
        pass
        

class Nodo(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = {}
    
    def __str__(self):
        return "<Nodo: %s>" % self.nombre
    
if __name__ == "__main__":
    r = RedDeFlujo()
    
    r.agregar_nuevo_nodo("O")
    r.agregar_nuevo_nodo("A")
    r.agregar_nuevo_nodo("B")
    r.agregar_nuevo_nodo("C")
    r.agregar_nuevo_nodo("D")
    r.agregar_nuevo_nodo("E")
    r.agregar_nuevo_nodo("T")
    
    r.conectar_nodos("O", "A", 5)
    r.conectar_nodos("O", "B", 7)
    r.conectar_nodos("O", "C", 4)
    r.conectar_nodos("A", "B", 1)
    r.conectar_nodos("A", "D", 3)
    r.conectar_nodos("B", "C", 2)
    r.conectar_nodos("B", "D", 4)
    r.conectar_nodos("B", "E", 5)
    r.conectar_nodos("C", "E", 4)
    r.conectar_nodos("D", "T", 9)
    r.conectar_nodos("E", "D", 1)
    r.conectar_nodos("E", "T", 6)
    
    rutas = r.obtener_rutas("O","T")
    
    print rutas
    print len(rutas)