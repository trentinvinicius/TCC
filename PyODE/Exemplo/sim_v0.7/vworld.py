#from visual import *
import visual
import time, math, random
#import ConfigParser
import ode
import numpy
import transformations

# the following parameter affects the stability of PyODE, change them carefully.
ulfactor = 0.1
umfactor = 10

#ulfactor = 1
#umfactor = 1

#ulfactor = 0.1
umfactor = 1


#################################################################################
# helper funcions

def RadianToDegree(rad):
    return rad / visual.pi * 180
def DegreeToRadian(deg):
    return float(deg)/180.0 * visual.pi

def body_translate(body,pos):
    newpos = numpy.array(pos) + numpy.array(body.getPosition())
    body.setPosition(newpos)

def rotate_transforms(*args):
    M = numpy.identity(4, dtype=numpy.float64)

    for a in args:
        #print "a", a
        (angle,axis) = a
        M1 = transformations.rotation_matrix(angle,axis)
        M = numpy.dot(M, M1)
    return M

def rotate_transforms_pt(pt, args):
    M = numpy.identity(4, dtype=numpy.float64)
    for (angle,axis) in args:
        M1 = transformations.rotation_matrix(angle,axis,pt)
        M = numpy.dot(M, M1)
    return M

# get the rotation matrix from a vpython object
def getDCM( renderable):
        z_axis = renderable.axis.cross( renderable.up).norm()
        y_axis = z_axis.cross( renderable.axis).norm()
        x_axis = renderable.axis.norm()
        ret = numpy.empty(3,3)
        #numpy.float
        ret[:,0] = x_axis
        ret[:,1] = y_axis
        ret[:,2] = z_axis
        return ret

# set the rotation matrix for a vpython object
def setDCM( renderable, DCM):
        renderable.axis = visual.vector(DCM[:,0]) * renderable.axis.mag
        renderable.up = visual.vector(DCM[:,1])

def length (vec):
    return math.sqrt (vec[0]**2 + vec[1]**2 + vec[2]**2)

