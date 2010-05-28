# -*- coding: utf-8 -*-
'''
Created on 27/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''
import wx
import wx.grid
import wx.lib.scrolledpanel as scrolledpanel
from aerowizard import AeroPage, AeroStaticText
from gridtables import TablaDeArcos

class Renderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        wx.grid.PyGridCellRenderer.__init__(self)
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)

        dc.SetBackgroundMode(wx.TRANSPARENT)
        f = attr.GetFont()
        f.SetWeight(wx.BOLD)
        dc.SetFont(f)

        text = grid.GetCellValue(row, col)
        w, h = dc.GetTextExtent(text)
        x = rect.x + 1 + (rect.width - w)/2
        y = rect.y + 1 + h

        if text == "0":
            dc.SetTextForeground("WHITE")
        else:
            dc.SetTextForeground("BLACK")

        for ch in text:
            dc.DrawText(ch, x, y)
            w, h = dc.GetTextExtent(ch)
            x = x + w
            if x > rect.right - 5:
                break


    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)


    def Clone(self):
        return Renderer()

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
        self.Bind(wx.EVT_BUTTON, self.EventoNuevo, boton_nuevo_flujo)
        boton_abrir_flujo = wx.Button(self, -1, u"\nAbrir flujo...\n ")
        hs.Add(boton_nuevo_flujo, 1, wx.EXPAND, 0)
        hs.Add(boton_abrir_flujo, 1, wx.EXPAND, 0)
        self.content.Add(hs, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.BOTTOM, 20)
    
    def EventoNuevo(self, event):
        self.wizard.route = "nuevo"
        self.GoToNext()
        
    def EventoAbrir(self, event):
        self.wizard.route = "abrir"
        self.GoToNext()
        
    def GetNext(self):
        return None
        
class PaginaCrearRed(AeroPage):
    '''
    Página para crear red
    '''
    def __init__(self, parent, data):
        AeroPage.__init__(self, parent, u"Defina la red")
        instrucciones = AeroStaticText(self, -1, u"Indique la cantidad de nodos que tendrá la red y los arcos que hay entre ellos.")
        self.content.Add(instrucciones, 0, wx.BOTTOM, 10)
        
        # cantidad de nodos
        hb = wx.BoxSizer(wx.HORIZONTAL)
        l = wx.StaticText(self, -1, u"Nodos:")
        hb.Add(l, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.cantidad_nodos = wx.SpinCtrl(self, -1, "3")
        self.cantidad_nodos.SetRange(1, 50)
        self.Bind(wx.EVT_SPINCTRL, self.OnSpin, self.cantidad_nodos)
        hb.Add(self.cantidad_nodos)
        self.content.Add(hb, 0, wx.BOTTOM, 10)
        
        hb = wx.BoxSizer(wx.HORIZONTAL)
        # tabla de arcos
        self.tabla_de_arcos = wx.grid.Grid(self, -1, (-1, -1), (500, 300))
        self.datos_de_arcos = TablaDeArcos()
        self.tabla_de_arcos.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.tabla_de_arcos.SetDefaultColSize(40)
        self.tabla_de_arcos.SetDefaultRowSize(40)
        self.tabla_de_arcos.SetDefaultRenderer(Renderer())
        hb.Add(self.tabla_de_arcos, 1, wx.EXPAND)
        hb.AddSpacer(10)
        # vista previa
        self.panel_vista_previa = scrolledpanel.ScrolledPanel(self, -1, size=(500,300))
        self.panel_vista_previa.SetBackgroundColour("#000000")
        hb.Add(self.panel_vista_previa, 0, wx.EXPAND)
        self.content.Add(hb, 0, wx.BOTTOM, 20)
        
    def OnShow(self, event):
        if event.GetShow():
            print "HOLA MUNDO"
            self.tabla_de_arcos.SetTable(self.datos_de_arcos)
            self.wizard.LayoutFitCenter()
            print "HOLA MUNDO"
            
    def OnSpin(self, event):
        self.datos_de_arcos.SetSize(event.EventObject.GetValue())
        print ">Z>L;SDPLASMDOASMDOKASMDOK MS AOKDMAS OKDMOKASDMOK"
        self.tabla_de_arcos.Refresh()
        self.tabla_de_arcos.ForceRefresh()
