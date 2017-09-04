from sets import Set
import time
import wxcommon

##import cmdcommon

gThreadPool = None

class ThreadPool():
    def __init__(self, log):
        self.log = log
        self.threads = Set()
        self.stopping = False

    def AddThread(self, thread):
        self.threads.add(thread)

    def RemoveThread(self, thread):
        if self.stopping:
            return

        self.threads.remove(thread)

    def StopThread(self, thread, remove=True):
        thread.Stop()
        while thread.IsRunning():
            time.sleep(0.1)

        if remove:
            self.threads.remove(thread)

    def StopAll(self):
        #time.sleep(0.5)
        self.stopping = True
        for thread in self.threads:
            self.StopThread(thread, False)
        self.threads.clear()
        self.stopping = False


class simJobThreadBase(wxcommon.JobThreadBase):
    def __init__(self, log):
        global gThreadPool

        wxcommon.JobThreadBase.__init__(self, log)

        if gThreadPool == None:
            gThreadPool = ThreadPool(log)
        gThreadPool.AddThread(self)

##    def Run(self):
##        self.running = True
##        model.Run()
##        self.running = False
##
##    def Stop(self):
##        model.keepGoing = False
##        wxcommon.JobThreadBase.Stop(self)