##########################################################
class vObjectBase():
    def __init__(self, parent=None, name=None, composite=False, holder=0, vw=None):
        self.setParent(parent)
        self.composite = composite
        self.holder = holder
        if name == None:
            self.name = self.getDefaultName()
        else:
            self.name = name
        self.vw = vw
        self.virtual = False

    def getAABB(self):
        return self.geom.getAABB()

    def computeMass(self):
        if self.holder == 0 or self.holder == 1:
            m = self.body.getMass()
            pos = self.body.getPosition()
            m.translate(pos)
            return m
        else:
            m = ode.Mass()
            for v in self.vobjlist:
                mv = v.computeMass()
                m.add(mv)
            return m

    def setVirtual(self, virtual):
        self.virtual = virtual

    def setParent(self, parent):
        self.parent = parent

    def setName(self, name):
        self.name = name


    def setStable(self):
        self.body.setForce((0,0,0))
        self.body.setTorque((0,0,0))
        self.body.setLinearVel((0,0,0))
        self.body.setAngularVel((0,0,0))

    def Rotate(self, r):
        pR =  r[0,0], r[0,1], r[0,2], r[1,0], r[1,1], r[1,2], r[2,0], r[2,1], r[2,2]
        self.body.setRotation(pR)

    def RotateMore(self, r):
        R = self.body.getRotation()
        dcm = numpy.array([[R[0],R[1],R[2]],[R[3],R[4],R[5]],[R[6],R[7],R[8]]])
        r3 = numpy.array([[r[0,0], r[0,1], r[0,2]],[ r[1,0], r[1,1], r[1,2]], [r[2,0], r[2,1], r[2,2]]])
        r = numpy.dot(r3,dcm)
        pR =  r[0,0], r[0,1], r[0,2], r[1,0], r[1,1], r[1,2], r[2,0], r[2,1], r[2,2]
        self.body.setRotation(pR)

    def RotateAtPos(self, anglelist, apos):
        pos = numpy.array(self.body.getPosition())
        M = rotate_transforms_pt(apos-pos, anglelist)
        self.RotateMore(M)
        self.Translate((M[0,3],M[1,3],M[2,3]))


    def Translate(self, displace):
        displace = numpy.array(displace)
        pos = numpy.array(self.body.getPosition()) + displace
        self.body.setPosition(pos)

    def translate(self, displace):
        displace = numpy.array(displace)
        #self.frame.pos = numpy.array(self.frame.pos) + displace
        if self.holder != 0:
            for gt in self.gtlist:
                pos = numpy.array(gt.getGeom().getPosition()) + displace
                gt.getGeom().setPosition(pos)
            #for vb in self.vobjlist:
            #    vb.M.translate(displace)
        else:
            pos = numpy.array(self.geom.getPosition()) + displace
            self.geom.setPosition(pos)
        self.M.translate(displace)


    def rotate(self, r):
        pR =  r[0,0], r[0,1], r[0,2], r[1,0], r[1,1], r[1,2], r[2,0], r[2,1], r[2,2]
        if self.holder != 0:
            print "Can not rotate a holder yet"
            die
        else:
            self.geom.setRotation(pR)

        dcm = numpy.array([[pR[0],pR[1],pR[2]],[pR[3],pR[4],pR[5]],[pR[6],pR[7],pR[8]]])
        setDCM(self.frame, dcm)


    def getLongName(self):
        if self.parent == None:
            return self.name
        else:
            return self.parent.getLongName() + "." + self.name

    def worldPosFromLocal(self, lpos):
        r = numpy.array(self.body.getRotation()).reshape(3,3)
        #lpos = self.vc1.geom.getPosition()
        rlpos = numpy.dot(r, lpos)
        pos = numpy.array(self.body.getPosition())
        return rlpos + pos


    def setCollideInfo(self, cat, collide):
        if self.holder == 0:
            #print "setting2", cat, collide
            if self.virtual:
                cat = 0x80000000
                #cat = 0
                collide = 0
            self.geom.setCategoryBits(cat)
            self.geom.setCollideBits(collide)

    def unload(self):
        self.vobj.visible = 0
        #del self.vobj
        #del self.frame
        self.geom.setBody(None)

        #del self.body

    def Save(self):
        self.savepos = self.body.getPosition()
        self.saverotation = self.body.getRotation()

    def Restore(self):
        self.body.setPosition(self.savepos)
        self.body.setRotation(self.saverotation)

    def setGravityMode(self,mode):
        self.body.setGravityMode(mode)

    def setTransparency(self, transparency, exceptlist):
        if self.getDefaultName() in exceptlist:
            return
        if self.holder == 0:
            color = self.vobj.color
            self.vobj.color = (color[0],color[1],color[2],transparency)
        elif self.holder == 1 or self.holder == 2:
            # composite object or composite object
            for v in self.vobjlist:
                v.setTransparency(transparency, exceptlist)
        else:
            print "unknown object"
            exit(1)


# create a box
class vBox(vObjectBase):
    def __init__(self, parent, name, composite, vw, density, lx, ly, lz, color=visual.color.white):
        vObjectBase.__init__(self,parent,name,composite,False,vw)


        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.frame = visual.frame()

        M = ode.Mass()
        M.setBox(density, lx, ly, lz)

        if not composite:
            geom = ode.GeomBox(vw.odespace, lengths=(lx,ly,lz))
            body = ode.Body(vw.odeworld)
            body.setMass(M)

            geom.setBody(body)
            vw.addObject(body, self)
        else:
            geom = ode.GeomBox(None, lengths=(lx,ly,lz))
            body = None

        self.vobj = visual.box(frame=self.frame, length=lx, height=ly, width=lz, color=color)
        self.M = M
        self.geom = geom
        self.body = body

    def getDefaultName(self):
        return "box"

class vCylinder(vObjectBase):
    def __init__(self, parent, name, composite, vw, density, radius, length, color=visual.color.white):
        vObjectBase.__init__(self,parent, name, composite,False,vw)

        self.frame = visual.frame()
        self.radius = radius
        self.length = length

        M = ode.Mass()
        M.setCylinder(density, 3, radius, length)

        if not composite:
            geom = ode.GeomCylinder(vw.odespace, radius=radius, length=length)
            #geom = ode.GeomCapsule(odespace, radius=radius, length=length)
            body = ode.Body(vw.odeworld)
            body.setMass(M)

            geom.setBody(body)
            vw.addObject(body, self)
        else:
            geom = ode.GeomCylinder(None, radius=radius, length=length)
            body = None

        self.vobj = visual.cylinder(frame=self.frame, pos=(0,0,-length/2), axis = (0,0,length), radius = radius, color=color)
        self.M = M
        self.geom = geom
        self.body = body

    def getDefaultName(self):
        return "cylinder"

