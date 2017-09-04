import time, random, math
import ode, numpy, threading
import vworld
import visual
from vcomponents import *
import modelthread



class modelBase(modelthread.simJobThreadBase):
    def __init__(self, log, myWorld):
        modelthread.simJobThreadBase.__init__(self, log)
        self.myWorld = myWorld
        self.rod = None
        self.model = None

        # for show frame
        self.aabbbox = vworld.framebox(visual.color.red)
        self.cg = vworld.cross(visual.color.green)
        self.setShowFrame(False)

        self.defaultPosition = False
        self.lock = threading.Semaphore()
        self.listeners = []
        self.recorder = None
        self.collisioncheck = True

    def getTime(self):
        self.lock.acquire()
        t = self.t
        self.lock.release()
        return t

    def setRecorder(self, recorder, framerate):
        self.lock.acquire()
        self.recorder = recorder
        self.recorder_time = 0.0
        self.frametime = 1.0/framerate
        self.lock.release()

    def addListener(self, listener):
        self.lock.acquire()
        self.listeners.append(listener)
        self.lock.release()

    def removeListener(self, listener):
        self.lock.acquire()
        self.listeners.remove(listener)
        self.lock.release()

    def unload(self):
        print "Unload"
        self.setShowFrame(False)
        if self.model != None:
            self.model.unload()
            self.model = None

    def __del__(self):
        self.unload()

    def loadRod(self, show=True):
        if show:
            rod = vworld.vBox(None, "rod", False, self.myWorld, 10, 5 * ulfactor,0.2* ulfactor,0.2* ulfactor, color=visual.color.yellow)
            rod.body.setPosition((5* ulfactor,15* ulfactor,0* ulfactor))
            rod.body.setGravityMode(False)
            # it will not touch virtual object and the ground
            rod.setCollideInfo(1, 0x7FFFFFFE)
            self.rod = rod
        else:
            if self.rod:
                self.rod.unload()
                #del self.rod
                self.rod = None

    def setShowFrame(self, showframe, trackobj=None):
        self.showframe = showframe
        if showframe:
            v = 1
            if trackobj:
                self.track = trackobj
            else:
                self.track = self.model
        else:
            v = 0
        self.aabbbox.setVisible(v)
        self.cg.setVisible(v)

    def handleKeys(self):
        if self.myWorld.scene.kb.keys: # is there an event waiting to be processed?
            s = self.myWorld.scene.kb.getkey()
            if self.rod != None:
                rod = self.rod
                step = 0.1 * ulfactor
                if s == 'left':
                    rod.Translate((-step,0,0))
                elif s == 'right':
                    rod.Translate((step,0,0))
                elif s == 'up':
                    rod.Translate((0,step,0))
                elif s == 'down':
                    rod.Translate((0,-step,0))
                elif s == 'page down':
                    rod.Translate((0,0,step))
                elif s == 'page up':
                    rod.Translate((0,0,-step))
                elif s == 'x':
                    M = vworld.rotate_transforms((numpy.pi/2,(1,0,0)))
                    rod.Rotate(M)
                elif s == 'y':
                    M = vworld.rotate_transforms((numpy.pi/2,(0,1,0)))
                    rod.Rotate(M)
                elif s == 'z':
                    M = vworld.rotate_transforms((numpy.pi/2,(0,0,1)))
                    rod.Rotate(M)
                elif s == '0':
                    rod.body.setPosition((0,5,0))
                    rod.body.setForce((0,0,0))
                    rod.body.setLinearVel((0,0,0))
                    rod.body.setAngularVel((0,0,0))
                    rod.Rotation(numpy.identity(3,float))

    def showFrame(self):
       if self.showframe and self.track != None:
            self.aabbbox.setParam(self.track.getAABB())
            m = self.track.computeMass()
            self.cg.setPos(m.c)

    # the simulation time vs realtime
    def updateTimeRatio(self, r):
        self.ratio = r
        #print "%0.2f", r

    def RestorePosition(self):
        self.defaultPosition = True


    def Run(self):
        self.running = True
        world = self.myWorld.odeworld
        space = self.myWorld.odespace
        contactgroup = ode.JointGroup()


        dt = 1.0/self.fps

        #world.setGravity((0,-self.myWorld.g,0))

        self.t = 0.0
        try:
            while (self.keepGoing):
                if self.defaultPosition:
                    self.model.Restore()
                    self.defaultPosition = False
                #visual.rate(fps)
                self.handleKeys()
                self.showFrame()

                self.myWorld.updateObjectPos()

                if self.myWorld.servomanager.fhold:
                    time.sleep(0.01)
                    continue

                t1 = time.time()
                n = 1
                adv = dt/n
                for i in range(n):
                    # Detect collisions and create contact joints
                    if self.collisioncheck:
                        space.collide((world,contactgroup,self.rod), vworld.near_callback)

                    # Simulation step
                    self.myWorld.updateServos(adv)

                    world.step(adv)

                    self.lock.acquire()
                    self.t += adv
                    for listener in self.listeners:
                        listener.t -= adv
                        if listener.t <= 0.0:
                            self.listeners.remove(listener)
                            listener.notify()
                    if self.recorder != None:
                        self.recorder_time += adv
                        if self.recorder_time >= self.frametime:
                            self.recorder.recordFrame()
                            self.recorder_time -= self.frametime
                    self.lock.release()

                    # Remove all contact joints
                    contactgroup.empty()
                delta = time.time() - t1
                self.updateTimeRatio(delta / dt)
        except Exception, e:
            self.log.write("Exception in Running model %s\n" % e)

        self.running = False
