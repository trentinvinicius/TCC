import time, random, math
import ode, numpy
import vworld
import visual
from vcomponents import *
from modelbase import *

import vrobot1


class model(modelBase):
    def __init__(self, log, myWorld):
        modelBase.__init__(self, log, myWorld)

    def load(self):
        vLBody = vrobot1.vLBody(None, None, self.myWorld)
        vLBody.setCollideInfo(0,1)
        self.model = vLBody
        self.myWorld.scene.center = (0,10 * ulfactor,0)
        #self.myWorld.scene.range = (20,20,20)
        self.fps = 200
        self.model.Save()
        #vLBody.setTransparency(0.2, ["Servo1"])

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