class vCompositeBase(vObjectBase):
    def __init__(self, parent, name, composite, vw):
        vObjectBase.__init__(self,parent, name, composite,1,vw)
        self.M = ode.Mass()
        self.gtlist = []
        self.vobjlist = []
        self.holderlist = []
        self.frame = visual.frame()
        if not self.composite:
            self.body = ode.Body(self.vw.odeworld)
        else:
            self.body = None

    def getDefaultName(self):
        return "composite"

    def getAABB(self):
        minx = 10000.0
        maxx = -10000.0
        miny = 10000.0
        maxy = -10000.0
        minz = 10000.0
        maxz = -10000.0

        for gt in self.gtlist:
            (minx1, maxx1, miny1, maxy1, minz1, maxz1) = gt.getAABB()
            minx = min(minx, minx1)
            maxx = max(maxx, maxx1)
            miny = min(miny, miny1)
            maxy = max(maxy, maxy1)
            minz = min(minz, minz1)
            maxz = max(maxz, maxz1)
        return (minx, maxx, miny, maxy, minz, maxz)

    def addObject(self, vobj):
        if vobj == None:
            # compute the total mass
            #for vb in self.vobjlist:
            #    print "Mass of ", vb.name, vb.M.mass, vb.M.c
            #    self.M.add(vb.M)
            #print "Mass of ", self.name, vb.M.mass, vb.M.c
            # shift the CG to 0,0,0
            cg = numpy.array(self.M.c)
            for vobj in self.vobjlist:
                geom = vobj.geom
                pos = numpy.array(geom.getPosition()) - cg
                geom.setPosition(pos)
                vobj.frame.pos = pos
            self.M.translate(-cg)

            # create the master object
            if not self.composite:
                self.body.setMass(self.M)
                self.SetBody(self.body)
                for gt in self.gtlist:
                    gt.setBody(self.body)

                self.vw.addObject(self.body, self)
        else:
            self.M.add(vobj.M)
            if vobj.holder:
                # merge their gt into this one
                for gt in vobj.gtlist:
                    self.gtlist.append(gt)
                for vb in vobj.vobjlist:
                    self.vobjlist.append(vb)
                    vb.setParent(self)
                vobj.frame.frame = self.frame
                self.holderlist.append(vobj)

            else:
                #if self.composite:
                #    gt = ode.GeomTransform(None)
                #else:
                #    gt = ode.GeomTransform(self.odespace)
                gt = ode.GeomTransform(self.vw.odespace)
                gt.setGeom(vobj.geom)
                vobj.frame.frame = self.frame
                self.gtlist.append(gt)
                self.vobjlist.append(vobj)
                vobj.setParent(self)

    def unload(self):
        for vb in self.vobjlist:
            vb.unload()
            #del vb
        self.vobjlist = None
        return
        for gt in self.gtlist:
            gt.setBody(None)
            del gt
        self.gtlist = None
        #del self.body

    def SetBody(self, body):
        # recursively set the body variable in the children
        for vb in self.vobjlist:
            vb.body = self.body
        for vb in self.holderlist:
            vb.body = self.body
            vb.SetBody(body)


    def worldPosFromLocal(self, lpos):
        r = numpy.array(self.body.getRotation()).reshape(3,3)
        #lpos = self.vc1.geom.getPosition()
        rlpos = numpy.dot(r, lpos)
        pos = numpy.array(self.body.getPosition())
        return rlpos + pos

    def setCollideInfo(self, cat, collide):
#        for gt in self.gtlist:
#            gt.setCategoryBits(cat)
#            gt.setCollideBits(collide)

#        for vb in self.vobjlist:
#            vb.setCollideInfo(cat, collide)
        for i in range(len(self.vobjlist)):
            vb = self.vobjlist[i]
            vb.setCollideInfo(cat, collide)
            gt = self.gtlist[i]
            gt.setCategoryBits(vb.geom.getCategoryBits())
            gt.setCollideBits(vb.geom.getCollideBits())
            #if vb.virtual:
            #    print "virtual", vb.geom.getCategoryBits()


