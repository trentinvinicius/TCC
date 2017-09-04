import ode, numpy
import vworld
import visual
from vcomponents import *

# foot object is a flat plate with a servo on top
class vFootBase(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        thickness = general_thickness
        w = 6.0 * ulfactor
        l = 8.0 * ulfactor

        self.hinge = vHinge1(self, None, False, vw, 2.5* ulfactor, 5.0* ulfactor)
        # rotate and translate
        self.hinge.RotateAtPos([(-visual.pi/2,[0.0,0,1.0])], (0,0,0))
        # rotate anothor 180 to match new model
        self.hinge.RotateAtPos([(visual.pi,[0.0,1,0.0])], (0,0,0))

        x,y,z = self.hinge.getPlate3Location()
        #print x,y,z
        #self.hinge.Translate((-x,-y,-z))
        self.hinge.Translate((-x,-y,-z))

        density = density_alloy
        x,y,z = (w,thickness,l)
        vb = vworld.vBox(self, None, False, vw, density, x,y,z)
        vb.translate((0, -vb.ly/2, 0))
        #vb.translate((0, 0, 0))

        self.addObject(self.hinge)
        self.addObject(vb)


        self.footplate = vb
        self.thickness = thickness

    def getDefaultName(self):
        return "FootBase"

    def getBottomPos(self):
        #(x,y,z) = self.footplate.geom.getPosition()
        #return self.footplate.worldPosFromLocal((0,y-self.footplate.ly/2,0))
        return self.footplate.worldPosFromLocal((0,-self.footplate.ly/2,0))


    def getJoint1Location(self):
        #print "r", self.hinge.geom.getRotation()
        x,y,z = self.hinge.getJoint1Location()
        return (x,y,z-self.hinge.thickness/2)
        #return self.hinge.worldPosFromLocal((x,y,z-self.hinge.thickness/2))

class vRightFoot(vFootBase):
    def __init__(self, parent, name, vw):
        vFootBase.__init__(self, parent, name, vw)

        self.hinge.Translate((-0.8* ulfactor,0,0))
        self.Finalize()

    def getDefaultName(self):
        return "RightFoot"

class vLeftFoot(vFootBase):
    def __init__(self, parent, name, vw):
        vFootBase.__init__(self, parent, name, vw)

        self.hinge.Translate((0.8* ulfactor,0,0))
        self.Finalize()

    def getDefaultName(self):
        return "LeftFoot"
###################################################################################
class vRKnee(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)
        self.hinge = vHinge1(self, None, False, vw, 2.5* ulfactor, 5.0* ulfactor)

        ## roate the hinge to match the new model
        self.hinge.RotateAtPos([(visual.pi,(1,0,0))],(0,0,0))
        ##
        x1,y1,z1 = self.hinge.getPlate3Location()

        self.servo = vServo1(self, None, False, vw)
        x2,y2,z2 = self.servo.vboxe1.geom.getPosition()
        x2 -= self.servo.vboxe1.lx/2
        self.servo.Translate((x1-x2,0,0))

        discpos = self.servo.getDiscPos()
        j1pos = self.hinge.getJoint1Location()
        ## no need to move in the new model
        #self.servo.Translate((0,0,j1pos[2]-discpos[2]))

        ## translate more to reflect the new model
        self.servo.Translate((0.4 * ulfactor,0,0))
        ##
        #discpos = self.servo.getDiscPos()
        #print j1pos,discpos

        self.addObject(self.hinge)
        self.addObject(self.servo)

        self.Finalize()
        self.RotateAtPos([(visual.pi/2,(0,0,1)), (-visual.pi/2,(1,0,0))],(0,0,0))

    def getDefaultName(self):
        return "RKnee"

class vLKnee(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)
        self.hinge = vHinge1(self, None, False, vw, 2.5* ulfactor, 5.0* ulfactor)
        ## roate the hinge to match the new model
        self.hinge.RotateAtPos([(visual.pi,(1,0,0))],(0,0,0))
        ##
        x1,y1,z1 = self.hinge.getPlate3Location()

        self.servo = vServo1(self, None, False, vw)
        x2,y2,z2 = self.servo.vboxe1.geom.getPosition()
        x2 -= self.servo.vboxe1.lx/2
        self.servo.Translate((x1-x2,0,0))

        discpos = self.servo.getDiscPos()
        j1pos = self.hinge.getJoint1Location()
        #self.servo.Translate((0,0,j1pos[2]-discpos[2]))

        ## translate more to reflect the new model
        self.servo.Translate((0.4 * ulfactor,0,0))
        ##
        self.addObject(self.hinge)
        self.addObject(self.servo)

        self.Finalize()
        self.RotateAtPos([(visual.pi/2,(0,0,1)), (visual.pi/2,(1,0,0))],(0,0,0))

    def getDefaultName(self):
        return "LKnee"

########################################################################
class vThigh(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)


        #self.hinge1 = vHinge1(self, "Hinge1", False, vw, 2.5* ulfactor, 5.0* ulfactor)
        #self.hinge2 = vHinge1(self, "Hinge2", False, vw, 4.5* ulfactor, 5.0* ulfactor)
        self.hinge1 = vHinge1(self, "Hinge1", False, vw, 3.3* ulfactor, 5.0* ulfactor)
        self.hinge2 = vHinge1(self, "Hinge2", False, vw, 3.3* ulfactor, 5.0* ulfactor)
        # rotate and translate

        self.hinge2.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))
        self.hinge2.RotateAtPos([(visual.pi,[1.0,0,0.0])], (0,0,0))

        x1,y1,z1 = self.hinge1.getPlate3Location()
        x2,y2,z2 = self.hinge2.getPlate3Location()
        #print x,y,z
        self.hinge2.Translate((x1-x2,y1-y2,z1-z2))

        self.addObject(self.hinge1)
        self.addObject(self.hinge2)

        self.Translate((0,5* ulfactor,0))
        self.Finalize()

        self.RotateAtPos([(visual.pi/2,(0,0,1)), (-visual.pi/2,(1,0,0))],(0,0,0))
        #print self.hinge1.getJoint1Location(),self.hinge2.getJoint1Location()

    def getDefaultName(self):
        return "Thigh"

