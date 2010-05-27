# -*- coding: utf-8 -*-
'''
Created on 27/05/2010

@author: Federico Cáceres <fede.caceres@gmail.com>
'''

import wx
from ui.aerowizard import AeroWizard, AeroPage
from ui.wizardpages import PaginaInicio

app = wx.PySimpleApp(redirect = False)

wizard = AeroWizard(u"PyFlow")
p1 = PaginaInicio(wizard, None)
wizard.SetStartPage(p1)

ib = wx.IconBundle()
ib.AddIconFromFile("ui/img/pyflow.ico", wx.BITMAP_TYPE_ANY)
wizard.SetIcons(ib)
wizard.RunWizzard()
try:
    wizard.Destroy()
except:
    pass