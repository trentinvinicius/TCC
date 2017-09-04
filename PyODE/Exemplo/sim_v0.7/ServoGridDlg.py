import os
import  wx
import  wx.grid as gridlib
import datetime, threading
import wxcommon, string
from array import array
import sequencer
import vworld

# file to store the previous editor content
editorfile = "editor.txt"

class ServoDetailGrid(wxcommon.GridBase):
    def __init__(self, parent, log):
        wxcommon.GridBase.__init__(self, parent, log, -1, size=(500, 600), sortable=True, RecordNumber=False)
        self.CreateGrid(0,0)
        self.Bind(wx.EVT_IDLE, self.onIdle)

    def Load(self, servomanager, servolist):
        self.cols = [
            ['#', '%d', wx.ALIGN_RIGHT,wx.ALIGN_CENTER ],
            ['Group', '%s', wx.ALIGN_LEFT,wx.ALIGN_CENTER ],
            ['Name', '%s', wx.ALIGN_LEFT,wx.ALIGN_CENTER ],
            ['Min', '%0.2f', wx.ALIGN_RIGHT,wx.ALIGN_CENTER ],
            ['Max', '%0.2f', wx.ALIGN_RIGHT,wx.ALIGN_CENTER ],
            ['Angle', '%0.2f', wx.ALIGN_RIGHT,wx.ALIGN_CENTER ],
        ]
        self.setColType(['N', 'S', 'S', 'N', 'N', 'N'])

        self.servomanager = servomanager
        self.servolist = servolist
        cols = self.cols
        #self.CreateGrid(len(datalist),len(cols))
        nrrows = self.GetNumberRows()
        nrcols = self.GetNumberCols()
        if nrrows > 0:
            self.DeleteRows(numRows=nrrows)
        if nrcols > 0:
            self.DeleteCols(numCols=nrcols)
        self.AppendCols(len(cols))
        self.AppendRows(len(servolist))

        for i in range(0, len(cols)):
            self.SetColLabelValue(i, cols[i][0])

        i = 0
        for servo in servolist:
            #[servonumber, name, amin, amax, angle] = servo
            #print servo
            j = 0
            for data in servo:
                self.SetCellValue(i,j,self.cols[j][1] % data)
                self.SetCellAlignment(i,j,self.cols[j][2],self.cols[j][3])
                j += 1
            i += 1

        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        #self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnCellSelect)
        #self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)

        self.AutoSizeColumns(True)
        self.EnableEditing(False)
        #self.SetSelectionMode(self.wxGridSelectRows)
        self.SetSelectionMode(self.wxGridSelectCells)
        self.SetRowLabelSize(1)

        #size = self.GetBestSize()
        #self.SetMaxSize(size.GetWidth(), 200)
        #self.log.write("size %d %d\n" % ( size.GetWidth(), size.GetHeight() ))
        self.Fit()
        self.parent.Fit()

    def onIdle(self, evt):
        nrrows = self.GetNumberRows()
        for i in range(nrrows):
            servoname = self.GetCellValue(i,2)
            servo = self.servomanager.map[servoname]
            angle = vworld.RadianToDegree(servo.getServoAngle())
            self.SetCellValue(i,5, self.cols[5][1] % angle)

    def OnCellLeftClick(self, evt):
        r = evt.GetRow()
        if self.selectedRow >= 0:
            servoname = self.GetCellValue(self.selectedRow,2)
            servo = self.servomanager.map[servoname]
            servo.changeColor(None)
        self.SelectRow(r)
        servoname = self.GetCellValue(r,2)
        servo = self.servomanager.map[servoname]
        servo.changeColor((1.0,0,0))

    def OnCellLeftDClick(self, evt):
        r = evt.GetRow()
        self.parent.ServoSelect(self.GetCellValue(r,0))


