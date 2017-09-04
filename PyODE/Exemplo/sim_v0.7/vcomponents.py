import time, random
import ode, numpy
import vworld
import visual
import threading

ulfactor = vworld.ulfactor
umfactor =vworld.umfactor
udfactor = 1.0 / (ulfactor ** 3)  * umfactor
density_alloy = 2.7 * udfactor
density_servo = 1.75 * udfactor
general_thickness = 0.1 * ulfactor

class vHinge1(vworld.vCompositeBase):
    def __init__(self, parent, name, composite, vw, l1=2.5 * ulfactor, l2=5.0 * ulfactor, w = 2.0 * ulfactor):
        vworld.vCompositeBase.__init__(self, parent, name, composite, vw)

        #odeworld = vw.odeworld
        #odespace = vw.odespace
        density = density_alloy
        thickness = general_thickness
        r = w / 2
        self.vbox1 = vworld.vBox(self, "box1", True, vw, density, l1, w, thickness)
        self.addObject(self.vbox1)

        self.vbox2 = vworld.vBox(self, "box2", True, vw, density, l1, w, thickness)
        self.vbox2.translate((0,0,-l2))
        self.addObject(self.vbox2)

        self.vbox3 = vworld.vBox(self, "box3", True, vw, density, thickness, w, l2)
        self.vbox3.translate((l1/2,0,-l2/2))
        self.addObject(self.vbox3)

        vc1 = vworld.vCylinder(self, "vc1", True, vw, density/2, r, thickness)
        vc1.translate((-l1/2,0,0))
        self.addObject(vc1)
        self.vc1 = vc1

        vc2 = vworld.vCylinder(self, "vc2", True, vw, density/2, r, thickness)
        vc2.translate((-l1/2,0,-l2))
        self.addObject(vc2)

        self.addObject(None)

        self.thickness = thickness

    def getDefaultName(self):
        return "Hinge1"

    def getJoint1Location(self):
        #return self.worldPosFromLocal(self.vc1.geom.getPosition())
        (x,y,z) = self.vc1.geom.getPosition()
        return self.worldPosFromLocal((x,y,z-self.thickness/2))

    def getPlate3Location(self):
        #return self.worldPosFromLocal(self.vbox3.geom.getPosition())
        x,y,z=self.vbox3.geom.getPosition()
        return self.worldPosFromLocal((x+self.thickness/2,y,z))


