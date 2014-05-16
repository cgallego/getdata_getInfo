# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 15:24:48 2014

@author: windows
"""

import wx

ID_MENU_NEW = wx.NewId()
ID_MENU_OPEN = wx.NewId()
ID_MENU_SAVE = wx.NewId()

class MyPanel(wx.Panel):
    
    def __init__(self, *args, **kw):
        super(MyPanel, self).__init__(*args, **kw) 

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e):
        
        print 'event reached panel class'
        e.Skip()


class MyButton(wx.Button):
    
    def __init__(self, *args, **kw):
        super(MyButton, self).__init__(*args, **kw) 

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)

    def OnButtonClicked(self, e):
        
        print 'event reached button class'
        e.Skip()
        
        
class Container(wx.Frame):
  
    def __init__(self, parent, title):
        super(Container, self).__init__(parent, title=title, 
            size=(850, 400))
        
        self.InitUI()
        # Initialize frame
        self.Centre()
        self.Show()


    def InitUI(self):
    
        panel = MyPanel(self)

        self.SetTitle('Simple Table')

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Name')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        tc = wx.TextCtrl(panel)
        hbox1.Add(tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.st2 = wx.StaticText(panel, label='Output')
        self.st2.SetFont(font)
        hbox2.Add(self.st2)
        vbox.Add(hbox2, flag=wx.LEFT | wx.TOP, border=10)

        vbox.Add((-1, 10))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox3.Add(tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, 
            border=10)

        vbox.Add((-1, 25))

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb1 = wx.CheckBox(panel, label='Case Sensitive')
        cb1.SetFont(font)
        hbox4.Add(cb1)
        cb2 = wx.CheckBox(panel, label='Nested Classes')
        cb2.SetFont(font)
        hbox4.Add(cb2, flag=wx.LEFT, border=10)
        cb3 = wx.CheckBox(panel, label='Non-Project classes')
        cb3.SetFont(font)
        hbox4.Add(cb3, flag=wx.LEFT, border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=10)

        vbox.Add((-1, 25))

        # Add a button for the interaction
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        #btn1 = wx.Button(panel, label='Ok', size=(70, 30))
        #hbox5.Add(btn1)
        btn1 = MyButton(panel, label='Ok')
        hbox5.Add(btn1)
        
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        
        btn2 = wx.Button(panel, label='Close', size=(70, 30))
        hbox5.Add(btn2, flag=wx.LEFT|wx.BOTTOM, border=5)
        vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10)

        panel.SetSizer(vbox)
        
               
        #The example displays the current position of the window.
        self.Bind(wx.EVT_MOVE, self.OnMove)
        
        #  destroy the window, or veto the event. 
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        self.CreateMenuBar()
        self.CreateStatusBar()


    def CreateMenuBar(self):
        
        mb = wx.MenuBar()
        
        fMenu = wx.Menu()
        fMenu.Append(ID_MENU_NEW, 'New')
        fMenu.Append(ID_MENU_OPEN, 'Open')
        fMenu.Append(ID_MENU_SAVE, 'Save')
        
        mb.Append(fMenu, '&File')
        self.SetMenuBar(mb)
        
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_NEW)
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_OPEN)
        self.Bind(wx.EVT_MENU, self.DisplayMessage, id=ID_MENU_SAVE)
        
    def DisplayMessage(self, e):
        
        sb = self.GetStatusBar()
                
        eid = e.GetId()
        
        if eid == ID_MENU_NEW:
            msg = 'New menu item selected'
        elif eid == ID_MENU_OPEN:
            msg = 'Open menu item selected'
        elif eid == ID_MENU_SAVE:
            msg = 'Save menu item selected'
        
        sb.SetStatusText(msg)
        
        
    def OnMove(self, e):
        
        x, y = e.GetPosition()
        self.st2.SetLabel(str(x))
        self.st2.SetLabel(str(y))

    def OnCloseWindow(self, e):

        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            
        ret = dial.ShowModal()
        
        if ret == wx.ID_YES:
            self.Destroy()
        else:
            e.Veto()
            
    def OnButtonClicked(self, e):
        
        print 'event reached frame class'
        e.Skip()            

if __name__ == '__main__':
  
    app = wx.App()
    Container(None, title='Size')
    app.MainLoop()