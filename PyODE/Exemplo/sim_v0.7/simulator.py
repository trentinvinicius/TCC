import math, datetime, os
import wx, time
import ImageGrab,Image  # PIL
import wxcommon
import vworld
import model1
#import model_servo
import model_gripper
import ServoGridDlg
import myVideo
#from visual import *


#####################################################3
id_SPACE = 11000
id_MODEL_1 = 11001
id_MODEL_2 = 11002

id_MODEL_UNLOAD = 11005
id_SERVO_DLG = 11006
id_MODEL_TRACK = 11007
id_MODEL_DEFPOS = 11008
id_SHOW_ROD = 11009


toolBtns = [
            (False, id_MODEL_1, "model1", "Model 1", "Model 1" ),
            (False, id_MODEL_2, "model2", "Model 2", "Model 2" ),
            (False, id_MODEL_UNLOAD, "unloadmodel", "Unload Model", "Unload Model" ),
            (True, id_MODEL_TRACK, "tracking", "Tracking", "Tracking" ),
            (False, id_MODEL_DEFPOS, "defaultpos", "Default Position", "Default Position" ),
            (False, id_SPACE, 10),
            (False, id_SERVO_DLG, "servo", "Servo Manager", "Servo Manager" ),
            (True, id_SHOW_ROD, "showrod", "Rod", "Rod" ),

 ]

class simControlPanel(wx.Panel):
    def __init__(self, parent, id, log, style, sizehint, sidebtn=True, loadbtn=True, cancelbtn=True):
        wx.Panel.__init__(self, parent, id, style=style)

        #self.datapath = os.getcwd()
        self.log = log
        self.sidebtn = sidebtn
        self.model = None

        sh = sizehint[0],100
        #self.nrwins = DEF_NRWINS
        if sidebtn or cancelbtn or loadbtn:
            toolSizer = wx.BoxSizer(wx.VERTICAL)
        else:
            toolSizer = None

        if sidebtn:
            self.toolBtns = []
            for tp in toolBtns:
                if tp[1] == id_SPACE:
                    toolSizer.AddSpacer((1,tp[2]))
                    continue

                if tp[0]:
                    btn = wx.ToggleButton(self, tp[1], tp[3])
                    btn.Bind(wx.EVT_TOGGLEBUTTON, self.onToolIconClick)
                else:
                    btn = wx.Button(self, tp[1], tp[3])
                    btn.Bind(wx.EVT_BUTTON, self.onToolIconClick)
                btn.SetToolTipString(tp[4])

                toolSizer.Add(btn,1,wx.LEFT | wx.RIGHT)
                self.toolBtns.append(btn)

            toolSizer.AddSpacer((1,10))