class vCompoundBase(vObjectBase):
    def __init__(self, parent, name, vw):
        vObjectBase.__init__(self, parent, name, False,2,vw)
        self.vobjlist = []
        self.joinlist = []

        #self.mass = ode.Mass()

    def getDefaultName(self):
        return "compound"

    def getAABB(self):
        minx = 10000.0
        maxx = -10000.0
        miny = 10000.0
        maxy = -10000.0
        minz = 10000.0
        maxz = -10000.0

        for vb in self.vobjlist:
            (minx1, maxx1, miny1, maxy1, minz1, maxz1) = vb.getAABB()
            minx = min(minx, minx1)
            maxx = max(maxx, maxx1)
            miny = min(miny, miny1)
            maxy = max(maxy, maxy1)
            minz = min(minz, minz1)
            maxz = max(maxz, maxz1)
        return (minx, maxx, miny, maxy, minz, maxz)


    def Finalize(self):
        for join in self.joinlist:
            join.setFixed()

    def addObject(self, obj, joint=True):
        obj.setParent(self)
        self.vobjlist.append(obj)
        #return
        if joint and len(self.vobjlist) > 1:
            join = ode.FixedJoint(self.vw.odeworld)
            join.attach(self.vobjlist[0].body, obj.body)
            self.joinlist.append(join)

    def Translate(self, pos):
        pos = numpy.array(pos)
        for vb in self.vobjlist:
            vb.Translate(pos)

    def RotateAtPos(self, anglelist, atpos):
        atpos = numpy.array(atpos)
        for vb in self.vobjlist:
            vb.RotateAtPos(anglelist, atpos)

    def setCollideInfo(self, cat, collide):
        for vb in self.vobjlist:
            #print "setting", cat, collide
            vb.setCollideInfo(cat, collide)

    def unload(self):
        for join in self.joinlist:
            del join
        self.joinlist = None

        for vb in self.vobjlist:
            vb.unload()
            del vb
        self.vobjlist = None

    def Save(self):
        for vb in self.vobjlist:
            vb.Save()

    def Restore(self):
        for vb in self.vobjlist:
            vb.Restore()

    def setGravityMode(self,mode):
        for vb in self.vobjlist:
            vb.setGravityMode(mode)

##########################################################################################################
class cross():
    def __init__(self,color):
        self.ybar = visual.cylinder(axis=(0,1,0), radius=0.1 * ulfactor, color=color)
        self.xbar = visual.cylinder(axis=(1,0,0), radius=0.1 * ulfactor, color=color)
        self.zbar = visual.cylinder(axis=(0,0,1), radius=0.1 * ulfactor, color=color)

    def setPos(self, pos):
        x,y,z=pos
        self.ybar.pos = (x,0,z)
        self.ybar.length = 20  * ulfactor

        self.xbar.pos = (x-10 * ulfactor,y,z)
        self.xbar.length = 20  * ulfactor

        self.zbar.pos = (x,y,z-10 * ulfactor)
        self.zbar.length = 20  * ulfactor

    def setVisible(self, v):
        for o in [self.xbar,self.ybar,self.zbar]:
            o.visible = v

class framebox():
    def __init__(self,color):
        #self.param = (minx, maxx, miny, maxy, minz, maxz)
        self.line1 = visual.box(color=color)
        self.line2 = visual.box(color=color)
        self.line3 = visual.box(color=color)
        self.line4 = visual.box(color=color)
        self.line5 = visual.box(color=color)
        self.line6 = visual.box(color=color)
        self.line7 = visual.box(color=color)
        self.line8 = visual.box(color=color)
        self.line9 = visual.box(color=color)
        self.line10 = visual.box(color=color)
        self.line11 = visual.box(color=color)
        self.line12 = visual.box(color=color)
        self.setParam((0.0, 1.0  * ulfactor, 0.0, 1.0 * ulfactor, 0.0, 1.0 * ulfactor))

    def setVisible(self, v):
        for o in [self.line1,self.line2,self.line3,self.line4,self.line5,self.line6,self.line7,self.line8,self.line9,self.line10,self.line11,self.line12]:
            o.visible = v

    def setParam(self, p):
        (minx, maxx, miny, maxy, minz, maxz) = p
        t = 0.1  * ulfactor
        l = maxx-minx
        h = maxy - miny
        w = maxz - minz
        self.line1.size =((maxx-minx), t, t)
        self.line1.pos = (minx+l/2,miny,minz)
        self.line2.size = (t, t, (maxz-minz))
        self.line2.pos = (maxx,miny,minz+w/2)
        self.line3.size = ((maxx-minx), t, t)
        self.line3.pos = (minx+l/2,miny,maxz)
        self.line4.size = (t, t, (maxz-minz))
        self.line4.pos = (minx,miny,minz+w/2)
        self.line5.size = (t, (maxy-miny), t)
        self.line5.pos = (minx,miny+h/2,minz)
        self.line6.size = (t, (maxy-miny), t)
        self.line6.pos = (maxx,miny+h/2,minz)
        self.line7.size = (t, (maxy-miny), t)
        self.line7.pos = (maxx,miny+h/2,maxz)
        self.line8.size = (t, (maxy-miny), t)
        self.line8.pos = (minx,miny+h/2,maxz)
        self.line9.size =((maxx-minx), t, t)
        self.line9.pos = (minx+l/2,maxy,minz)
        self.line10.size = (t, t, (maxz-minz))
        self.line10.pos = (maxx,maxy,minz+w/2)
        self.line11.size = ((maxx-minx), t, t)
        self.line11.pos = (minx+l/2,maxy,maxz)
        self.line12.size = (t, t, (maxz-minz))
        self.line12.pos = (minx,maxy,minz+w/2)


