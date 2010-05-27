# -*- coding: utf-8 -*-
'''
Created on 27/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''
import wx
from aerowizard import AeroPage, AeroStaticText

class PaginaInicio(AeroPage):
    '''
    Página de inicio
    '''
    def __init__(self, parent, data):
        AeroPage.__init__(self, parent, u"Bienvenido a PyFlow")
        text1 = AeroStaticText(self, -1, u"Investigación de Operaciones - Trabajo práctico\nIngeniería Informática - Junio 2010")
        self.content.Add(text1, 0, wx.BOTTOM, 10)
        
        hs = wx.BoxSizer(wx.HORIZONTAL)
        boton_nuevo_flujo = wx.Button(self, -1, u"\nCrear nuevo flujo\n ")
        boton_abrir_flujo = wx.Button(self, -1, u"\nAbrir flujo...\n ")
        hs.Add(boton_nuevo_flujo, 1, wx.EXPAND, 0)
        hs.Add(boton_abrir_flujo, 1, wx.EXPAND, 0)
        self.content.Add(hs, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 20)