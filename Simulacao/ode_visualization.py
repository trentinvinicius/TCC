import vtk
import ode
from ode_objects import *
import threading
from operator import eq

class VTK_Visualization(threading.Thread):
    """ Visualization-Window """
    def __init__(self):
        self.ren = vtk.vtkRenderer()
                
        self.win = vtk.vtkRenderWindow()
        self.win.AddRenderer( self.ren )
        
        self.iren = vtk.vtkRenderWindowInteractor();
        self.iren.SetRenderWindow(self.win);
        
        style = vtk.vtkInteractorStyleTrackballCamera();
        self.iren.SetInteractorStyle(style);
        
        self._ctrl = False
        
        self.iren.AddObserver("KeyPressEvent", self._KeypressCtrl)
        self.iren.AddObserver("KeyReleaseEvent", self._KeyreleaseCtrl)
        self.iren.AddObserver("ExitEvent", self._stop)
             
        axesActor = vtk.vtkAxesActor();
        self.axes = vtk.vtkOrientationMarkerWidget()
        self.axes.SetOrientationMarker(axesActor)
        self.axes.SetInteractor(self.iren)
        self.axes.EnabledOn()
        self.axes.InteractiveOn()
        self.ren.ResetCamera()
        
        # information
        self.info = vtk.vtkTextActor()
        self.info.SetDisplayPosition(10,10)
        self.ren.AddActor(self.info)
        
        # window-definitions
        self.SetSize(600, 800)
        self.SetWindowName("ode-viz")
        self.SetBackground( 0.6, 0.6, 0.8 )
        
    def SetSize(self, width, height):
        """ set the size of the window (width, height)  """
        self.win.SetSize( width, height )
        
    def SetWindowName(self, title):
        """ set the name of the window """
        self.win.SetWindowName(title)
        
    def SetBackground(self, red, green, blue):
        """ set background color (red, green, blue) """
        self.ren.SetBackground( red, green, blue )

    def GetActiveCamera(self):
        """ return the current camera """
        return self.ren.GetActiveCamera()
        
    def _KeypressCtrl(self, obj, event):
        key = obj.GetKeySym()
        
        if key == "Control_L" or key == "Control_R":
            self._ctrl = True
            
    def _KeyreleaseCtrl(self, obj, event):
        key = obj.GetKeySym()
        
        if key == "Control_L" or key == "Control_R":
            self._ctrl = False
          
    def run(self):
        self.execute()
        
    def execute(self):
        pass
    
    def _stop(self, obj, event):
        self.stop()
    
    def stop(self):
        pass
    
    def setInfo(self, info):
        self.info.SetInput(info)
        

