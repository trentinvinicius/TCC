import sys, os, time, traceback, types, datetime, string, operator
import  wx
#import ColorPanel
#from wx.lib.buttons import GenBitmapButton, GenBitmapToggleButton
import locale
import  wx.grid as gridlib
import thread, threading

msgLabels = {}
MSG_OK = wx.ID_OK
MSG_CANCEL = wx.ID_CANCEL
MSG_YES = wx.ID_HIGHEST + 101
MSG_NO = wx.ID_HIGHEST + 102
msgLabels[MSG_OK] = 'OK'
msgLabels[MSG_CANCEL] = 'Cancel'
msgLabels[MSG_YES] = 'Yes'
msgLabels[MSG_NO] = 'No'



class MsgBoxDlg(wx.Dialog):
    def __init__(
        self, parent, ID, title, msg, button1 = MSG_OK, button2 = -1, button3 = -1, size=wx.DefaultSize, pos = wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)
        #self.log = log

        box = wx.BoxSizer(wx.VERTICAL)
        btnBox = wx.BoxSizer(wx.HORIZONTAL)


        self.button1 = button1
        self.button2 = button2
        self.button3 = button3
        if button1 >= 0:
            btn1 = wx.Button(self, wx.ID_OK, msgLabels[button1])
            btn1.Bind(wx.EVT_BUTTON, self.OnButton1)
            btnBox.Add(btn1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 15)
            btn1.SetDefault()

        if button2 >= 0:
            if button3 >= 0:
                id = button2
            else:
                id = wx.ID_CANCEL
            btn2 = wx.Button(self, id, msgLabels[button2])
            btn2.Bind(wx.EVT_BUTTON, self.OnButton2)
            btnBox.Add(btn2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 15)

        if button3 >= 0:
            btn3 = wx.Button(self, wx.ID_CANCEL, msgLabels[button3])
            btn3.Bind(wx.EVT_BUTTON, self.OnButton3)
            btnBox.Add(btn3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 15)

        #---- msg
        self.msg = wx.StaticText(self,-1,msg)
        box.Add(self.msg, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT, 30)
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        box.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.LEFT|wx.RIGHT, 20)

        box.Add(btnBox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 25)
        self.SetSizer(box)
        #parent.Fit()
        box.Fit(self)


    def OnButton1(self, evt):
        #button = evt.GetId()
        self.EndModal(self.button1)
        evt.Skip()

    def OnButton2(self, evt):
        #button = evt.GetId()
        self.EndModal(self.button2)
        evt.Skip()

    def OnButton3(self, evt):
        #button = evt.GetId()
        self.EndModal(self.button3)
        evt.Skip()

def msgbox(parent, ID, title, msg, button1 = MSG_OK, button2 = -1, button3 = -1,
        size=wx.DefaultSize, pos = wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, centerparent=True):
    mbDlg = MsgBoxDlg(parent, ID, title, msg, button1, button2, button3, size, pos, style)
    parent.msgbox = mbDlg
    if centerparent:
        mbDlg.CenterOnParent()
    else:
        mbDlg.CenterOnScreen()
        mbDlg.Raise()
    f = mbDlg.ShowModal()
    parent.msgbox = None
    mbDlg.Destroy()
    return f


################################################################################
# this class can be use for message logging
class messageDlg(wx.Dialog):
    def __init__(
            self, parent, log, ID=-1, title="Messages", sizehint=(100, 100), size=(100, 100), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)
        self.log = log

        self.msgtext = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=size)

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.msgtext, 1)
        btn = wx.Button(self, -1, "Clear")
        btn.Bind(wx.EVT_BUTTON, self.onClear)
        box.Add(btn, 0)

##        btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
##        box.Add(btnCancel, 0)
##        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)


        box.SetSizeHints(self)
        self.SetSizer(box)
        #parent.Fit()
        box.Fit(self)
        #self.Fit()
        self.logging = True
        self.lock = threading.Semaphore()

    def onClear(self, event):
        self.msgtext.Clear()

    def write(self, msg):
        self.lock.acquire()
        if self.logging:
            self.msgtext.AppendText(msg)
        self.lock.release()


################################################################################
# this class is used for display image
class imageDlg(wx.Dialog):
    def __init__(
            self, parent, log, ID=-1, title="Image", sizehint=(640, 480), size=(640, 480), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)
        self.log = log

        self.bitmap = wx.StaticBitmap(self,size=size)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.bitmap, 1)
#        btn = wx.Button(self, -1, "Clear")
#        btn.Bind(wx.EVT_BUTTON, self.onClear)
#        box.Add(btn, 0)

##        btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
##        box.Add(btnCancel, 0)
##        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)


        box.SetSizeHints(self)
        self.SetSizer(box)
        #parent.Fit()
        box.Fit(self)
        #self.Fit()
        #self.lock = threading.Semaphore()

    def loadFile(self, file):
        i = wx.Image(file, wx.BITMAP_TYPE_JPEG)
        bm = wx.BitmapFromImage(i)
        self.bitmap.SetBitmap(bm)


################################################################################
class JobThreadBase():
    def __init__(self, log):
        #self.parent = parent
        self.log = log
        self.keepGoing = self.running = False

    def Start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = False

    def StopAndWait(self):
        self.Stop()
        while (self.running):
            time.sleep(0.01)

    def IsRunning(self):
        return self.running

    def IsKeepGoing(self):
        return self.keepGoing