#################################################################################
class vRUhip(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)
        self.servo = vServo1(self, "Servo", False, vw)
        self.servo.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))

        self.hinge = vHinge1(self, "hinde", False, vw, 1.5* ulfactor)
        self.hinge.RotateAtPos([(-visual.pi/2,[0.0,0,1.0])], (0,0,0))


        discpos = self.servo.getDiscPos()
        j1pos = self.hinge.getJoint1Location()

        self.hinge.Translate(discpos - j1pos)

        self.addObject(self.servo,False)
        self.addObject(self.hinge,False)
        #self.Finalize()

        self.servo.attach(self.hinge,(0,0,1))

    def getDefaultName(self):
        return "vRUhip"


class vLUhip(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)
        self.servo = vServo1(self, "Servo", False, vw)

        self.hinge = vHinge1(self, "hinde", False, vw, 1.5* ulfactor)
        self.hinge.RotateAtPos([(-visual.pi/2,[0.0,0,1.0])], (0,0,0))
        #self.hinge.RotateAtPos([(visual.pi,[0.0,1,0.0])], (0,0,0))


        discpos = self.servo.getDiscPos()
        j1pos = self.hinge.getJoint1Location()

        self.hinge.Translate(discpos - j1pos)

        self.addObject(self.servo,False)
        self.addObject(self.hinge,False)
        #self.Finalize()

        self.servo.attach(self.hinge,(0,0,1))

    def getDefaultName(self):
        return "vLUhip"

#################################################################################
# vRhip looks like a vRCrossServo
class vRhip(vRCrossServo):
    def __init__(self, parent, name, vw):
        vRCrossServo.__init__(self, parent, name, vw)

        self.RotateAtPos([(visual.pi/2,[1,0,0.0])], (0,0,0))
        #self.RotateAtPos([(-visual.pi/2,[0,1.,.0])], (0,0,0))

    def getDefaultName(self):
        return "vRhip"

# vLhip looks like a vLCrossServo
class vLhip(vLCrossServo):
    def __init__(self, parent, name, vw):
        vLCrossServo.__init__(self, parent, name, vw)

        self.RotateAtPos([(visual.pi/2,[1,0,0.0])], (0,0,0))
        #self.RotateAtPos([(-visual.pi/2,[0,1.,.0])], (0,0,0))

    def getDefaultName(self):
        return "vLhip"

