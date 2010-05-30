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
from ui.graficacion import GraficoDeRed

class Renderer(wx.grid.PyGridCellRenderer):
    def __init__(self):
        wx.grid.PyGridCellRenderer.__init__(self)
        
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        f = attr.GetFont()
        text = grid.GetCellValue(row, col)
        if text == "0":
            dc.SetTextForeground("#cccccc")
        else:
            f.SetWeight(wx.BOLD)
            dc.SetTextForeground("BLACK")

        if (row == col):
            dc.SetBrush(wx.Brush("#f6f6f6", wx.SOLID))
        else:
            dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
        dc.SetBackgroundMode(wx.SOLID)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(rect)

        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetFont(f)

        #text = grid.GetCellValue(row, col)
        w, h = dc.GetTextExtent(text)
        x = rect.x + 1 + (rect.width - w)/2
        y = rect.y + 1 + h

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
        box = wx.StaticBox(self, -1, u"Capacidad de los arcos")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.tabla_de_arcos = wx.grid.Grid(self, -1, (-1, -1), (500, 300))
        self.datos_de_arcos = TablaDeArcos()
        self.tabla_de_arcos.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.tabla_de_arcos.SetDefaultColSize(40)
        self.tabla_de_arcos.SetDefaultRowSize(40)
        self.tabla_de_arcos.SetDefaultRenderer(Renderer())
        self.tabla_de_arcos.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.OnCellChange)
        bsizer.Add(self.tabla_de_arcos, 1, wx.EXPAND)
        hb.Add(bsizer, 1, wx.EXPAND)
        hb.AddSpacer(10)
        
        # vista previa
        box = wx.StaticBox(self, -1, u"Vista previa")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        self.panel_vista_previa = scrolledpanel.ScrolledPanel(self, -1, size=(500,300))
        self.panel_vista_previa.SetBackgroundColour("#000000")
        self.bitmap_grafo = wx.StaticBitmap(self.panel_vista_previa, -1)
        self.panel_vista_previa.SetAutoLayout(1)
        self.panel_vista_previa.SetBackgroundColour(wx.WHITE)
        self.panel_vista_previa.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.panel_vista_previa.GetSizer().Add(self.bitmap_grafo, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        self.graficador = GraficoDeRed(self.datos_de_arcos.GetRed())
        bsizer.Add(self.panel_vista_previa, 0, wx.EXPAND)
        hb.Add(bsizer, 0, wx.EXPAND)
        self.content.Add(hb, 0, wx.BOTTOM, 20)
        
        
    def OnShow(self, event):
        if event.GetShow():
            self.tabla_de_arcos.SetTable(self.datos_de_arcos)
            self.wizard.LayoutFitCenter()
            self.ActualizarVistaPrevia()
            
    def OnSpin(self, event):
        self.datos_de_arcos.SetSize(event.EventObject.GetValue())
        self.tabla_de_arcos.Refresh()
        self.tabla_de_arcos.ForceRefresh()
        self.ActualizarVistaPrevia()
        
    def OnCellChange(self, event):
        self.ActualizarVistaPrevia()
        
    def ActualizarVistaPrevia(self):
        self.graficador.graficar_red()
        image = self.graficador.get_wx_image()
        bitmap = wx.BitmapFromImage(image)
#        print image.GetSize(), self.bitmap_grafo.GetParent().GetSize()
#        if (image.GetSize()[0] > self.bitmap_grafo.GetParent().GetSize()[0]):
#            bitmap.SetSize(self.bitmap_grafo.GetParent().GetSize())
#        else:
#            bitmap.SetSize(image.GetSize())
        self.bitmap_grafo.SetBitmap(bitmap)
        self.bitmap_grafo.GetParent().Refresh()
        self.panel_vista_previa.SetupScrolling()
