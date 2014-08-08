# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 16:55:18 2014

@author: windows
"""

import wx
import wx.grid
from numpy import size
import wx.lib.scrolledpanel
scrolled = wx.lib.scrolledpanel 


class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
               
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        try: 
            cols = size(self.data)/len(self.data)
        except ZeroDivisionError: # empty
            cols=0
        return cols

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

class ScrolledPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        # --------------------------------------------------
        scrolled.ScrolledPanel.__init__(self, parent, size=wx.DisplaySize()) ##e=(1100,800)) ##wx.DisplaySize())
        # -------------------------------------------------
        self.SetAutoLayout(1)
        self.SetupScrolling()


class Container(wx.Frame):
    def __init__(self, app):
        """Cad_Container Constructor"""
        wx.Frame.__init__(self, parent=None, title="Query Output", size=wx.DisplaySize()) 
        self.panel = ScrolledPanel(self)
        self.app = app
        
        # define fots        
        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(12)

        #  put it in a sizer mainly because that’s just the proper way to contain widgets 
        self.vbox = wx.BoxSizer(wx.VERTICAL) # Base container for all widgets
        #self.vbox.Add( self.panel )
        
        ## add continue # add more control        
        btn = wx.Button(self.panel, label="Continue")
        
        hbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(btn, proportion=0, flag=wx.LEFT, border=8)
        self.vbox.Add(hbox)
        self.vbox.Add((-1, 30))
        self.panel.SetSizer(self.vbox)
        
        #continue
        btn.Bind(wx.EVT_BUTTON, self.continueExec)
        #  destroy the window, or veto the event. 
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
                   
              
    def Cad_Container_initGUI(self, data, rowLabels, colLabels):        
       
        # Add label to display category        
        st1 = wx.StaticText(self.panel, label="Patient MRI CAD record")
        st1.SetFont(self.font)
        
        hbox1 = wx.BoxSizer(wx.VERTICAL)
        hbox1.Add(st1, proportion=0, flag=wx.LEFT, border=8)
        self.vbox.Add(hbox1)
        self.vbox.Add((-1, 30))
        
        #  put it in a sizer mainly because that’s just the proper way to contain widgets 
         # Use generic table to create grid
        myGrid = wx.grid.Grid(self.panel)
        tableBase = GenericTable(data, rowLabels, colLabels)
        myGrid.AutoSizeColumns(setAsMin=False)
        myGrid.SetTable(tableBase) 
        myGrid.CanDragColSize()
        
        self.vbox.Add(myGrid, proportion=0, flag=wx.RIGHT|wx.EXPAND, border=10)
        
        self.vbox.Add((-1, 30))
        
        self.panel.SetSizer(self.vbox)
           
        
    def MassNonM_Container_initGUI(self, datamassNm, rowLabelsmassNm, colLabelsmassNm, labelPanel):        

        # Add label to display category        
        hbox2 = wx.BoxSizer(wx.VERTICAL)
        st2 = wx.StaticText(self.panel, label=labelPanel)
        st2.SetFont(self.font)
        hbox2.Add(st2, proportion=0, flag=wx.LEFT, border=8)
        self.vbox.Add(hbox2)
        self.vbox.Add((-1, 30))
        
        #  put it in a sizer mainly because that’s just the proper way to contain widgets 
        # Use generic table to create grid
        myGrid = wx.grid.Grid(self.panel)
        tablemassNm = GenericTable(datamassNm, rowLabelsmassNm, colLabelsmassNm)
        myGrid.SetTable(tablemassNm) 
        self.vbox.Add(myGrid, proportion=1, flag=wx.RIGHT|wx.EXPAND, border=10)
        
        self.vbox.Add((-1, 30))
        
        # Set panel sizer
        self.panel.SetSizerAndFit(self.vbox)
        
    
    def continueExec(self,e):
        self.app.ExitMainLoop()      
        
        
    def OnCloseWindow(self, e):

        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()         
        
#########################################################        
def test():
    """ Unit test for running module and catching errors."""
    data = (("A", "B"), 
        ("C", "D"), 
        ("E", "F"), 
        ("G", "G"),
        ("F", "F"), 
        ("Q", "Q"))
    datamass = data            
    colLabels = ("Last", "First")
    rowLabels = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    colLabelsmass = ("Second", "Thrid")
    rowLabelsmass = ("10", "20", "30", "40", "50", "6", "7", "8", "9")
    
    app = wx.PySimpleApp()
    frame = Container(None, -1)
    frame.Cad_Container_initGUI(data, rowLabels, colLabels)
    frame.MassNonM_Container_initGUI(datamass, rowLabelsmass, colLabelsmass, "Masstest")
    frame.Centre()
    frame.Show(True)
    app.MainLoop()