class mesh_plane():
    def __init__(self, size, nrgrids):
        gridsize=size/nrgrids
        self.frame = visual.frame()
        x = -size
        while x < size:
            z = -size
            while z < size:
                c=visual.curve (frame=self.frame, color=visual.color.white, radius=0.1 * ulfactor)
                c.append(pos=(x,0,z))
                c.append(pos=(x+gridsize,0,z))
                c.append(pos=(x+gridsize,0,z+gridsize))
                c.append(pos=(x,0,z+gridsize))
                c.append(pos=(x,0,z))
                z += gridsize
            x += gridsize


class vServoManager():
    def __init__(self):
        self.servogroups =  {}
        self.servonumber = 0
        self.map = {}
        self.map2 = {}
        self.fhold = False

    def hold(self, fHold):
        self.fhold = fHold

    def addServo(self, servo, group):
        self.servonumber += 1
        servo.setServoNumber(self.servonumber)
        if group in self.servogroups:
            list = self.servogroups[group]
            list.append(servo)

        else:
            self.servogroups[group] = [servo]

    def removeServo(self, servo, group):
        if group in self.servogroups:
            list = self.servogroups[group]
            list.remove(servo)
            #list.append(servo)

    def updateServos(self, dt):
        if not self.fhold:
            for group in self.servogroups:
                list = self.servogroups[group]
                for s in list:
                    s.control(dt)

    def getGroupNames(self):
        return self.servogroups.keys()

    def getServoList(self, group):
        return self.servogroups[group]

    def dumpAll(self):
        for group in self.servogroups:
            list = self.servogroups[group]
            for s in list:
                print s.getLongName(), s.amin, s.amax

    def Finalize(self):
        self.map = {}
        self.map2 = {}
        for group in self.servogroups:
            list = self.servogroups[group]
            for s in list:
                self.map[s.getLongName()] = s
                self.map2[s.servonumber] = s

    def getServo(self, servono):
        if servono in self.map2:
            return self.map2[servono]
        return None