### vRhip looks like a vLCrossServo
##class vRhip(vworld.vCompoundBase):
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
##
##        (ex1,ey1,ez1) =  self.servo1.vboxe2.geom.getPosition()
##
##        xd1 = x1 + self.servo1.vbox1.lz / 2 - ex1
##        #print xd1
##        xd = x2+self.servo2.vbox1.lx/2-x1-self.servo1.vbox1.lz/2 - xd1
##        yd = y2-y1+self.servo1.vbox1.ly
##        zd = z2+self.servo2.vbox1.lz/2-z1-self.servo1.vbox1.lx/2
##        self.servo1.Translate((xd,yd,zd))
##
##
##        #self.testbox = vworld.vBox(self, "testbox", False, vw, 100, 1,1,1)
##        #x,y,z = self.servo1.body.getPosition()
##        #self.testbox.Translate((x,y-5,z))
##        #self.addObject(self.testbox)
##
##        self.addObject(self.servo1)
##        self.addObject(self.servo2)
##        self.Finalize()
##
##        self.RotateAtPos([(visual.pi/2,[0,0,1.0])], (0,0,0))
##        self.RotateAtPos([(-visual.pi/2,[0,1.,.0])], (0,0,0))
##
##    def getDefaultName(self):
##        return "vRhip"

### vLhip looks like a vRCrossServo
##class vLhip(vworld.vCompoundBase):
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
##
##        (ex1,ey1,ez1) =  self.servo1.vboxe1.geom.getPosition()
##
##        xd1 = x1 - self.servo1.vbox1.lz / 2 - ex1
##        xd1 = x1 - self.servo1.vbox1.lz / 2 - ex1 + 0.2 * ulfactor # don't know where this o.2 coming from....just a quick fix
##        #print xd1
##        xd = x2+self.servo2.vbox1.lx/2-x1-self.servo1.vbox1.lz/2 - xd1
##        yd = y2-y1+self.servo1.vbox1.ly
##        zd = z2+self.servo2.vbox1.lz/2-z1-self.servo1.vbox1.lx/2
##        self.servo1.Translate((xd,yd,zd))
##
##
##        self.addObject(self.servo1)
##        self.addObject(self.servo2)
##        self.Finalize()
##
##        self.RotateAtPos([(-visual.pi/2,[0,0,1.0])], (0,0,0))
##        self.RotateAtPos([(visual.pi/2,[0,1.,.0])], (0,0,0))
##
##    def getDefaultName(self):
##        return "vLhip"
##