##        if loadbtn:
##            btn = wx.Button(self, -1, "Load Default")
##            self.Bind(wx.EVT_BUTTON, self.OnLoadDefault, btn)
##            toolSizer.Add(btn,1,wx.LEFT | wx.RIGHT)
##            btn = wx.Button(self, -1, "Load File")
##            self.Bind(wx.EVT_BUTTON, self.OnLoad, btn)
##            toolSizer.Add(btn,1,wx.LEFT | wx.RIGHT)

        if cancelbtn:
            btn = wx.Button(self, wx.ID_CANCEL, "Cancel")
            toolSizer.Add(btn,1,wx.LEFT | wx.RIGHT)

        if sidebtn:
            statusSizer = wx.BoxSizer(wx.VERTICAL)
            self.lblStatus1 = wx.StaticText(self)
            statusSizer.Add(self.lblStatus1,1,wx.LEFT)
            #self.toolBtns.append(self.lblStatus1)
            statusSizer.AddSpacer((1,10))
            self.lblStatus2 = wx.StaticText(self)
            statusSizer.Add(self.lblStatus2,1,wx.LEFT)
            statusSizer.AddSpacer((1,30))
            #self.toolBtns.append(self.lblStatus2)
            toolSizer.AddSpacer((1,5))
            toolSizer.Add(statusSizer, 0)

        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        if toolSizer != None:
            topSizer.Add(toolSizer, 0)

        self.SetAutoLayout(True)
        self.SetSizer(topSizer)

        self.block = False
        self.text = None
        self.Bind(wx.EVT_IDLE, self.onIdle)
        #self.LoadIni()

        # default tracking is on
        btn = self.FindWindowById(id_MODEL_TRACK)
        btn.SetValue(True)

    def __del__(self):
        self.unloadModel()

    def startRecording(self, framerate):
        global gMyWorld
        #defaultname = defaultname + ".jpg"
        #filename = wx.FileSelector("Save as", wildcard="*.jpg",default_path=DEFAULT_IMG_PATH,default_filename=defaultname)
        outavi = "sim.avi"
        sz = (gMyWorld.scenewidth, gMyWorld.sceneheight)
        self.video = myVideo.VideoWriter()
        #framerate = framerate * 125
        framerate = 125 * 30
        self.video.Init(outavi, sz[0], sz[1], framerate)

    def stopRecording(self):
        self.video.Close()

    def recordFrame(self):
        global gMyWorld
        tmpfile = "tmp.jpg"
        mysize = (gMyWorld.scenewidth, gMyWorld.sceneheight)
        #x = gMyWorld.scene.x
        #y = gMyWorld.scene.y
        x = gMyWorld.x
        y = gMyWorld.y
        box = (x,y,x+mysize[0],y+mysize[1])
        img = ImageGrab.grab(box)
        img.save(tmpfile)
        self.video.WriteFrame(tmpfile)

    def onIdle(self, event):
        if not self.block:
            self.block = True
            if self.text != None:
                text = self.text
                self.text = None
                wxcommon.msgbox(self, -1, "Message", text, centerparent=False)
                #wxcommon.msgbox(self, -1, "Message", text)

            #poslist = gMyWorld.arm.ForwardKinematics()
            #pos = poslist[3]
            #msg = "(%0.1f, %0.1f, %0.1f)\n" % (pos[0],pos[1],pos[2])
            #pos = poslist[2]
            #msg = msg + "(%0.1f, %0.1f, %0.1f)\n" % (pos[0],pos[1],pos[2])
            #pos = poslist[1]
            #msg = msg + "(%0.1f, %0.1f, %0.1f)\n" % (pos[0],pos[1],pos[2])
            #self.SetStatusMessage2(msg)
            #self.SetStatusMessage1("(%d,%d, %d, %d)" % (gMyWorld.arm.ComputeStepMotorValue(),gMyWorld.arm.ComputeServoValue(0),gMyWorld.arm.ComputeServoValue(1),gMyWorld.arm.ComputeServoValue(2)))
            self.block = False

    def SetStatusMessage2(self, text):
        self.lblStatus2.SetLabel(text)

    def SetStatusMessage1(self, text):
        self.lblStatus1.SetLabel(text)



    def onToolIconClick(self, event):
        global g_invert
        """ Respond to the user clicking on one of our tool icons.
        """
        id = event.GetEventObject().GetId()
        if id >= id_MODEL_1 and id <= id_MODEL_2:
            self.loadModel(id-id_MODEL_1+1)
        elif id == id_MODEL_UNLOAD:
            self.unloadModel()
        elif id == id_SERVO_DLG:
            self.servoDlg()
        elif id == id_MODEL_TRACK:
            showframe = event.GetEventObject().GetValue()
            self.model.setShowFrame(showframe)
        elif id == id_MODEL_DEFPOS:
            if self.model != None:
                self.model.RestorePosition()
        elif id == id_SHOW_ROD:
            showrod = event.GetEventObject().GetValue()
            if self.model != None:
                self.model.loadRod(showrod)



        event.Skip()

    def servoDlg(self):
        global gMyWorld
        dlg = ServoGridDlg.ServoDetailDlg(self, self.log, -1, "Servo Manager", pos=(600,100), model=self.model)
        dlg.Load(gMyWorld.servomanager)
        dlg.ShowModal()
        dlg.Destroy()

    def unloadModel(self):
        if self.model != None:
            self.model.StopAndWait()
            self.model.unload()
            del self.model
            self.model = None

    def loadModel(self, modelid):
        global gRobotInfo, gMyWorld
        self.unloadModel()
        if modelid == 1:
            self.model = model1.model(self.log, gMyWorld)
            self.model.load()
        elif modelid == 2:
            #self.model = model_servo.model(self.log, gMyWorld)
            self.model = model_gripper.model(self.log, gMyWorld)
            self.model.load()
        gMyWorld.servoManagerFinalize()

        btn = self.FindWindowById(id_MODEL_TRACK)
        self.model.setShowFrame(btn.GetValue())

        self.model.Start()

    def mymsgbox(self, text):
        if not self.block:
            self.block = True
            self.text = text
            self.block = False


class simControlDlg(wx.Dialog):
    def __init__(
            self, parent, log, ID=-1, title="Robot Simulator", sizehint=(800, 600), size=(800, 600), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE
            ):
        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)
        self.log = log
        self.topPanel = simControlPanel(self, -1, self.log, sizehint=sizehint, style=wx.SIMPLE_BORDER)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.topPanel, 1)

##        btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
##        box.Add(btnCancel, 0)
##        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)


        box.SetSizeHints(self)
        self.SetSizer(box)
        #parent.Fit()
        box.Fit(self)
        #self.Fit()

    def OnCancel(self):
        #print "cancel"
        pass

class myApp(wx.App):
    def OnInit(self):
            global gRobotInfo, gMyWorld
            #gRobotInfo = varm.ArmInfo(self)
            gMyWorld =  vworld.vWorld("Simulation", 800, 600, 0, 100)

            dlg = simControlDlg(None, self, sizehint=(200, 800), pos=(800,100))
            #dlg.CenterOnParent()
            dlg.ShowModal()
            #if simanimator.gThreadPool != None:
            #    simanimator.gThreadPool.StopAll()
            dlg.Destroy()
            gMyWorld.quit()
            return True

    def write(self, s):
        print s

def main():
    _app = myApp(0)
    _app.MainLoop()

if __name__ == '__main__':
    main()