class vWorld():
    def __init__(self, title, width, height, x, y, D3D = False):
        if D3D:
            self.scene = visual.display(title=title, width=width,height=height,x=x,y=y,
                center=(0,0,0), background=(0.1,0.1,0.1), stereo="redblue")
            self.scene.stereodepth = 1
        else:
            self.scene = visual.display(title=title, width=width,height=height,x=x,y=y,
                center=(0,4,0), background=(0.2,0.2,0.2))
        self.scenewidth = width
        self.sceneheight = height
        self.x = x
        self.y = y
        self.D3D = D3D
        #self.scene.center = (10,5,0)
        self.scene.ambient = 0.3

        self.frame = visual.frame()
        self.floor = mesh_plane(50 * ulfactor,5)
        self.floor.frame.frame = self.frame
        #self.floor = visual.box(pos=(0,-50,0),length=500, height=100, width=500, color=(52.0/255,100.0/255,150.0/255))
        #self.floor.frame = self.frame

        #self.center = cylinder(frame=self.frame, pos=(0,0,0), axis = (0,0,0), color=color.red, radius = 0.5)

        self.scene.autoscale = 0
        self.scene.autocenter = 0
        self.scene.range = (20 * ulfactor,20 * ulfactor,20 * ulfactor)
        self.scene.forward = (-0.4,-0.2,-0.9)
        #self.scene.forward = (-0,-0.2,-0)

        odeworld = ode.World()
        self.odeworld = odeworld
        self.g = 10 * ulfactor / 0.01
        #self.g = 10 # a lot of problem if not use a small value
        odeworld.setGravity((0,-self.g,0))
        odeworld.setERP(0.8)
        #odeworld.setERP(0.99)
        odeworld.setCFM(1E-5)
        #odeworld.setCFM(0)
        self.odespace = ode.Space()

        # Create a plane geom which prevent the objects from falling forever
        self.odefloor = ode.GeomPlane(self.odespace, (0,1,0), 0)
        #print self.odefloor.getCategoryBits(), self.odefloor.getCollideBits()
        self.odefloor.setCategoryBits(1)
        self.odefloor.setCollideBits(0)

        self.objectlist = []

        self.servomanager = vServoManager()

    def addObject(self, geom, vObj):
        self.objectlist.append((geom,vObj))

    def updateObjectPos(self):
        for geom,vb in self.objectlist:
                pos = geom.getPosition()
                R = geom.getRotation()
                dcm = numpy.array([[R[0],R[1],R[2]],[R[3],R[4],R[5]],[R[6],R[7],R[8]]])
                vb.frame.pos = pos
                setDCM(vb.frame, dcm)

    def registerServo(self, group, servo):
        self.servomanager.addServo(servo, group)

    def unregisterServo(self, group, servo):
        self.servomanager.removeServo(servo, group)

    def servoManagerFinalize(self):
        self.servomanager.Finalize()

    def updateServos(self, dt):
            self.servomanager.updateServos(dt)

    def defaultSim(self, mtime, dt, fps):
        contactgroup = ode.JointGroup()
        if fps > 0:
            showtime = 1.0/fps
        while (mtime > 0):
            mtime -= dt
            #print mtime,dt
            if fps > 0:
                showtime -= dt
                if showtime <= 0:
                    self.updateObjectPos()
                    visual.rate(fps)
                    showtime = 1.0/fps


            self.odespace.collide((self.odeworld,contactgroup,None), near_callback)
            self.odeworld.step(dt)
            self.updateServos(dt)
            contactgroup.empty()

    def testServos(self, servos, show):
        # before calling this function, it shall move the an empty space and avoid other obstacles around
        # also set gravity to zero

        fps = 100
        dt = 1.0/fps
        if show:
            sfps = 50
        else:
            sfps = 0

        # use 3 secods to move to the default position
        mtime = 3.0
        for servo in servos:
            print "move all to 0"
            for others in servos:
                others.MoveServoLinear(0, mtime)
            self.defaultSim(mtime+0.5, dt, sfps)

            print "move to -90"
            servo.MoveServoLinear(-visual.pi/2, mtime)
            self.defaultSim(mtime+0.5, dt, sfps)
            minangle = servo.getServoAngle()

            print "move to 90"
            servo.MoveServoLinear(visual.pi/2, 2*mtime)
            self.defaultSim(mtime*2+0.5, dt, sfps)
            maxangle = servo.getServoAngle()

            servo.setAngleRange(minangle, maxangle)

        for others in servos:
            others.MoveServoLinear(0, mtime)

        self.defaultSim(mtime+0.1, dt, sfps)

    def quit(self):
        # ver 5.0 seems has no hide function
        #self.scene.hide()
        #self.scene.display = False
        pass

    def __deinit__(self):
        # ver 5.0 seems has no hide function
        #self.scene.hide()
        #self.scene.display = False
        pass

########################################################################################################3
def near_callback(args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """
    #print "Near", geom1.getPosition()
    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    world,contactgroup,otherwise = args
    if otherwise != None and (otherwise.geom == geom1 or otherwise.geom == geom2):
        for c in contacts:
            (pos, normal, depth, geom1, geom2)  = c.getContactGeomParams()
            print "Contact: %0.2f, %0.2f, %0.3f" % pos
            if geom1 == otherwise.geom:
                geom = geom2
            else:
                geom = geom1
            print otherwise.geom.getCategoryBits(), otherwise.geom.getCollideBits()
            print geom.getCategoryBits(), geom.getCollideBits()
            return

    for c in contacts:
        #c.setBounce(0.2)
        c.setBounce(0.2)
        ##c.setMu(5000 * umfactor) # ???
        c.setMu(5000 * umfactor) # ???
        #c.setMu(0 * umfactor) # ???
        ##c.setMu(50000 * umfactor) # ???
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

