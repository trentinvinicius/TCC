import ode, numpy, math
import vworld
import visual
from vcomponents import *

class vGripperBase(vworld.vCompoundBase):

    def Fixing(self,body1,body2):
        join1 = ode.FixedJoint(self.vw.odeworld)
        join1.attach(body1,body2)
        join1.setFixed()
        self.fixjoints.append(join1)

    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)
        self.fixjoints = []

        thickness = general_thickness
        w1 = 5.0 * ulfactor
        #w1 = 4.0 * ulfactor
        w2 = 1.5 * ulfactor
        #w2 = 2.0 * ulfactor
        l1 = 3.0 * ulfactor
        l2 = 1.0 * ulfactor
        l3 = 3.0 * ulfactor
        lf = 4.0 * ulfactor
        tf = 1.5 * ulfactor

        #t1 = 0.5 * ulfactor
        t1 = 1.0 * ulfactor
        #tail = 1.0 * ulfactor
        tail = 2.5 * ulfactor
        #tail = 2.0 * ulfactor
        edge = 0.3 * ulfactor
        boltradius = 0.15 * ulfactor
        delta = thickness / 2
        colorb = visual.color.blue

        density = density_alloy
        x = l1
        z = t1
        y = thickness
        fr = vworld.vBox(self, None, False, vw, density, lf,tf,thickness)
        fl = vworld.vBox(self, None, False, vw, density, lf,tf,thickness)

        qr = vworld.vBox(self, None, False, vw, density, x+tail+2*edge,y,z)
        pr = vworld.vBox(self, None, False, vw, density, x+2*edge,y,z)
        pl = vworld.vBox(self, None, False, vw, density, x+2*edge,y,z)
        ql = vworld.vBox(self, None, False, vw, density, x+tail+2*edge,y,z)
        qr.Translate(((l1+tail)/2,0,(w1/2+ w2)))
        ql.Translate(((l1+tail)/2,0,-(w1/2+ w2)))
        x = tail + l2 + l1/2
        pl.Translate((x,0,-w1/2))
        pr.Translate((x,0,w1/2))

        x = t1
        z = l3
        y = thickness
        rl = vworld.vBox(self, None, False, vw, density, x,y,z+2*edge)
        angle1 = math.atan(l2/w2)
        rl.Translate((0,0,rl.lz/2))
        rl.RotateAtPos([(-angle1,(0,-1,0))], (0,0,0))
        rl.Translate((l1+tail,-thickness-delta,-(w1/2+w2)))

        rr = vworld.vBox(self, None, False, vw, density, x,y,z+2*edge)
        rr.Translate((0,0,-rr.lz/2))
        rr.RotateAtPos([(-angle1,(0,1,0))], (0,0,0))
        rr.Translate(((l1+tail),-thickness-delta,(w1/2+w2)))

        fl.Translate((lf/2+l2+tail+l1/2,0,-w2/2))
        fr.Translate((lf/2+l2+tail+l1/2,0,w2/2))
        if True:
             # setup the hinge joint for rr and qr
            (x,y,z) = qr.body.getPosition()
            #print (x,y,z)
            x += (l1 + tail)/2
            bolt1 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt1.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt1.Translate((x,thickness * 1.2,z))
            self.Fixing(bolt1.body, qr.body)

            hinge1 = ode.HingeJoint(self.vw.odeworld)
            hinge1.attach(qr.body, rr.body)
            hinge1.setAnchor((x,y,z))
            hinge1.setAxis((0,1,0))
            self.hinge1 = hinge1

            # setup the hinge joint for pr and rr
            (x,y,z) = pr.body.getPosition()
            x += (l1)/2
            bolt2 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt2.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt2.Translate((x,thickness * 1.2,z))
            self.Fixing(bolt2.body, pr.body)

            hinge2 = ode.HingeJoint(self.vw.odeworld)
            hinge2.attach(pr.body, rr.body)
            hinge2.setAnchor((x,y,z))
            hinge2.setAxis((0,1,0))
            self.hinge2 = hinge2

            # setup the hinge joint for pl and rl
            (x,y,z) = pl.body.getPosition()
            x += (l1)/2
            bolt3 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt3.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt3.Translate((x,thickness*1.2,z))
            self.Fixing(bolt3.body, pl.body)

            hinge3 = ode.HingeJoint(self.vw.odeworld)
            hinge3.attach(pl.body, rl.body)
            hinge3.setAnchor((x,y,z))
            hinge3.setAxis((0,1,0))
            self.hinge3 = hinge3

            # setup the hinge joint for ql and rl
            (x,y,z) = ql.body.getPosition()
            x += (l1+tail)/2
            bolt4 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt4.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt4.Translate((x,thickness*1.2,z))
            self.Fixing(bolt4.body, ql.body)

            hinge4 = ode.HingeJoint(self.vw.odeworld)
            hinge4.attach(ql.body, rl.body)
            hinge4.setAnchor((x,y,z))
            hinge4.setAxis((0,1,0))
            self.hinge4 = hinge4


        coreplate = vworld.vBox(self, None, False, vw, density, l2+tail+2*edge,thickness,w1+w2*2+2*edge, color=visual.color.red)
        coreplate.Translate((coreplate.lx/2,-thickness-delta-delta*2,0))

        if True:
             # setup the hinge joint for qr and coreplate
            (x,y,z) = qr.body.getPosition()
            #print (x,y,z)
            x += -(l1 + tail)/2 + tail
            bolt5 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt5.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt5.Translate((x,thickness*2,z))
            self.Fixing(bolt5.body, qr.body)

            hinge5 = ode.HingeJoint(self.vw.odeworld)
            hinge5.attach(coreplate.body, qr.body)
            hinge5.setAnchor((x,y,z))
            hinge5.setAxis((0,1,0))
            self.hinge5 = hinge5

            # setup the hinge joint for pr and coreplate
            (x,y,z) = pr.body.getPosition()
            x += -(l1)/2
            bolt6 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt6.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt6.Translate((x,thickness * 1.2,z))
            self.Fixing(bolt6.body, pr.body)

            hinge6 = ode.HingeJoint(self.vw.odeworld)
            hinge6.attach(pr.body, coreplate.body)
            hinge6.setAnchor((x,y,z))
            hinge6.setAxis((0,1,0))
            self.hinge6 = hinge6

            # setup the hinge joint for pl and coreplate
            (x,y,z) = pl.body.getPosition()
            x += -(l1)/2
            bolt7 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt7.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt7.Translate((x,thickness * 1.2,z))
            self.Fixing(bolt7.body, pl.body)

            hinge7 = ode.HingeJoint(self.vw.odeworld)
            hinge7.attach(pl.body, coreplate.body)
            hinge7.setAnchor((x,y,z))
            hinge7.setAxis((0,1,0))
            self.hinge7 = hinge7


            # setup the hinge joint for ql and coreplate
            (x,y,z) = ql.body.getPosition()
            x += -(l1+tail)/2 + tail
            bolt8 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
            bolt8.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
            bolt8.Translate((x,thickness*2,z))
            self.Fixing(bolt8.body, ql.body)

            hinge8 = ode.HingeJoint(self.vw.odeworld)
            hinge8.attach(ql.body, coreplate.body)
            hinge8.setAnchor((x,y,z))
            hinge8.setAxis((0,1,0))
            self.hinge8 = hinge8


        self.addObject(coreplate, False)
        self.addObject(pr, False)
        self.addObject(pl, False)
        self.addObject(qr, False)
        self.addObject(ql, False)
        self.addObject(rr, False)
        self.addObject(rl, False)
        self.addObject(fl, False)
        self.addObject(fr, False)
        self.Fixing(fr.body, rr.body)
        self.Fixing(fl.body, rl.body)
        self.addObject(bolt1, False)
        self.addObject(bolt2, False)
        self.addObject(bolt3, False)
        self.addObject(bolt4, False)
        self.addObject(bolt5, False)
        self.addObject(bolt6, False)
        self.addObject(bolt7, False)
        self.addObject(bolt8, False)
        self.pr=pr
        self.pl=pl
        self.qr=qr
        self.ql=ql
        self.rr=rr
        self.rl=rl
        self.coreplate = coreplate
        # add the major shaft
        #sl = 5.0 * ulfactor
        #sl = 4.0 * ulfactor
        sl = 3.0 * ulfactor
        t2 = 0.5 * ulfactor
        lever = vworld.vBox(self, None, False, vw, density, sl+2*edge,thickness,t2)
        lever.Translate((0,thickness * 4, 0))
        hinge9 = ode.HingeJoint(self.vw.odeworld)
        hinge9.attach(lever.body, coreplate.body)
        hinge9.setAnchor((0,0,0))
        hinge9.setAxis((0,1,0))
        self.hinge9 = hinge9

        # connect the lever to qr and ql
        z1 = w1/2+w2
        ls = math.sqrt((sl/2) ** 2 + (z1) ** 2)
        angle = math.atan(sl/2/z1)
        sq1 = vworld.vBox(self, None, False, vw, density, t1,thickness,ls+2*edge)

        sq1.RotateAtPos([(-angle,(0,1,0))], (0,0,0))
        sq1.Translate((sl/4,thickness+delta,z1/2))

        hinge10 = ode.HingeJoint(self.vw.odeworld)
        hinge10.attach(sq1.body, qr.body)
        hinge10.setAnchor((0,0,z1))
        hinge10.setAxis((0,1,0))
        self.hinge10 = hinge10

        bolt10 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
        bolt10.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
        bolt10.Translate((0,thickness * 2.2 + delta,z1))
        self.Fixing(bolt10.body, qr.body)
        self.addObject(bolt10, False)


        hinge11 = ode.HingeJoint(self.vw.odeworld)
        hinge11.attach(sq1.body, lever.body)
        hinge11.setAnchor((sl/2,0,0))
        hinge11.setAxis((0,1,0))
        self.hinge11 = hinge11

        self.addObject(sq1, False)

        bolt11 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
        bolt11.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
        bolt11.Translate((sl/2,thickness * 6, 0))
        self.Fixing(bolt11.body, lever.body)
        self.addObject(bolt11, False)


        sq2 = vworld.vBox(self, None, False, vw, density, t1,thickness,ls+2*edge)

        sq2.RotateAtPos([(-angle,(0,1,0))], (0,0,0))
        sq2.Translate((-sl/4,thickness+delta,-z1/2))

        hinge12 = ode.HingeJoint(self.vw.odeworld)
        hinge12.attach(sq2.body, ql.body)
        hinge12.setAnchor((0,0,-z1))
        hinge12.setAxis((0,1,0))
        self.hinge12 = hinge12

        bolt12 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
        bolt12.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
        bolt12.Translate((0,thickness * 2.2 + delta,-z1))
        self.Fixing(bolt12.body, ql.body)
        self.addObject(bolt12, False)


        hinge13 = ode.HingeJoint(self.vw.odeworld)
        hinge13.attach(sq2.body, lever.body)
        hinge13.setAnchor((-sl/2,0,0))
        hinge13.setAxis((0,1,0))
        self.hinge13 = hinge13
        self.addObject(sq2, False)

        bolt13 = vworld.vCylinder(self, None, False, vw, density, boltradius, thickness, color=colorb)
        bolt13.RotateAtPos([(visual.pi/2, (1,0,0))], (0,0,0))
        bolt13.Translate((-sl/2,thickness * 6, 0))
        self.Fixing(bolt13.body, lever.body)
        self.addObject(bolt13, False)


        self.lever = lever

        #self.Translate((0,thickness*1.5+delta,0))

        # lift it up
        #self.Translate((0,1.*ulfactor,0))

        # fix it
        #join = ode.FixedJoint(self.vw.odeworld)
        #join.attach(coreplate.body, None)
        #join.setFixed()
        #self.join = join

        (x,y,z) = ql.body.getPosition()
        x += -(l1+tail)/2
