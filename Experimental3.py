import wx
import wx.grid as gridlib
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import os
import itertools
from itertools import chain
 
########################################################################
class MyPanel(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.currentlySelectedCell = (0, 0)
 
        self.myGrid = gridlib.Grid(self)
        self.myGrid.CreateGrid(101, 12)
        self.myGrid.Bind(gridlib.EVT_GRID_SELECT_CELL, self.onSingleSelect)
        self.myGrid.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.onDragSelection)
        self.myGrid.SetColLabelValue(0, "Index")
        self.myGrid.SetColLabelValue(1, "Data Path 1")
        self.myGrid.SetColLabelValue(2, "Data Path 2")
        self.myGrid.SetColLabelValue(3, "Data Path 3")
        self.myGrid.SetColLabelValue(4, "Data Path 4")
        self.myGrid.SetColLabelValue(5, "Data Path 5")
        self.myGrid.SetColLabelValue(6, "Data Path 6")
        self.myGrid.SetColLabelValue(7, "Data Path 7")
        self.myGrid.SetColLabelValue(8, "Data Path 8")
        self.myGrid.SetColLabelValue(9, "Data Path 9")
        self.myGrid.SetColLabelValue(10, "Data Path 10")
        self.myGrid.SetColLabelValue(11, "Phase Changes")
        self.myGrid.SetColSize(11, 10)
        selectBtn = wx.Button(self, label="Analyze Selection")
        selectBtn.Bind(wx.EVT_BUTTON, self.onGetSelection)
        for row in range(101):
            rowNum = row
            self.myGrid.SetRowLabelValue(row, "Row %s" % rowNum)
        self.myGrid.SetRowLabelValue(0, "Data Label")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.myGrid, 1, wx.EXPAND)
        sizer.Add(selectBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(sizer)
        
      
    #----------------------------------------------------------------------
    def onDragSelection(self, event):
        """
        Gets the cells that are selected by holding the left
        mouse button down and dragging
        """
        if self.myGrid.GetSelectionBlockTopLeft():
            top_left = self.myGrid.GetSelectionBlockTopLeft()[0]
            bottom_right = self.myGrid.GetSelectionBlockBottomRight()[0]
            self.printSelectedCells(top_left, bottom_right)
 
    #----------------------------------------------------------------------
    def onGetSelection(self, event):
        """
        Get whatever cells are currently selected
        """
        cells = self.myGrid.GetSelectedCells()
        phase_change=[]
        print self.myGrid.GetCellValue(0,10)
        for i in range(100):
            if self.myGrid.GetCellValue(i, 11): #is not string
                phase_change.append(self.myGrid.GetCellValue(i, 11))
                print phase_change
            
        for phase in phase_change:
            plt.axvline(x=float(phase), ymin=0, ymax=1.0, linewidth=12, color='w')
            plt.axvline(x=float(phase), ymin=0, ymax=1.0, linewidth=1, color='k')
        plt.show()
        os.remove('jorfile.csv')
        if not cells:
            if self.myGrid.GetSelectionBlockTopLeft():
                top_left = self.myGrid.GetSelectionBlockTopLeft()[0]
                bottom_right = self.myGrid.GetSelectionBlockBottomRight()[0]
                self.printSelectedCells(top_left, bottom_right)
            else:
                print self.currentlySelectedCell
        else:
            print cells

 
    #----------------------------------------------------------------------
    def onSingleSelect(self, event):
        """
        Get the selection of a single cell by clicking or 
        moving the selection with the arrow keys
        """
            #print "You selected Row %s, Col %s" % (event.GetRow(),
            #event.GetCol())
        self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())
        event.Skip()
 
    #----------------------------------------------------------------------
    def printSelectedCells(self, top_left, bottom_right):
        """
        Based on code from http://ginstrom.com/scribbles/2008/09/07/getting-the-selected-cells-from-a-wxpython-grid/
        """
        cells = []
 
        rows_start = top_left[0]
        rows_end = bottom_right[0]
 
        cols_start = top_left[1]
        cols_end = bottom_right[1]
 
        rows = range(rows_start, rows_end+1)
        cols = range(cols_start, cols_end+1)
 
        cells.extend([(row, col)
            for row in rows
            for col in cols])
            
        hi=[]
        for i in range(rows_end + 1):
            hi.append([])
        print hi
        for cell in cells:
            row, col = cell
            hi[row].append(self.myGrid.GetCellValue(row, col))
    
        
        
        hi2 = hi[:] #clone list of grid values
        del hi2[0] #delete first list in 2d list
      
        
        d=hi2
        df=pd.DataFrame(d, columns=hi[0])
        find_index=self.myGrid.GetCellValue(0, 0)
        with_new_index=df.set_index(str(find_index))
        print with_new_index
        with_new_index.to_csv('jorfile.csv')
        jor=pd.read_csv('jorfile.csv', index_col=find_index)
        
        markers=itertools.cycle(('o', 's', 'D', 's', 'h', '8'))
        markercolor=itertools.cycle(('k', 'w'))
        path_1_length=len(hi2)
        single_list=[i for i in chain.from_iterable(hi2)]
        print max(single_list)
        print single_list
        
        if path_1_length < 10:
            marker_logic = 7
        elif path_1_length < 15:
            marker_logic = 5
        elif path_1_length < 25:
            marker_logic = 4
        elif path_1_length > 35:
            marker_logic = 3
        else:
            marker_logic = 5
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.axes.set_ylim([0,100])
        fig.set_tight_layout(True)
        box=wx.TextEntryDialog(None, "Please enter a title", "Title", "Default Text")
        if box.ShowModal()==wx.ID_OK:
            title=box.GetValue()
            box.Destroy()
        for col in (jor):
            jor[col].plot(marker=markers.next(), figsize=(8,4), markersize=marker_logic, color='k', title=title, markerfacecolor=markercolor.next(), grid=False)


