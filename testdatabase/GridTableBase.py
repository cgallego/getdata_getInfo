# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 16:55:18 2014

@author: windows
"""

import wx
import wx.grid

class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
        
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        
    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        pass         


class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        tableBase = GenericTable(data, rowLabels, colLabels)
        self.SetTable(tableBase)                   

class Container(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Query Output", size=(850, 400))
        panel = wx.Panel(self)
    
        # define fots        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        #  put it in a sizer mainly because that’s just the proper way to contain widgets 
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Use generic table to create grid
        myGrid = wx.grid.Grid(panel)
        tableBase = GenericTable(data, rowLabels, colLabels)
        myGrid.SetTable(tableBase)                   
        
        # Add label to display category
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label="Patient MRI CAD record")
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        
        #  put it in a sizer mainly because that’s just the proper way to contain widgets 
        vbox.Add(myGrid, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # Set panel sizer
        panel.SetSizer(vbox)        
        self.Centre()
        self.Show()

        
        
        
#########################################################        
if __name__ == '__main__':
    global data
    
    data = (("A", "B"), 
        ("C", "D"), 
        ("E", "F"), 
        ("G", "G"),
        ("F", "F"), 
        ("Q", "Q"))
            
    colLabels = ("Last", "First")
    rowLabels = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    app = wx.PySimpleApp()
    frame = Container()
    app.MainLoop()
     