##    def LoadList(self, servolist):
##        self.cols = [
##            ['#', '%d', wx.ALIGN_RIGHT,wx.ALIGN_CENTER ],
##            ['Name', '%s', wx.ALIGN_LEFT,wx.ALIGN_CENTER ],
##        ]
##        self.servolist = servolist
##        #for s in servolist:
##        #    self.cols.append( ["%d" % s.servonumber, '%0.2f', wx.ALIGN_RIGHT, wx.ALIGN_CENTER ])
##
##        self.date = date
##        cols = self.cols
##        #self.CreateGrid(len(datalist),len(cols))
##        nrrows = self.GetNumberRows()
##        nrcols = self.GetNumberCols()
##        if nrrows > 0:
##            self.DeleteRows(numRows=nrrows)
##        if nrcols > 0:
##            self.DeleteCols(numCols=nrcols)
##        self.AppendCols(len(cols))
##        self.AppendRows(len(result))
##
##        #self.Fit()
##        #parent.Fit()
##
##        for i in range(0, len(cols)):
##            self.SetColLabelValue(i, cols[i][0])
##
##        i = 0
##        for code in result:
##             self.SetCellValue(i,0,self.cols[0][1] % code)
##             name = dbcommon.dbcache.GetStockDefaultName(code)
##             self.SetCellValue(i,1,self.cols[1][1] % name)
##
##             list = result[code]
##             j = 2
##             for data in list:
##                 if data != None:
##                     ok, running, delta = data
##                     if ok:
##                        self.SetCellValue(i,j,self.cols[j][1] % (running * 100))
##                        self.SetCellAlignment(i,j,self.cols[j][2],self.cols[j][3])
##                     j = j + 1
##
##             i = i + 1
##
##
####        dateset = result
####        for i in range(0, len(dateset)):
####            sector, data = dateset[i]
####            for j in range(0, len(self.cols)):
####                if j == 0:
####                    self.SetCellValue(i,0,self.cols[0][1] % sector)
####                else:
####                    self.SetCellValue(i,j,self.cols[j][1] % (data[j-1] * 100))
####                self.SetCellAlignment(i,j,self.cols[j][2],self.cols[j][3])
##
##        self.AutoSizeColumns(True)
##
##        ##self.DisableCellEditControl()
##        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
##        #self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
##        #self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnCellSelect)
##        #self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
##
##        self.AutoSizeColumns(True)
##        self.EnableEditing(False)
##        #self.SetSelectionMode(self.wxGridSelectRows)
##        self.SetSelectionMode(self.wxGridSelectCells)
##        self.SetRowLabelSize(1)
##
##        #size = self.GetBestSize()
##        #self.SetMaxSize(size.GetWidth(), 200)
##        #self.log.write("size %d %d\n" % ( size.GetWidth(), size.GetHeight() ))
##
##

class ServoDetailDlg(wx.Dialog):
    def __init__(
            self, parent, log, ID, title, size=(100, 500), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, model=None
            ):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)
        self.log = log
        self.model = model
        self.parent = parent
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        box = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.Bind(wx.EVT_IDLE, self.onIdle)

        #-- filter
