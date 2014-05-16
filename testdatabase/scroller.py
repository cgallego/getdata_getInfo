# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 13:34:47 2014

@author: windows
"""

# Broken down here to show sizer child-parent hiearchy 
# AND widget child-parent hiearchy need to be congruent

import wx
import wx.lib.scrolledpanel
scrolled = wx.lib.scrolledpanel #i use reload(...) in pyslices.py


class Panel(wx.Panel):
    def __init__(self, parent, color='black'):
        wx.Panel.__init__(self, parent, size=(800,100))

        # several "Panels" sized added together 
        # are bigger than ScrolledPanel size

        self.SetMinSize( (800, 100) )
        self.SetBackgroundColour( color )

        widget1 = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        widget2 = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( widget1, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( widget2, 1, wx.ALL | wx.EXPAND, 15 )

        self.SetSizer( sizer )


class BigPanel(wx.Panel):
    def __init__(self, parent):

        # at least one child widget or aggregate width 
        # of several child widgets has to be wider than 
        # ScrolledPanel to show its horizontal scroll bar

        # at least one child widget or aggregate height
        # of more then one child widget has to be "taller" than
        # the height of the ScrolledPanel for it to show
        # its vertical scroll bar

        # -------------------------------------V---V
        wx.Panel.__init__(self, parent, size=(800,800))
        # -------------------------------------^---^

        panel0 = Panel(self, 'black')
        panel1 = Panel(self, 'red')
        panel2 = Panel(self, 'green')
        panel3 = Panel(self, 'blue')
        panel4 = Panel(self, 'white')
        panel5 = Panel(self, 'purple')

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add( panel0, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( panel1, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( panel2, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( panel3, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( panel4, 1, wx.ALL | wx.EXPAND, 15 )
        sizer.Add( panel5, 1, wx.ALL | wx.EXPAND, 15 )

        self.SetSizer( sizer )


class ScrolledPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        # ---------------------------------------------------V---V
        scrolled.ScrolledPanel.__init__(self, parent, size=(400,400))
        # ---------------------------------------------------^---^

        bigpanel = BigPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( bigpanel, 1, wx.ALL | wx.EXPAND, 15 )

        self.SetSizer( sizer )
        self.SetAutoLayout(1)
        self.SetupScrolling()


class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent = wx.GetApp().GetTopWindow(),
            title = 'Trouble with scrolling through several panels in wxpython',
            size = (500,400))

        scroll = ScrolledPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add( scroll, 1, wx.ALL | wx.EXPAND, 15 )
        self.SetSizer( sizer )


if __name__ == '__main__':
    app = wx.GetApp()
    if not app: app = wx.App(0)
    frame = Frame()
    frame.Show()
    if not app.IsMainLoopRunning():
        app.MainLoop()