class vServo1(vworld.vCompositeBase):
    def __init__(self, parent, name, composite, vw):
        vworld.vCompositeBase.__init__(self, parent, name, composite, vw)

        sdensity = density_alloy/2
        #density = 1.75
        density = density_servo

        corel = 4 * ulfactor
        edgel = (5.3-4)/2 * ulfactor
        edgew = 0.3 * ulfactor
        h = 2 * ulfactor
        w = 3.8 * ulfactor
        shaft1h = 0.7 * ulfactor
        shaftr = 0.15 * ulfactor
        thickness = 0.1 * ulfactor
        discr = 1.0 * ulfactor

        color1 = (0.6,0.6,0.6)
        self.color1 = color1
        colord = (0.2,0.2,0.2)
        vbox1 = vworld.vBox(self, None, True, vw, density, corel, h, w, color1)
        self.addObject(vbox1)
        self.vbox1 = vbox1
        #self.box1h = h
        #self.box1w = w

        vboxe2 = vworld.vBox(self, None, True, vw, density, edgel, h, edgew, color1)
        vboxe2.translate((corel/2+edgel/2,0,w/2-1 * ulfactor))
        self.addObject(vboxe2)
        self.vboxe2 = vboxe2

        vboxe1 = vworld.vBox(self, None, True, vw, density, edgel, h, edgew, color1)
        vboxe1.translate((-corel/2-edgel/2,0,w/2-1 * ulfactor))
        self.addObject(vboxe1)
        self.vboxe1 = vboxe1

        vshaft1 = vworld.vCylinder(self, None, True, vw, sdensity, shaftr, shaft1h, color1)
        vshaft1.translate((1.0 * ulfactor, 0, w/2+shaft1h/2))
        self.addObject(vshaft1)
        self.vshaft1 = vshaft1
        self.vshaft1.setVirtual(True)


        self.vdisc = vworld.vCylinder(self, None, True, vw, sdensity, discr, thickness, colord)
        self.vdisc.translate((1.0* ulfactor, 0, w/2+shaft1h+thickness/2))
        self.addObject(self.vdisc)
        #baseshaft = cylinder(frame=self.baseframe, pos=(1,0,-3.8/2+0.2), axis = (0,0,4.5), color=self.scolor, radius = 0.5)
        #disc = cylinder(frame=self.baseframe, pos=(1,0,3.8/2+0.5), axis = (0,0,0.2), color=self.color, radius = 1)

        self.addObject(None)
        self.hindgejoint = None

        self.servonumber = 0
        self.angle = 0.0
        self.setAngleRange(-visual.pi/2, visual.pi/2)
        self.dt = 0.0
        self.original = 0.0
        self.t = 1
        self.lock = threading.Semaphore()

    def changeColor(self, color=None):
        if color == None:
            color = self.color1
        self.vbox1.vobj.color = color
        self.vboxe1.vobj.color = color
        self.vboxe2.vobj.color = color

    def setServoNumber(self, servonumber):
        self.servonumber = servonumber

    def getDefaultName(self):
        return "Servo1"

    def getBottomPos(self):
        (x,y,z) = self.vbox1.geom.getPosition()
        y = y - self.box1h/2
        return self.worldPosFromLocal((x,y,z))

    def getCoreBoxPos(self):
        (x,y,z) = self.vbox1.geom.getPosition()
        return self.worldPosFromLocal((x,y,z))


    def getSide1TopPos(self):
        (x,y,z) = self.vboxe1.geom.getPosition()
        z = z + self.vboxe1.lz/2
        return self.worldPosFromLocal((x,y,z))

    def getSide2TopPos(self):
        (x,y,z) = self.vboxe2.geom.getPosition()
        z = z + self.vboxe2.lz/2
        return self.worldPosFromLocal((x,y,z))

    def getDiscPos(self):
        (x,y,z) = self.vdisc.geom.getPosition()
        z += self.vdisc.length/2
        return self.worldPosFromLocal((x,y,z))


    def detach(self):
        if self.hindgejoint != None:
            del self.hindgejoint
            self.hindgejoint = None

    def attach(self, obj, axis = (0.0,0.0,1.0)):
        pos = self.getDiscPos()
        self.hindgejoint = ode.HingeJoint(self.vw.odeworld)
        self.hindgejoint.attach(self.body, obj.body)
        self.hindgejoint.setAnchor(pos)
        self.hindgejoint.setAxis(axis)

        self.angle = self.hindgejoint.getAngle()
        self.targetangle = self.angle
        self.vel = visual.pi/3.0/0.22
        F = 12000 * self.vw.g * umfactor
        #F = F * 10000 / ulfactor
        #F /= 10
        self.hindgejoint.setParam(ode.ParamFMax, F) # 12 kg-g per cm
        self.hindgejoint.setParam(ode.ParamVel, 0)
        self.err = 0

    def Save(self):
        vworld.vCompositeBase.Save(self)
        self.saveangle = self.angle

    def Restore(self):
        vworld.vCompositeBase.Restore(self)
        self.angle = self.saveangle
        self.targetangle = self.angle
        #if self.hindgejoint != None:
        #    self.hindgejoint.Set

    def setAngleRange(self, amin, amax):
        self.amin = amin
        self.amax = amax

    def getServoAngle(self):
        self.lock.acquire()
        angle = self.angle
        self.lock.release()
        return angle

    def MoveServoLinear(self, target, t, delay):
        # delay is ignored in this simulator
        self.lock.acquire()

        self.t = float(t)
        self.dt = 0.0
        self.targetangle = target
        self.original = self.angle
        #self.vel = visual.pi/3.0/0.22
        self.lock.release()

    def control(self, dt):
        if self.hindgejoint == None:
            return
        self.lock.acquire()
        self.angle = self.hindgejoint.getAngle()
        if self.dt >= self.t:
            targetangle = self.targetangle
        else:
            self.dt += dt
            targetangle = (self.targetangle - self.original) * self.dt / self.t + self.original
        err = self.angle - targetangle
        if err > 0:
            v = -self.vel
        else:
            v = self.vel
        err = abs(err)
        #print err, v

        deadband = 0.0
        #cutoff = 0.072
        cutoff = 0.036
        if err <= deadband/1024.0 * visual.pi:
            v = 0
        elif err < cutoff:
            v *= (err) / cutoff / 2
        ##v = v * 100
        ##print "v" , v
        self.hindgejoint.setParam(ode.ParamVel, v)
        self.err = err
        angle = self.angle
        self.lock.release()
        return angle


    def unload(self):
        self.detach()
        vworld.vCompositeBase.unload(self)

##    def controlOld(self):
##        if self.hindgejoint == None:
##            return
##
##        self.angle = self.hindgejoint.getAngle()
##        err = self.angle - self.targetangle
##        #err * self.vel
##
##        if err > 0:
##            v = -self.vel
##        else:
##            v = self.vel
##        #err = abs(err)
##        #if err < 0.018:
##        #    v *= (err) / 0.018
##        #print err
##        self.hindgejoint.setParam(ode.ParamVel, v)
##        return self.angle