#################################################################################
class vRightLeg(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        self.vhip = vRhip(self, "vRhip", vw)
        self.addObject(self.vhip, False)

        self.vThigh = vThigh(self, "vThigh", vw)
        self.addObject(self.vThigh, False)

        self.vKnee = vRKnee(self, "vRKnee", vw)
        self.addObject(self.vKnee, False)

        self.vFoot = vRightFoot(self, "vRF", vw)
        self.addObject(self.vFoot, False)

        (x,y,z) = self.vFoot.getBottomPos()
        #self.vFoot.Translate((0,-y+0.1* ulfactor,0))
        self.vFoot.Translate((0,-y,0))
        j1pos = self.vFoot.getJoint1Location()

        self.vAnkle = vRCrossServo(self, "vRAnkle", vw)
        self.addObject(self.vAnkle, False)

        discpos = self.vAnkle.servo2.getDiscPos()
        self.vAnkle.Translate(j1pos-discpos)
        self.vAnkle.servo2.attach(self.vFoot.hinge)

        j1pos = self.vKnee.hinge.getJoint1Location()
        discpos = self.vAnkle.servo1.getDiscPos()
        self.vKnee.Translate(discpos-j1pos)
        self.vAnkle.servo1.attach(self.vKnee.hinge, (1,0,0))


        j1pos = self.vThigh.hinge1.getJoint1Location()
        discpos = self.vKnee.servo.getDiscPos()
        self.vThigh.Translate(discpos-j1pos)
        self.vKnee.servo.attach(self.vThigh.hinge1,(1,0,0))

        j1pos = self.vThigh.hinge2.getJoint1Location()
        discpos = self.vhip.servo1.getDiscPos()
        self.vhip.Translate(j1pos-discpos)
        self.vhip.servo1.attach(self.vThigh.hinge2,(1,0,0))


        for servo in [
            self.vhip.servo1,
            self.vhip.servo2,
            self.vKnee.servo,
            self.vAnkle.servo1,
            self.vAnkle.servo2]:
            vw.registerServo(self.name, servo)

    def getDefaultName(self):
        return "RightLeg"


##class vRightLegOld(vworld.vCompoundBase):
##    def __init__(self, parent, name, vw):
##        vworld.vCompoundBase.__init__(self, parent, name, vw)
##
###        self.vUhip = vRUhip(self, "vRUhip", vw)
###        self.addObject(self.vUhip, False)
##
##        self.vhip = vRhip(self, "vRhip", vw)
##        self.addObject(self.vhip, False)
##
##        self.vThigh = vThigh(self, "vThigh", vw)
##        self.addObject(self.vThigh, False)
##
##        self.vKnee = vRKnee(self, "vRKnee", vw)
##        self.addObject(self.vKnee, False)
##
##        self.vFoot = vRightFoot(self, "vRF", vw)
##        self.addObject(self.vFoot, False)
##
##        (x,y,z) = self.vFoot.getBottomPos()
##        #self.vFoot.Translate((0,-y+0.1* ulfactor,0))
##        self.vFoot.Translate((0,-y,0))
##        j1pos = self.vFoot.getJoint1Location()
##
##
##        self.vAnkle = vRCrossServo(self, "vRAnkle", vw)
##        self.addObject(self.vAnkle, False)
##
##        discpos = self.vAnkle.servo2.getDiscPos()
##        self.vAnkle.Translate(j1pos-discpos)
##        self.vAnkle.servo2.attach(self.vFoot.hinge)
##
##        j1pos = self.vKnee.hinge.getJoint1Location()
##        discpos = self.vAnkle.servo1.getDiscPos()
##        self.vKnee.Translate(discpos-j1pos)
##        self.vAnkle.servo1.attach(self.vKnee.hinge, (1,0,0))
##
##
##        j1pos = self.vThigh.hinge1.getJoint1Location()
##        discpos = self.vKnee.servo.getDiscPos()
##        self.vThigh.Translate(discpos-j1pos)
##        self.vKnee.servo.attach(self.vThigh.hinge1,(1,0,0))
##
##        j1pos = self.vThigh.hinge2.getJoint1Location()
##        discpos = self.vhip.servo2.getDiscPos()
##        self.vhip.Translate(j1pos-discpos)
##        self.vhip.servo2.attach(self.vThigh.hinge2,(1,0,0))
##
###        j3pos = self.vUhip.hinge.getPlate3Location()
###        discpos = self.vhip.servo1.getDiscPos()
###        self.vUhip.Translate(discpos-j3pos)
###        self.vhip.servo1.attach(self.vUhip.hinge,(0,1,0))
##
##        for servo in [
###            self.vUhip.servo,
##            self.vhip.servo1,
##            self.vhip.servo2,
##            self.vKnee.servo,
##            self.vAnkle.servo1,
##            self.vAnkle.servo2]:
##            vw.registerServo(self.name, servo)
##
##    def getDefaultName(self):
##        return "RightLeg"
##

class vLeftLeg(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        self.vhip = vLhip(self, "vLhip", vw)
        self.addObject(self.vhip, False)

        self.vThigh = vThigh(self, "vThigh", vw)
        self.vThigh.RotateAtPos([(visual.pi,(0,1,0))], (0,0,0))
        self.addObject(self.vThigh, False)

        self.vKnee = vLKnee(self, "vLKnee", vw)
        self.addObject(self.vKnee, False)

        self.vFoot = vLeftFoot(self, "vLF", vw)
        self.addObject(self.vFoot, False)

        (x,y,z) = self.vFoot.getBottomPos()
        #self.vFoot.Translate((0,-y+0.1* ulfactor,0))
        self.vFoot.Translate((0,-y,0))
        j1pos = self.vFoot.getJoint1Location()

        self.vAnkle = vLCrossServo(self, "vLAnkle", vw)
        self.addObject(self.vAnkle, False)

        discpos = self.vAnkle.servo2.getDiscPos()
        self.vAnkle.Translate(j1pos-discpos)
        self.vAnkle.servo2.attach(self.vFoot.hinge)

        j1pos = self.vKnee.hinge.getJoint1Location()
        discpos = self.vAnkle.servo1.getDiscPos()
        self.vKnee.Translate(discpos-j1pos)
        self.vAnkle.servo1.attach(self.vKnee.hinge, (1,0,0))


        j1pos = self.vThigh.hinge1.getJoint1Location()
        discpos = self.vKnee.servo.getDiscPos()
        self.vThigh.Translate(discpos-j1pos)
        self.vKnee.servo.attach(self.vThigh.hinge1,(1,0,0))

        j1pos = self.vThigh.hinge2.getJoint1Location()
        discpos = self.vhip.servo1.getDiscPos()
        self.vhip.Translate(j1pos-discpos)
        self.vhip.servo1.attach(self.vThigh.hinge2,(1,0,0))

        for servo in [
            #self.vUhip.servo,
            self.vhip.servo1,
            self.vhip.servo2,
            self.vKnee.servo,
            self.vAnkle.servo1,
            self.vAnkle.servo2]:
            vw.registerServo(self.name, servo)

    def getDefaultName(self):
        return "LeftLeg"

##class vLeftLegOld(vworld.vCompoundBase):
##    def __init__(self, parent, name, vw):
##        vworld.vCompoundBase.__init__(self, parent, name, vw)
##
###        self.vUhip = vLUhip(self, "vLUhip", vw)
###        self.addObject(self.vUhip, False)
##
##        self.vhip = vLhip(self, "vLhip", vw)
##        self.addObject(self.vhip, False)
##
##        self.vThigh = vThigh(self, "vThigh", vw)
##        self.vThigh.RotateAtPos([(visual.pi,(0,1,0))], (0,0,0))
##        self.addObject(self.vThigh, False)
##
##        self.vKnee = vLKnee(self, "vLKnee", vw)
##        self.addObject(self.vKnee, False)
##
##        self.vFoot = vLeftFoot(self, "vLF", vw)
##        self.addObject(self.vFoot, False)
##
##        (x,y,z) = self.vFoot.getBottomPos()
##        #self.vFoot.Translate((0,-y+0.1* ulfactor,0))
##        self.vFoot.Translate((0,-y,0))
##        j1pos = self.vFoot.getJoint1Location()
##
##
##        self.vAnkle = vLCrossServo(self, "vLAnkle", vw)
##        self.addObject(self.vAnkle, False)
##
##        discpos = self.vAnkle.servo2.getDiscPos()
##        self.vAnkle.Translate(j1pos-discpos)
##        self.vAnkle.servo2.attach(self.vFoot.hinge)
##
##        j1pos = self.vKnee.hinge.getJoint1Location()
##        discpos = self.vAnkle.servo1.getDiscPos()
##        self.vKnee.Translate(discpos-j1pos)
##        self.vAnkle.servo1.attach(self.vKnee.hinge, (1,0,0))
##
##
##        j1pos = self.vThigh.hinge1.getJoint1Location()
##        discpos = self.vKnee.servo.getDiscPos()
##        self.vThigh.Translate(discpos-j1pos)
##        self.vKnee.servo.attach(self.vThigh.hinge1,(1,0,0))
##
##        j1pos = self.vThigh.hinge2.getJoint1Location()
##        discpos = self.vhip.servo2.getDiscPos()
##        self.vhip.Translate(j1pos-discpos)
##        self.vhip.servo2.attach(self.vThigh.hinge2,(1,0,0))
##
###        j3pos = self.vUhip.hinge.getPlate3Location()
###        discpos = self.vhip.servo1.getDiscPos()
###        self.vUhip.Translate(discpos-j3pos)
###        self.vhip.servo1.attach(self.vUhip.hinge,(0,1,0))
##
##        for servo in [
##            #self.vUhip.servo,
##            self.vhip.servo1,
##            self.vhip.servo2,
##            self.vKnee.servo,
##            self.vAnkle.servo1,
##            self.vAnkle.servo2]:
##            vw.registerServo(self.name, servo)
##
##    def getDefaultName(self):
##        return "LeftLeg"

########################################################################
class vHip(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        self.bottom = vworld.vBox(self, None, False, vw, density_alloy, 4 * ulfactor, general_thickness, 4 * ulfactor)

        self.vURhipServo = vServo1(self, "URServo", False, vw)
        self.vURhipServo.RotateAtPos([(visual.pi,[0.0,0,1.0])], (0,0,0))
        self.vURhinge = vHinge1(self, "URhinde", False, vw, 1.5* ulfactor)
        self.vURhinge.RotateAtPos([(-visual.pi/2,[0.0,0,1.0])], (0,0,0))


        self.vULhipServo = vServo1(self, "ULServo", False, vw)
        self.vULhinge = vHinge1(self, "ULhinde", False, vw, 1.5* ulfactor)
        self.vULhinge.RotateAtPos([(-visual.pi/2,[0.0,0,1.0])], (0,0,0))

        # move the servos
        servo = self.vURhipServo
        (xs,ys,zs) = servo.getCoreBoxPos()
        ys -= servo.vbox1.ly/2
        xs += servo.vbox1.lx/2
        self.vURhipServo.Translate((-self.bottom.lx/2-xs, -ys+self.bottom.ly/2, -zs))

        servo = self.vULhipServo
        (xs,ys,zs) = servo.getCoreBoxPos()
        ys -= servo.vbox1.ly/2
        xs -= servo.vbox1.lx/2
        self.vULhipServo.Translate((self.bottom.lx/2-xs, -ys+self.bottom.ly/2, -zs))

        # fix them
        self.addObject(self.vURhipServo, True)
        self.addObject(self.vULhipServo, True)
        self.addObject(self.bottom, True)
        self.Finalize()


        # set up the R hinge
        discpos = self.vURhipServo.getDiscPos()
        j1pos = self.vURhinge.getJoint1Location()
        self.vURhinge.Translate(discpos - j1pos)
        self.vURhipServo.attach(self.vURhinge,(0,0,1))


        # set up the L hinge
        discpos = self.vULhipServo.getDiscPos()
        j1pos = self.vULhinge.getJoint1Location()
        self.vULhinge.Translate(discpos - j1pos)
        self.vULhipServo.attach(self.vULhinge,(0,0,1))


        vw.registerServo(self.name, self.vULhipServo)
        vw.registerServo(self.name, self.vURhipServo)

        #print self.vURhipServo.getDiscPos(),self.vULhipServo.getDiscPos()

    def getDefaultName(self):
        return "vHip"

class vLBody(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)


        self.vLLeg = vLeftLeg(self, "vLLeg", vw)
        self.vRLeg = vRightLeg(self, "vRLeg", vw)
        self.vhip = vHip(self, "vHip", vw)

        j3pos = self.vhip.vURhinge.getPlate3Location()
        discpos = self.vRLeg.vhip.servo2.getDiscPos()
#        self.vhip.Translate(discpos - j3pos)
        self.vRLeg.Translate(j3pos - discpos)
        self.vRLeg.Translate((0,-0.5*ulfactor,-0.5*ulfactor))

        self.vRLeg.vhip.servo2.attach(self.vhip.vURhinge,(0,1,0))

        j3pos = self.vhip.vULhinge.getPlate3Location()
        discpos = self.vLLeg.vhip.servo2.getDiscPos()
        self.vLLeg.Translate(j3pos - discpos)
        self.vLLeg.Translate((0,-0.5*ulfactor,-0.5*ulfactor))
        self.vLLeg.vhip.servo2.attach(self.vhip.vULhinge,(0,1,0))


        self.addObject(self.vhip, False)
        self.addObject(self.vLLeg, False)
        self.addObject(self.vRLeg, False)
        self.addObject(self.vhip.vURhinge, False)
        self.addObject(self.vhip.vULhinge, False)

        (x,y,z) = self.vRLeg.vFoot.getBottomPos()
        pos = (0,-y+0.3*ulfactor, -z)
        #pos = (0,-y, -z)
        #print pos
        self.Translate(pos)

        #print self.vRLeg.vFoot.getBottomPos(), self.vLLeg.vFoot.getBottomPos()
        #print self.vRLeg.vFoot.hinge.getPlate3Location(),self.vLLeg.vFoot.hinge.getPlate3Location()
        #print self.vhip.vURhipServo.getDiscPos()
        #print self.vhip.vULhipServo.getDiscPos()
    def getDefaultName(self):
        return "LBody"



