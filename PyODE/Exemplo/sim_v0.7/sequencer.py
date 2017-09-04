import threading
import vworld
import modelthread
import ConfigParser
import time,sys

#import serial,vmotor, cmdcommon

class CommandList():
    def __init__(self, log):
        self.log = log
        self.commandlist = []

    def Parse(self, lines):
        self.commandlist = []
        try:
            for line in lines.split("\n"):
                line = line.strip()
                if len(line) == 0:
                    continue
                if line[0] == "#":
                    if len(line) > 1 and line[1] != "#":
                        self.commandlist.append(["#", line])
                    continue
                commands = line.split(":")
                #if len(commands) == 0:
                #    continue
                if commands[0].strip() == "servo":
                    if len(commands) == 5:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = float(commands[3].strip())
                        dt = float(commands[4].strip())
                        self.commandlist.append(["s",servonumber,pos,t,dt])
                    elif len(commands) == 4:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = float(commands[3].strip())
                        self.commandlist.append(["s",servonumber,pos,t,0.0])
                    elif len(commands) == 3:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = -1
                        self.commandlist.append(["s",servonumber,pos,t,0.0])
                    else:
                        self.log.write("Invalid servo parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "curve":
                    if len(commands) == 5:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = float(commands[3].strip())
                        dt = float(commands[4].strip())
                        self.commandlist.append(["c",servonumber,pos,t,dt])
                    elif len(commands) == 4:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = float(commands[3].strip())
                        self.commandlist.append(["c",servonumber,pos,t,0.0])
                    elif len(commands) == 3:
                        servonumber = int(commands[1].strip())
                        pos = float(commands[2].strip())
                        t = -1
                        self.commandlist.append(["c",servonumber,pos,t,0.0])
                    else:
                        self.log.write("Invalid servo parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "tv":
                    if len(commands) == 2:
                        t = float(commands[1].strip())
                        self.commandlist.append(["tv",t])
                    else:
                        self.log.write("Invalid time variable parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "sleep":
                    if len(commands) == 2:
                        t = float(commands[1].strip())
                        self.commandlist.append(["w",t])
                    else:
                        self.log.write("Invalid sleep parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "csleep":
                    if len(commands) == 2:
                        t = float(commands[1].strip())
                        self.commandlist.append(["cw",t])
                    else:
                        self.log.write("Invalid csleep parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "timefactor":
                    if len(commands) == 2:
                        t = float(commands[1].strip())
                        self.commandlist.append(["f",t])
                    else:
                        self.log.write("Invalid timefactor parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "label":
                    if len(commands) == 2:
                        self.commandlist.append(["l", commands[1].strip()])
                    else:
                        self.log.write("Invalid label parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "goto":
                    if len(commands) == 2:
                        self.commandlist.append(["g", commands[1].strip(), 0])
                    else:
                        self.log.write("Invalid goto parameters: %s\n" % line)
                        return False
                elif commands[0].strip() == "hold":
                    self.commandlist.append(["h"])
                elif commands[0].strip() == "release":
                    self.commandlist.append(["r"])
                elif commands[0].strip() == "break":
                    self.commandlist.append(["b"])
                elif commands[0].strip() == "quit":
                    self.commandlist.append(["q"])
                else:
                    self.log.write("Invalid command: %s\n" % line)
                    return False
            # check if goto label exists
            for command in self.commandlist:
                if command[0] == "g":
                    found = False
                    i = 0
                    for label in self.commandlist:
                        if label[0] == "l":
                            if label[1] == command[1]:
                                found = True
                                command[2] = i
                                break
                        i += 1
                    if not found:
                        self.log.write("Goto label not defined: %s\n" % command[1])
                        return False

            return True
        except Exception,e:
            self.log.write("Invalid command: %s, %s\n" % (line,e))
            return False


class Sequencer(modelthread.simJobThreadBase):
    def __init__(self, log, parent, model):
        modelthread.simJobThreadBase.__init__(self, log)
        self.log = log
        self.parent = parent
        self.model = model
#        self.commandlist = []
        self.cl = CommandList(log)
        self.timerlock = threading.Semaphore()
        self.timerlock.acquire()
        self.steplock = threading.Semaphore()
        self.steplock.acquire()
        self.breaking = False

    def Execute(self, servomanager, stepping=False):
        self.servomanager = servomanager
        if not self.running:
            self.stepping = stepping
            self.Start()

    def Stop(self):
        modelthread.simJobThreadBase.Stop(self)
        self.steplock.release()
        self.timerlock.release()

    def NextStep(self):
        if self.breaking:
            self.steplock.release()

    def Run(self):
        self.running = True
        self.breaking = False
        try:
            starttime = self.model.getTime()
            i = 0
            timefactor = 1.0
            self.servomanager.hold(False)
            tv = 0.0
            while i < (len(self.cl.commandlist)):
                commands = self.cl.commandlist[i]
                if commands[0] == "s":
                    servo = self.servomanager.getServo(commands[1])
                    if servo == None:
                        self.log.write("No such servo: %d\n" % commands[1])
                        break
                    else:
                        if commands[3] == -1:
                            t = tv
                        else:
                            t = commands[3]
                        s = "servo : %d : %0.2f : %0.2f : %0.2f\n" % (commands[1],commands[2],t, commands[4])
                        self.parent.appendResult(s)
                        servo.MoveServoLinear(vworld.DegreeToRadian(commands[2]), t * timefactor, commands[4] * timefactor)
                elif commands[0] == "c":
                    servo = self.servomanager.getServo(commands[1])
                    if servo == None:
                        self.log.write("No such servo: %d\n" % commands[1])
                        break
                    else:
                        if commands[3] == -1:
                            t = tv
                        else:
                            t = commands[3]
                        s = "curve : %d : %0.2f : %0.2f : %0.2f\n" % (commands[1],commands[2],t,commands[4])
                        self.parent.appendResult(s)
                        servo.MoveServoCurve(vworld.DegreeToRadian(commands[2]), t * timefactor, commands[4] * timefactor)
                elif commands[0] == "h":
                    self.servomanager.hold(True)
                elif commands[0] == "r":
                    self.servomanager.hold(False)
                elif commands[0] == "f":
                    timefactor = commands[1]
                    s = "timefactor : %0.2f\n" % timefactor
                    self.parent.appendResult(s)
                elif commands[0] == "tv":
                    tv = commands[1]
                elif commands[0] == "w":
                    self.t = commands[1]
                    self.t *= timefactor
                    s = "sleep : %0.2f\n" % self.t
                    self.parent.appendResult(s)
                    self.model.addListener(self)
                    self.timerlock.acquire() # wait until the model release it
                    if self.keepGoing and self.stepping:
                        self.parent.appendResult("==> Break\n")
                        self.breaking = True
                        self.steplock.acquire()
                        self.breaking = False
                elif commands[0] == "cw":
                    self.t = commands[1]
                    s = "sleep : %0.2f\n" % self.t
                    self.parent.appendResult(s)
                    self.model.addListener(self)
                    self.timerlock.acquire() # wait until the model release it
                    if self.keepGoing and self.stepping:
                        self.parent.appendResult("==> Break\n")
                        self.breaking = True
                        self.steplock.acquire()
                        self.breaking = False
                elif commands[0] == "b":
                    self.parent.appendResult("==> Break\n")
                    self.breaking = True
                    self.steplock.acquire()
                    self.breaking = False
                elif commands[0] == "q":
                    break
                elif commands[0] == "l":
                    self.parent.appendResult("label : %s\n" % commands[1])
                    #continue
                elif commands[0] == "g":
                    self.parent.appendResult("goto : %s\n" % commands[1])
                    i = commands[2]
                elif commands[0] == "#":
                    self.parent.appendResult(commands[1] + "\n")


                endtime = self.model.getTime()
                self.totalTime =(endtime - starttime)
                if not self.keepGoing:
                    break
                self.log.write("Total time: %0.1f" % self.totalTime)
                i += 1


            if self.keepGoing:
                self.parent.appendResult("==> Exit: execution time: %0.1f\n" % self.totalTime)

        except Exception, e:
            self.log.write("Exception in Sequence Run %s\n" % e)

        if self.keepGoing:
            self.parent.OnSequencerExit(self)
        self.running = False

    # self.model will call this function when self.t is reaching 0.0
    def notify(self):
        self.timerlock.release()

    def Parse(self, lines):
        return self.cl.Parse(lines)

class ServoInfo():
    def __init__(self, normalpos, minpos, maxpos, steps):
        self.normalpos = normalpos
        self.minpos = minpos
        self.maxpos = maxpos
        self.steps = steps

    def getServoPos(self, angle):
        pos = self.normalpos + int((self.steps * angle) / 90.0)
        if pos > self.maxpos:
            pos = self.maxpos
        elif pos < self.minpos:
            pos = self.minpos
        return pos

    def getAngle(self, pos):
        diff = pos - self.normalpos
        angle = float(diff) / float(self.steps) * 90
        return angle

class ServoInfoCfg:
    def __init__(self, log, filename):
        self.log = log
        self.servoinfo = []
        self.read(filename)

    def read(self, filename):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(filename))
        self.refresh()

    def refresh(self):
        section = "Servo"
        for motor in range(1,30):
            section = "Servo%d" % motor
            if self.config.has_section(section):
                vnormal = self.config.getint(section, "normal")
                vmax = self.config.getint(section, "max")
                vmin = self.config.getint(section, "min")
                vsteps = self.config.getint(section, "steps")
                self.servoinfo.append(ServoInfo(vnormal, vmin, vmax, vsteps))
            else:
                break