class vRCrossServo(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        self.servo1 = vServo1(self, "Servo1", False, vw)
        self.servo2 = vServo1(self, "Servo2", False, vw)

        self.servo1.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))
        self.servo1.RotateAtPos([(visual.pi/2,[.0,1,0.0])], (0,0,0))
        (x1,y1,z1) = self.servo1.vbox1.geom.getPosition()

        #self.servo2.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))
        self.servo2.RotateAtPos([(visual.pi,[.0,1,0.0])], (0,0,0))
        (x2,y2,z2) = self.servo2.vbox1.geom.getPosition()
        self.servo1.Translate((0,y2-y1+self.servo1.vbox1.ly,z2-z1))
        #self.servo1.Translate((x2-x1,y2-y1+self.servo1.vbox1.ly,z2-z1))

        (x1,y1,z1) =  self.servo2.getSide2TopPos()
        (x2,y2,z2) = self.servo1.getCoreBoxPos()
        #self.servo1.Translate((0,0,z1 - z2 - self.servo1.vbox1.lx/2))

        (x1,y1,z1) =  self.servo1.getSide2TopPos()
        (x2,y2,z2) = self.servo2.getCoreBoxPos()
        #self.servo1.Translate((x2 - x1 - self.servo2.vbox1.lx/2, 0, 0))

        self.addObject(self.servo1)
        self.addObject(self.servo2)
        self.Finalize()

    def getDefaultName(self):
        return "vRCrossServo"

class vLCrossServo(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        self.servo1 = vServo1(self, "Servo1", False, vw)
        self.servo2 = vServo1(self, "Servo2", False, vw)

        self.servo1.RotateAtPos([(-visual.pi/2,[0.0,1,0.0])], (0,0,0))
        self.servo2.RotateAtPos([(visual.pi,[1.0,0,0.0])], (0,0,0))
        (x1,y1,z1) = self.servo1.vbox1.geom.getPosition()

        (x2,y2,z2) = self.servo2.vbox1.geom.getPosition()
        #self.servo1.Translate((x2-x1,y2-y1+self.servo1.vbox1.ly,z2-z1))
        self.servo1.Translate((0,y2-y1+self.servo1.vbox1.ly,0))

        (x1,y1,z1) =  self.servo2.getSide2TopPos()
        (x2,y2,z2) = self.servo1.getCoreBoxPos()
        #self.servo1.Translate((0,0,z1 - z2 - self.servo1.vbox1.lx/2))

        (x1,y1,z1) =  self.servo1.getSide1TopPos()
        (x2,y2,z2) = self.servo2.getCoreBoxPos()
        #self.servo1.Translate((x2 - x1 + self.servo2.vbox1.lx/2, 0, 0))

        self.addObject(self.servo1)
        self.addObject(self.servo2)
        self.Finalize()

    def getDefaultName(self):
        return "vLCrossServo"

##class vRCrossServo(vworld.vCompoundBase):
##    def __init__(self, parent, name, vw):
##        vworld.vCompoundBase.__init__(self, parent, name, vw)
##
##        self.servo1 = vServo1(self, "Servo1", False, vw)
##        self.servo2 = vServo1(self, "Servo2", False, vw)
##
##        self.servo1.RotateAtPos([(-visual.pi/2,[.0,1,0.0])], (0,0,0))
##        (x1,y1,z1) = self.servo1.vbox1.geom.getPosition()
##
##        self.servo2.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))
##        (x2,y2,z2) = self.servo2.vbox1.geom.getPosition()
##        self.servo1.Translate((x2-x1,y2-y1+self.servo1.vbox1.ly,z2-z1))
##
##        (x1,y1,z1) =  self.servo2.getSide2TopPos()
##        (x2,y2,z2) = self.servo1.getCoreBoxPos()
##        self.servo1.Translate((0,0,z1 - z2 - self.servo1.vbox1.lx/2))
##
##        (x1,y1,z1) =  self.servo1.getSide2TopPos()
##        (x2,y2,z2) = self.servo2.getCoreBoxPos()
##        self.servo1.Translate((x2 - x1 - self.servo2.vbox1.lx/2, 0, 0))
##
##        self.addObject(self.servo1)
##        self.addObject(self.servo2)
##        self.Finalize()
##
##    def getDefaultName(self):
##        return "vRCrossServo"

##class vLCrossServo(vworld.vCompoundBase):
##    def __init__(self, parent, name, vw):
##        vworld.vCompoundBase.__init__(self, parent, name, vw)
##
##        self.servo1 = vServo1(self, "Servo1", False, vw)
##        self.servo2 = vServo1(self, "Servo2", False, vw)
##
##        self.servo1.RotateAtPos([(visual.pi,[0.0,0,1.0]),(-visual.pi/2,[.0,1,0.0])], (0,0,0))
##        (x1,y1,z1) = self.servo1.vbox1.geom.getPosition()
##
##        (x2,y2,z2) = self.servo2.vbox1.geom.getPosition()
##        self.servo1.Translate((x2-x1,y2-y1+self.servo1.vbox1.ly,z2-z1))
##
##        (x1,y1,z1) =  self.servo2.getSide2TopPos()
##        (x2,y2,z2) = self.servo1.getCoreBoxPos()
##        self.servo1.Translate((0,0,z1 - z2 - self.servo1.vbox1.lx/2))
##
##        (x1,y1,z1) =  self.servo1.getSide1TopPos()
##        (x2,y2,z2) = self.servo2.getCoreBoxPos()
##        self.servo1.Translate((x2 - x1 + self.servo2.vbox1.lx/2, 0, 0))
##
##        self.addObject(self.servo1)
##        self.addObject(self.servo2)
##        self.Finalize()
##
##    def getDefaultName(self):
##        return "vLCrossServo"
