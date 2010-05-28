# -*- coding: utf-8 -*-
'''
Tablas que se utilizarán para el wx.grid.Grid

Created on 28/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

import wx
import wx.grid
from model.red import RedDeFlujo

class TablaDeArcos(wx.grid.PyGridTableBase):
    '''
    Tabla donde se almacenan la cantidad de nodos y los arcos (con su capacidad)
    '''
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = RedDeFlujo()
        
        self.data.agregar_nuevo_nodo("a")
        self.data.agregar_nuevo_nodo("b")
        self.data.agregar_nuevo_nodo("c")
        self.data.agregar_nuevo_nodo("d")
        self.data.agregar_nuevo_nodo("e")
        self.data.agregar_nuevo_nodo("f")
        
        print ">>>", len(self.data.nodos)
        
    def GetRed(self):
        '''Retornar la red almacenada en esta tabla'''
        return self.data
    
    def SetSize(self, i):
        print len(self.data.nodos), self.data.nodos
        if (i < len(self.data.nodos)):
            print "MENOS"
            change = len(self.data.nodos) - i
            while (len(self.data.nodos) > i):
                self.data.quitar_nodo(chr(97 + len(self.data.nodos) - 1))
            # notify!
            msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_COLS_DELETED, len(self.data.nodos) + change, change)
            self.GetView().ProcessTableMessage(msg)
            msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED, len(self.data.nodos) + change, change)
            self.GetView().ProcessTableMessage(msg)
        if (i > len(self.data.nodos)):
            print "MAS"
            change = i - len(self.data.nodos)
            while (len(self.data.nodos) < i):
                self.data.agregar_nuevo_nodo(chr(97 + len(self.data.nodos)))
            # notify!
            msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_COLS_APPENDED, change)
            self.GetView().ProcessTableMessage(msg)
            msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, change)
            self.GetView().ProcessTableMessage(msg)
    
    # -----------
    # Cosas requeridas por PyGridTable
    
    def GetNumberRows(self):
        print self.data.nodos
        print "COLS"
        return len(self.data.nodos)
    
    def GetNumberCols(self):
        print self.data.nodos
        print "COLS"
        return len(self.data.nodos)
    
    def IsEmptyCell(self, row, col):
        return False
    
    def GetValue(self, row, col):
        return self.data.obtener_arco(chr(97+row), chr(97+col))
    
    def SetValue(self, row, col, value):
        self.data.conectar_nodos(chr(97+row), chr(97+col), value, False)
    
    # -------------
    # etiquetas!
    
    def GetColLabelValue(self, col):
        return chr(col + 97)
    
    def GetRowLabelValue(self, row):
        return chr(row + 97)
    
    
    
        