########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="SSD-Single Subject Designs", size=(950, 600))
        panel = MyPanel(self)
        self.Show()
#----Start MenuBar-------------------------------------------------
        menubar=wx.MenuBar()
        first=wx.Menu()
        second=wx.Menu()
        third=wx.Menu()
        fourth=wx.Menu()
        
        first.Append(wx.NewId(),"New Window", "This is a new window")
        first.Append(wx.NewId(),"Open...", "This will open a new window")
        first.Append(wx.NewId(), "Save Dataframe", "")
        first.Append(wx.NewId(), "Save As", "")
        quitter=first.Append(wx.NewId(),"Exit", "This will close the program")
        
        second.Append(wx.NewId(), "Cut", "This will cut the selection")
        second.Append(wx.NewId(), "Copy", "This will copy the selection")
        second.Append(wx.NewId(), "Paste", "This will paste the selection")
        
        
        third.Append(wx.NewId(), "Analyze IOA", "Analyze Interobserver Agreement Data")
        
        third.Append(wx.NewId(), "AB.. Design", "A simple baseline, intervention design with x phases.")
        third.Append(wx.NewId(), "Multiple Baseline Design", "Effects demonstrated by introducing the intervention to different baselines.")
        third.Append(wx.NewId(), "Changing Criterion Design", "A design with several subphases within the treatment phase.")
        third.Append(wx.NewId(), "Multiple-Treatment Design", "A design with 2 or more treatments in an intervention phase.")
        fourth.Append(wx.NewId(), "Import from Google Sheets", "Import a data set from Google")
        fourth.Append(wx.NewId(), "Import from Excel", "Import a data set from Microsoft Excel")
        menubar.Append(first, "File")
        menubar.Append(second, "Edit")
        menubar.Append(third, "Analyze")
        menubar.Append(fourth, "Import")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Quit, quitter)
    
#Exit Function--------------------------------------------------------
    def Quit(self, e):
        yesNoBox=wx.MessageDialog(None, "Are you sure you want to quit?", "Exit?", wx.YES_NO)
        yesNoAnswer=yesNoBox.ShowModal()
        print yesNoAnswer
        if yesNoAnswer == 5103:
            self.Close()
            yesNoBox.Destroy()
        else:
            yesNoBox.Destroy()


#-----End Menubar------------------------------------------------------
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()