#        ql.body.addForceAtPos((0,0,-100),(x,y,z))
        z += w1 + w2 * 2
        #qr.body.addForceAtPos((0,0,100),(x,y,z))
        #lever.body.addForceAtPos((0,0,100),(sl/2,0,0))

        #self.RotateAtPos([(visual.pi/2,(1,0,0))], (0,0,0))
        #print self.hinge1.getParam(ode.ParamFMax)

class vGripper(vworld.vCompoundBase):
    def __init__(self, parent, name, vw):
        vworld.vCompoundBase.__init__(self, parent, name, vw)

        GB = vGripperBase(self,None, vw)
        #GB.Translate((0,8.0 * ulfactor,0))

        servo = vServo1(self, None, False, vw)
        servo.RotateAtPos([(-visual.pi/2,(1,0,0)), (visual.pi/2,(0,0,1))], (0,0,0))
        #servo.Translate((0,3.0 * ulfactor,0))
        discpos = servo.getDiscPos()
        #print discpos
        (x,y,z) = GB.lever.body.getPosition()
        #print x,y,z
        #y -= GB.lever.ly/2
        y -= GB.lever.ly
        lpos = numpy.array((x,y,z))
        #print discpos-lpos
        #GB.Translate(discpos-lpos)
        servo.Translate(lpos - discpos)
        self.addObject(GB, False)
        self.addObject(servo, False)
        servo.attach(GB.lever, (0,1,0))
        #servo.attach(GB.coreplate, (0,1,0))

        self.Translate((0,4.0 * ulfactor,0))
        self.servo = servo

        join1 = ode.FixedJoint(self.vw.odeworld)
        join1.attach(servo.body, GB.coreplate.body)
        join1.setFixed()
        self.join1 = join1

        # hook the servo in the sky
        join = ode.FixedJoint(self.vw.odeworld)
        join.attach(servo.body, None)
        join.setFixed()
        self.join = join

        vw.registerServo("T", servo)
