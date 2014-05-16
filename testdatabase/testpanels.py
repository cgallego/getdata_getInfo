# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 17:19:20 2014

@author: windows
"""

#!/usr/bin/env python

import wx

class MyFrame(wx.Frame):
  def __init__(self, prnt, ID):
    wx.Frame.__init__(self, prnt, wx.ID_ANY)

    topLevelBox = wx.BoxSizer(wx.VERTICAL)        # Base container for all widgets
    row4 = wx.BoxSizer(wx.HORIZONTAL)             # Fourth  row of widgets
    row4b = wx.BoxSizer(wx.HORIZONTAL)            # for the Add button

    # Fourth row:
    labelTSNum = wx.StaticText(self, wx.ID_ANY, label='No. of fuzzy sets:')
    varTSNum = wx.SpinCtrl(self, wx.ID_ANY, '3', size=wx.Size(50,28),
                           style=wx.SP_ARROW_KEYS|wx.SP_WRAP, min=1, max=7, initial=3)

    labelTSName = wx.StaticText(self, wx.ID_ANY, label='Names:')
    varTSName = wx.ComboBox(self, wx.ID_ANY, size=wx.Size(125, 25), style=wx.CB_DROPDOWN)
 
    labelRHS = wx.StaticText(self, wx.ID_ANY, 'Consequent geometry:')
    varRHS = wx.Choice(self, wx.ID_ANY, choices=['Fuzzy Space', 'Singleton', 'Vote Bounded'],
                       style=wx.TAB_TRAVERSAL|wx.RAISED_BORDER)

    addTS = wx.Button(self, wx.ID_ADD, 'Add term set')

    row4b.Add(addTS, 0, wx.ALIGN_CENTER_HORIZONTAL)
    

    TermSetSizer = wx.BoxSizer(wx.HORIZONTAL)
    TermSetSizer.Add(labelTSNum, 0, wx.Right|wx.TOP, 5)
    TermSetSizer.Add(varTSNum, 0, wx.ALL, 5)
    TermSetSizer.Add(labelTSName, 0, wx.ALL, 5)
    TermSetSizer.Add(varTSName, 0, wx.ALL, 5)
    TermSetSizer.Add(labelRHS, 0, wx.ALL, 5)
    TermSetSizer.Add(varRHS, 0, wx.ALL, 5)
    TermSetSizer.Add((-1,50), 0)
    
    row4.Add(TermSetSizer, 0)
    
    TermSetBox = wx.StaticBox(self, wx.ID_ANY, label=' Fuzzy Term Set ',
                       style=wx.RAISED_BORDER)
    outerBox = wx.StaticBoxSizer(TermSetBox, wx.VERTICAL)           # Adds to space around widgets

    outerBox.Add(row4, 1, wx.EXPAND|wx.ALL, 5)
    outerBox.Add(row4b, 0, wx.CENTER)

    topLevelBox.Add(outerBox, 0, wx.ALL, 10)
    self.SetSizerAndFit(topLevelBox)


app = wx.App()
frame = MyFrame(None, -1)
frame.Show()
app.MainLoop()