class GridBase(gridlib.Grid):
    def __init__(self, parent, log, id, size, sortable = False, RecordNumber=False):
        gridlib.Grid.__init__(self, parent, id, size)
        self.parent = parent
        self.log = log
        self.Bind(wx.EVT_CHAR, self.OnChar)
        if sortable:
            self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnSortColReverseBase)
            self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnSortColBase)
        self.RecordNumber = RecordNumber
        self.coltypelist = None
        self.selectedRow = -1

    def setColType(self, coltypelist):
        self.coltypelist = coltypelist


    def SetRowColor(self, r, color):
        # set row attr crash
        nrcols = self.GetNumberCols()
        for c in range(nrcols):
            self.SetCellBackgroundColour(r, c, color)

    def SelectRow(self, row):
        #attr = wx.grid.GridCellAttr()
        if self.selectedRow >= 0:
            self.SetRowColor(self.selectedRow, 'WHITE')
            #attr.SetBackgroundColour('WHITE')
            #self.SetRowAttr(self.selectedRow, attr)
        if row >= 0:
            self.SetRowColor(row, 'RED')
            #attr.SetBackgroundColour('BLUE')
            #self.SetRowAttr(row, attr)
        self.selectedRow = row

    def ClearRow(self, row):
        nrcols = self.GetNumberCols()
        for c in range(0,nrcols):
            self.SetCellValue(row, c, "")

    def GetCellValueInt(self, row, col):
        v = self.GetCellValue(row, col)
        try:
            return int(v)
        except Exception, e:
            return 0

    def GetCellValueFloat(self, row, col):
        v = self.GetCellValue(row, col)
        try:
            v = v.replace(",", "")
            return float(v)
        except Exception, e:
            return 0.0

    def OnChar(self, event):
        #key = unichr(event.GetKeyCode())
        #self.log.write(unichr(key))
        #if event.GetKeyCode() in [32 , ord('0')]:
        fHeader = event.ShiftDown()
        if event.GetKeyCode() == 3:
            event.Skip()
            #Array = self.GetSelectedCells()
            #print Array
            topleft = self.GetSelectionBlockTopLeft()
            bottomright = self.GetSelectionBlockBottomRight()
            #print topleft, bottomright
            if topleft == [] or bottomright == []:
                cols = self.GetSelectedCols()
                if cols == []:
                    left = self.GridCursorCol
                    right = left + 1
                    cols = [left]
                    top = self.GridCursorRow
                    bottom = top + 1
                else:
                    cols.sort()
                    left = cols[0]
                    right = cols[-1] + 1
                    top = 0
                    bottom = self.GetNumberRows()
            else:
                cols = []
                left = topleft[0][1]
                right = bottomright[0][1] + 1
                top = topleft[0][0]
                bottom = bottomright[0][0] + 1
                for c in range(left,right):
                    cols.append(c)
        elif event.GetKeyCode() == 1:
            # copy all
            event.Skip()
            left = 0
            right = self.GetNumberCols()
            top = 0
            bottom = self.GetNumberRows()
            cols = []
            for c in range(left,right):
                cols.append(c)
        else:
            return

        if True:
            v = ""
            paste = False
            if fHeader:
                for c in cols:
                    v = v + self.GetColLabelValue(c) + "\t"
                v = v + "\n"

            for row in range(top,bottom):
                if row > top:
                    v = v + "\n"
                for col in range(left,right):
                    if col in cols:
                        if col > left:
                            v = v + "\t"
                        x = self.GetCellValue(row, col).strip()
                        if len(x) > 0:
                            paste = True
                        v = v + x

            if paste:
                clipdata = wx.TextDataObject()
                clipdata.SetText(v)
                self.cb = wx.Clipboard()
                self.cb.Open()
                self.cb.SetData(clipdata)
                self.cb.Close()


    def OnSortColBase(self, evt):
        col = evt.GetCol()
        if col > 0 or not self.RecordNumber:
            self.SortColBase(col, False)

    def OnSortColReverseBase(self, evt):
        col = evt.GetCol()
        if col > 0 or not self.RecordNumber:
            self.SortColBase(col, True)

    def SortColBase(self, c, freverse):
        list= []
        slist = []
        for row in range(0,self.GetNumberRows()):
            record = []
            srecord = [row]
            for col in range(0, self.GetNumberCols()):
                record.append(self.GetCellValue(row, col))
                if (self.coltypelist == None and c > 0) or  (self.coltypelist != None and self.coltypelist[c] == 'N'):
                    srecord.append(self.GetCellValueFloat(row, col))
                else:
                    srecord.append(self.GetCellValue(row, col))
            list.append(record)
            slist.append(srecord)

        if (self.coltypelist == None and c > 0) or  (self.coltypelist != None and self.coltypelist[c] == 'N'):
            slist = sorted(slist,key=operator.itemgetter(c+1), reverse=freverse)
        else:
            slist = sorted(slist,cmp=lambda x,y: cmp(x.lower(), y.lower()), key=operator.itemgetter(c+1), reverse=freverse)


        for row in range(0,len(list)):
            record = list[slist[row][0]]
            for col in range(0, self.GetNumberCols()):
                if col == 0 and self.RecordNumber:
                    self.SetCellValue(row, col, "%d" % (row+1))
                else:
                    self.SetCellValue(row, col, record[col])

#####################################################################################3
def tuple_format(t, mask="%0.2f"):
    ret = "("
    for i in range(len(t)):
        if i > 0:
            ret += ", "
        ret += mask % t[i]
    ret += ")"
    return ret


#####################################################################################3
class myApp(wx.App):
    def OnInit(self):
            dlg = imageDlg(None, self)
            dlg.loadFile(sys.argv[1])
            dlg.ShowModal()
            dlg.Destroy()
            return False

    def write(self, s):
        print s

def main():
    _app = myApp(0)
    _app.MainLoop()

if __name__ == '__main__':
    main()