#        self.tcFilter = wx.TextCtrl(self,-1,key,size=(150,-1))
#        self.tcFilter.SetInsertionPointEnd()
#        self.tcFilter.SetFont(font)
#        box.Add(self.tcFilter, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        self.detailGrid = ServoDetailGrid(self, self.log)
        #if result != None:
        #    self.detailGrid.LoadList(result)
        box.Add(self.detailGrid, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        self.editor = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(200,200))
        self.result = wx.TextCtrl(self,style=wx.TE_MULTILINE,size=(200,200))
        hbox.Add(self.result, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 0)
        hbox.Add(self.editor, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 0)
        box.Add(hbox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        self.messageBox = wx.StaticText(self, size=(300,30))
        box.Add(self.messageBox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        #--- Ok Cancel Button
        btnExecute = wx.Button(self, -1, "Execute")
        btnStepping = wx.Button(self, -1, "Stepping")
        btnStop = wx.Button(self, -1, "Stop")
        #btnExecute = wx.Button(self, wx.ID_OK, "Execute")
        #btnExecute.SetDefault()
        btnRestore = wx.Button(self, -1, "Restore")
        btnRecording = wx.ToggleButton(self, -1, "Recording")
        btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        btnBox1 = wx.BoxSizer(wx.HORIZONTAL)
        btnBox1.Add(btnExecute, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        btnBox1.Add(btnStepping, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        btnBox1.Add(btnStop, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        box.Add(btnBox1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        btnBox2 = wx.BoxSizer(wx.HORIZONTAL)
        btnBox2.Add(btnRestore, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        btnBox2.Add(btnRecording, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        btnBox2.Add(btnCancel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT, 5)
        box.Add(btnBox2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER|wx.ALL, 2)

        self.SetSizer(box)
        box.Fit(self)

        # Binding
#        self.Bind(wx.EVT_TEXT, self.OnFilter, self.tcFilter)
        btnExecute.Bind(wx.EVT_BUTTON, self.OnExecute)
        btnStepping.Bind(wx.EVT_BUTTON, self.OnStepping)
        btnStop.Bind(wx.EVT_BUTTON, self.OnStop)

        btnRestore.Bind(wx.EVT_BUTTON, self.OnRestore)
        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.btnRecording = btnRecording
        self.seq = None
        self.recording = False
        self.stoppingjob = False
        self.LoadEditor()
        self.framerate = 30.0
        self.lock = threading.Semaphore()


    def LoadEditor(self):
        try:
            if os.path.exists(editorfile):
                fp = open(editorfile, "r")
                s = fp.read()
                fp.close()
                self.editor.SetValue(s)
        except Exception,e:
            self.log.write("Unable to read file %s, error %s\n" % (editorfile, e))

    def SaveEditor(self):
        try:
            fp = open(editorfile, "w")
            fp.write(self.editor.GetValue())
            fp.close()
        except Exception,e:
            self.log.write("Unable to write file %s, error %s\n" % (editorfile, e))


    def Load(self, servomanager):
        datalist = []
        self.servomanager = servomanager
        for group in servomanager.getGroupNames():
            servolist = servomanager.getServoList(group)
            for s in servolist:
                data = [s.servonumber, group, s.getLongName(), vworld.RadianToDegree(s.amin), vworld.RadianToDegree(s.amax), vworld.RadianToDegree(s.getServoAngle())]
                datalist.append(data)
        self.detailGrid.Load(servomanager,datalist)


    def OnRestore(self, evt):
        if self.model != None:
            self.model.RestorePosition()


    def write(self, message):
        if self.lock.acquire(False):
            self.messageBox.SetLabel(message)
            self.lock.release()

    def execute(self, stepping):
        if self.seq == None and self.model != None:
            self.seq = sequencer.Sequencer(self, self, self.model)
            if (self.seq.Parse(self.editor.GetValue())):
                self.result.SetValue("")
                self.model.setRecorder(None, self.framerate)
                self.recording = False
                if not stepping:
                    if (self.btnRecording.GetValue()):
                        self.recording = True
                        self.parent.startRecording(self.framerate)
                        self.model.setRecorder(self.parent,self.framerate)
                self.seq.Execute(self.servomanager,stepping)
            else:
                self.seq = None

    def OnExecute(self, evt):
        self.execute(False)

    def OnStepping(self, evt):
        if self.seq == None:
            self.execute(True)
        else:
            self.seq.NextStep()

    # sequencer job will call this before existing
    def OnSequencerExit(self, sequencer):
        self.seq = None
        self.StopRecording()

    def appendResult(self, text):
        if self.lock.acquire(False):
            self.result.WriteText(text)
            self.lock.release()

    def StopRecording(self):
        if (self.recording):
            self.model.setRecorder(None,self.framerate)
            self.parent.stopRecording()
            self.recording = False

    def StopSequencer(self):
        self.stoppingjob = False
        if self.seq != None:
            self.StopRecording()
            self.seq.StopAndWait()
            t = self.seq.totalTime
            self.seq = None
            return t
        return 0.0

    def onIdle(self, evt):
        if self.stoppingjob:
            if self.lock.acquire(False):
                t = self.StopSequencer()
                self.lock.release()
                self.appendResult("Running time: %0.1f" % t)

    def OnStop(self,evt):
        self.stoppingjob = True

    def OnCancel(self, evt):
        if self.seq != None:
            return
        self.SaveEditor()
        #self.StopSequencer()
        self.EndModal(0)

    def ServoSelect(self, servono):
        self.editor.WriteText("servo : %s : " % servono)
        p = self.editor.GetInsertionPoint()
        self.editor.WriteText("pos : time\n")
        self.editor.SetInsertionPoint(p)
        self.editor.SetFocus()
