import time, random, math
import ode, numpy
import vworld
import visual
from vcomponents import *
from modelbase import *

import vgripper


class model(modelBase):
    def __init__(self, log, myWorld):
        modelBase.__init__(self, log, myWorld)

    def load(self):
        vG = vgripper.vGripper(None, None, self.myWorld)
        vG.setGravityMode(False)
        #print vG.qr.geom.getCollideBits()
        vG.setCollideInfo(2,3)
        #vG.setCollideInfo(0,0)

        self.model = vG
        self.myWorld.scene.center = (0,0 * ulfactor,0)
        #self.myWorld.scene.range = (20,20,20)
        #self.myWorld.odeworld.setGravity((0,0,0))

        self.fps = 200
        self.model.Save()
        #self.collisioncheck = False

class mylog():
    def write(self, s):
        print s

def main():
    myworld = vworld.vWorld("Simulation", 800, 600, 100, 100)

    log = mylog()
    t = model(log, myworld)
    t.load()
    t.loadRod()
    #t.setShowFrame(True)
    t.Start()
    while (1):
        time.sleep(1)


if __name__ == '__main__':
    main()