class ODE_Visualization(VTK_Visualization):
    """ Visualization of the ODE-Space  """
    
    # status
    STOPPED = 0
    RUNNING = 1
    PAUSED  = 2
    statusString = ["stopped", "running", "paused"]
    
    def __init__(self, world, space, dt=0.01):
        """ Create an object of this class with an instance of the world and space.
            All geometric information is automatically extracted from the space and gets
            converted to adequat vtk-representations
        """
        VTK_Visualization.__init__(self)
        self.world = world       
        self.space = space
        self.dt = dt
        self.obj = []
        
        self.simulationStatus = ODE_Visualization.RUNNING
        self.simulationTime   = 0
        self.simulationStep   = 0
        
        self.iren.AddObserver("KeyPressEvent", self._Keypress)

        self.create()
        
    def execute(self, caller, event):
        """ execute one simulation step and update the view;
            overwrite this method to change the simulation
        """
        self.step(self.dt)
        self.update()
        
    def step(self, dt):
        if self.simulationStatus == ODE_Visualization.RUNNING:
            self.world.step(dt)
        
    def GetProperty(self, geom):
        """ return the VTK-Property for a given ode body or geometry """
        if type(geom) == ode.Body:
            for obj in self.obj:
                if obj.geom.getBody() == geom:
                    return obj.act.GetProperty()
        else :
            for obj in self.obj:
                if obj.geom == geom:
                    return obj.act.GetProperty()

    def GetActor(self, geom):
        """ return the VTK-Actor for a given ode body or geometry """
        if type(geom) == ode.Body:
            _find = lambda o: eq(o.geom.getBody(), geom)
        elif type(geom) == str:
            _find = lambda o: eq(o.geom.ident, geom)
        else:
            _find = lambda o: eq(o.geom, geom)
        for obj in self.obj:
            if _find(obj):
                return obj.act  

    def GetObject(self, geom):
        """ return the VTK-Objec tdrafor a given ode body or geometry """
        if type(geom) == ode.Body:
            _find = lambda o: eq(o.geom.getBody(), geom)
        elif type(geom) == str:
            _find = lambda o: eq(o.geom.ident, geom)
        else:
            _find = lambda o: eq(o.geom, geom)
        for obj in self.obj:
            if _find(obj):
                return obj  
   
    def create(self):
        """ this method searches the space for objects to visualize """
        for space in self.space:
            for i in range(space.getNumGeoms()):
                geom = space.getGeom(i)
                self.addGeom(geom)
        
    def start(self):
        """ starts the simulation, can be overwritten """
        self.iren.Initialize()
        
        self.iren.AddObserver('TimerEvent', self.execute)
        self.iren.CreateRepeatingTimer(10);

        self.iren.Start()
        
    def stop(self):
        """ stops the simulation """
        ode.CloseODE()
        
    def _Keypress(self, obj, event):
        key = obj.GetKeySym()

        # toggle shadows
        # Ctrl + s
        if (key == "s" or key == "S") and self._ctrl:
            print "shadow"
        
        # print current viewpoint coordinates
        # Crtl + v
        if (key == "v" or key == "V") and self._ctrl:
            (val1, val2, val3) = self.ren.GetActiveCamera().GetPosition()
            print "Position:  ", val1, val2, val3
            (val1, val2, val3) = self.ren.GetActiveCamera().GetFocalPoint()
            print "FocalPoint:", val1, val2, val3
            (val1, val2, val3) = self.ren.GetActiveCamera().GetViewUp()
            print "ViewUp:    ", val1, val2, val3
        
        # Ctrl + x -> stops the simulation
        if (key == "x" or key == "X") and self._ctrl:
            self.iren.ExitCallback()

        # pause or unpause
        # Ctrl + p
        if (key == "p" or key == "P") and self._ctrl:
            if (self.simulationStatus == ODE_Visualization.PAUSED):
                self.simulationStatus = ODE_Visualization.RUNNING
            elif (self.simulationStatus == ODE_Visualization.RUNNING):
                self.simulationStatus = ODE_Visualization.PAUSED
        
        self.Keypress(key)
        
    def Keypress(self, key):
        """ overwrite this method to define own Keypress-Actions """
        pass
    
    def updateStatus(self):
        """ prints the current simulation-status and time """
        if self.simulationStatus == ODE_Visualization.RUNNING:
            self.simulationTime += self.dt
            self.simulationStep += 1
        
        info =  "simulation\n" + \
                "status: " + ODE_Visualization.statusString[self.simulationStatus] + "\n" + \
                "step:   " + str(self.simulationStep) + "\n" + \
                "time:   " + str(self.simulationTime)
        
        self.setInfo(info)
    
    def update(self):        
        self.updateStatus()
        
        objs = iter(self.obj) 
        for obj in objs:
            obj.update()
        self.win.Render()
        
    def addGeom(self, geom):
        obj = False
        # Box
        if type(geom) == ode.GeomBox:
            obj = ODE_Box(geom)
        # Sphere
        elif type(geom) == ode.GeomSphere:
            obj = ODE_Sphere(geom)
        # Plane
        elif type(geom) == ode.GeomPlane:
            obj = ODE_Plane(geom)
        # Ray
        elif type(geom) == ode.GeomRay:
            obj = ODE_Ray(geom)
        # TriMesh
        elif type(geom) == ode.GeomTriMesh:
            obj = ODE_TriMesh(geom)
        # Cylinder
        elif type(geom) == ode.GeomCylinder:
            obj = ODE_Cylinder(geom)
        # Capsule
        elif type(geom) == ode.GeomCapsule:
            obj = ODE_Capsule(geom)
        # CappedCylinder
        elif type(geom) == ode.GeomCCylinder:
            obj = ODE_Capsule(geom)
            
        if obj:
            self.obj.append(obj)
            self.addActor(obj.act)

    def drawLines(self, points):       
        for p in points:
            line = vtk.vtkLineSource()
            line.SetPoint1(p[0:3])
            line.SetPoint2(p[3:6])
            line.SetResolution(100)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(line.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(1,1,1)
            if (p[6]):
                actor.GetProperty().SetLineStipplePattern(0xf0f0)
            actor.GetProperty().SetLineStippleRepeatFactor(1)
            actor.GetProperty().SetPointSize(1)
            actor.GetProperty().SetLineWidth(1.5)
            self.addActor(actor)

    def stlGeom(self, obj, file):
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file)
        if vtk.VTK_MAJOR_VERSION <= 5:
            obj.map.SetInput(reader.GetOutput())
        else:
            obj.map.SetInputConnection(reader.GetOutputPort())
        obj.act.SetMapper(obj.map)
        self.addActor(obj.act)

            
    def removeGeom(self, geom):
        if type(geom) == ode.Body:
            for obj in self.obj:
                if obj.geom.getBody() == geom:
                    self.obj.remove(obj)
                    break
        else :
            for obj in self.obj:
                if obj.geom == geom:
                    self.obj.remove(obj)
                    break

    def addActor(self, actor):
        self.ren.AddActor(actor)
