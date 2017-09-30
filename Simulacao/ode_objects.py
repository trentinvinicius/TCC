import vtk
import ode

class ODE_Object():
    """ Standard class for visualizations of ODE-Geometries  """
    def __init__(self, geom, mapper=0):
        self.geom = geom
        
        self.map   = vtk.vtkPolyDataMapper()
        self.act   = vtk.vtkActor()
        self.trans = vtk.vtkTransform()
        
        if mapper == 0:
            self.map.SetInputConnection( self.src.GetOutputPort() )
        else:
            self.map.SetInput(eval("self.src" + mapper))
            
        self.map.ScalarVisibilityOff(); 
            
        self.act.SetMapper( self.map )
        self.act.SetUserTransform(self.trans)     

    def getRotation(self):
        return self.geom.getRotation()
    
    def getPosition(self):
        return self.geom.getPosition()
    
    def update(self):
        if self.geom.isEnabled():
            (x,y,z) = self.getPosition()
            R = self.getRotation()
        
            self.trans.SetMatrix([R[0], R[1], R[2], x,
                                  R[3], R[4], R[5], y,
                                  R[6], R[7], R[8], z,
                                  0,    0,    0,    1])  

        
        
class ODE_Box(ODE_Object):
    """ VTK visualization of class ode.GeomBox  """
    def __init__(self, geom, image = None):
        '''modified by Vinicius Trentin'''
        
        self.src = vtk.vtkCubeSource()
        ODE_Object.__init__(self, geom)
        
        (xsize, ysize, zsize) = self.geom.getLengths()

        self.src.SetXLength(xsize)
        self.src.SetYLength(ysize)
        self.src.SetZLength(zsize)

    def SetTexture(self, image):
        self.reader = vtk.vtkPNGReader()
        self.reader.SetFileName(image)
        self.texture = vtk.vtkTexture()
        self.trans.Scale(.1,0.1,1.0)
        self.texture.SetTransform(self.trans)
        self.texture.SetInput(self.reader.GetOutput())
        self.map.SetInput(self.src.GetOutput())
        self.act.SetMapper(self.map)
        self.act.SetTexture(self.texture)

            
class ODE_Ray(ODE_Object):
    """ VTK visualization of class ode.GeomRay  """
    def __init__(self, geom):
        
        self.src = vtk.vtkLineSource()
        ODE_Object.__init__(self, geom, ".GetOutput()")
        
        length = self.geom.getLength()

        self.src.SetPoint1(0, 0,-length/2)
        self.src.SetPoint2(0, 0, length/2)
        
class ODE_TriMesh(ODE_Object):
    """ VTK visualization of class ode.GeomTriMesh  """
    def __init__(self, geom):
        
        self.src   = vtk.vtkPolyData()
        ODE_Object.__init__(self, geom, "")
                        
        points = vtk.vtkPoints()
        vertices = vtk.vtkCellArray()

        for i in range(geom.getTriangleCount()) :
            (p0,p1,p2) = geom.getTriangle(i)
            id0 = points.InsertNextPoint(p0)
            id1 = points.InsertNextPoint(p1)
            id2 = points.InsertNextPoint(p2)
            
            vertices.InsertNextCell(3)
            vertices.InsertCellPoint(id0)
            vertices.InsertCellPoint(id1)
            vertices.InsertCellPoint(id2)
        
        self.src.SetPoints(points)
        self.src.SetPolys(vertices)
        
class ODE_Sphere(ODE_Object):
    """ VTK visualization of class ode.GeomSphere  """
    def __init__(self, geom):
        self.src = vtk.vtkSphereSource()
        ODE_Object.__init__(self, geom)
        
        radius = self.geom.getRadius()

        self.src.SetRadius(radius)
        self.src.SetThetaResolution(20)
        self.src.SetPhiResolution(11)


class ODE_Cylinder(ODE_Object):
    """ VTK visualization of class ode.GeomCylinder  """
    def __init__(self, geom):
        self.src = vtk.vtkCylinderSource()

        ODE_Object.__init__(self, geom)
        
        (radius, height) = self.geom.getParams() 

        self.src.SetRadius(radius)
        self.src.SetHeight(height)
        
        self.src.SetResolution(20)
        
    def update(self):
        if self.geom.isEnabled():
            ODE_Object.update(self)
            self.trans.RotateX(90)
        
        
class ODE_Capsule_imp(ODE_Object):
    """ VTK visualization of class ode.GeomCapsule  """
    def __init__(self, geom):
        
        self.src = vtk.vtkAppendPolyData()        
        
        ODE_Object.__init__(self, geom)
        
        (radius, height) = geom.getParams()
        
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetResolution(20)
        cylinder.SetRadius(radius)
        cylinder.SetHeight(height)        
        
        sphere_1 = vtk.vtkSphereSource()
        sphere_1.SetThetaResolution(20)
        sphere_1.SetPhiResolution(11)
        sphere_1.SetRadius(radius)
        sphere_1.SetCenter(0, 0.5*height, 0)
        
        sphere_2 = vtk.vtkSphereSource()
        sphere_2.SetThetaResolution(20)
        sphere_2.SetPhiResolution(11)
        sphere_2.SetRadius(radius)
        sphere_2.SetCenter(0, -0.5*height, 0)
        
        self.src.AddInput(cylinder.GetOutput())        
        self.src.AddInput(sphere_1.GetOutput())
        self.src.AddInput(sphere_2.GetOutput())
        
    def update(self):
        if self.geom.isEnabled():
            ODE_Object.update(self)
            self.trans.RotateX(90)
        
class ODE_Capsule(ODE_Object):
    """ VTK visualization of class ode.GeomCapsule  """
    def __init__(self, geom):
        
        self.src = vtk.vtkContourFilter()      
        
        ODE_Object.__init__(self, geom)
        
        (radius, height) = geom.getParams()
        
        cylinder = vtk.vtkCylinder()
        cylinder.SetRadius(radius)

        vertPlane = vtk.vtkPlane()
        vertPlane.SetOrigin(0, height/2, 0)
        vertPlane.SetNormal(0, 1, 0)
        
        basePlane = vtk.vtkPlane()
        basePlane.SetOrigin(0, -height/2, 0)
        basePlane.SetNormal(0, -1, 0)
        
        sphere_1 = vtk.vtkSphere()
        sphere_1.SetCenter(0,-height/2, 0)
        sphere_1.SetRadius(radius)

        sphere_2 = vtk.vtkSphere()
        sphere_2.SetCenter(0, height/2, 0)
        sphere_2.SetRadius(radius)

        # Combine primitives, Clip the cone with planes.
        cylinder_fct = vtk.vtkImplicitBoolean()
        cylinder_fct.SetOperationTypeToIntersection()
        cylinder_fct.AddFunction(cylinder)
        cylinder_fct.AddFunction(vertPlane)
        cylinder_fct.AddFunction(basePlane)

        # Take a bite out of the ice cream.
        capsule = vtk.vtkImplicitBoolean()
        capsule.SetOperationTypeToUnion()
        capsule.AddFunction(cylinder_fct)
        capsule.AddFunction(sphere_1)
        capsule.AddFunction(sphere_2)
        
        capsule_fct = vtk.vtkSampleFunction()
        capsule_fct.SetImplicitFunction(capsule)
        capsule_fct.ComputeNormalsOff()
        capsule_fct.SetModelBounds(-height-radius,height+radius,-height-radius,height+radius,-height-radius,height+radius)
        
        self.src.SetInputConnection(capsule_fct.GetOutputPort())
        self.src.SetValue(0, 0.0)        
        
    def update(self):
        if self.geom.isEnabled():
            ODE_Object.update(self)
            self.trans.RotateX(90)


class ODE_Plane(ODE_Object):
    """ VTK visualization of class ode.GeomPlane  """
    def __init__(self, geom):
        self.src = vtk.vtkDiskSource()
        ODE_Object.__init__(self, geom)
        self.size = 1000
        
        self.src.SetOuterRadius(self.size)
        self.src.SetInnerRadius(0)
        self.src.SetCircumferentialResolution(30)

    def getRotation(self):
        (a, b, c), d = self.geom.getParams()
        
        p1 = [.5, .5, .0]
        p2 = [.1, .7, .2]
        
        if a != 0:
            p1[0] = (b*p1[1] + c*p1[2] - d) / -a
            p2[0] = (b*p2[1] + c*p2[2] - d) / -a        
        elif b != 0:
            p1[1] = (a*p1[0] + c*p1[2] - d) / -b
            p2[1] = (a*p2[0] + c*p2[2] - d) / -b        
        elif c != 0:
            p1[2] = (a*p1[0] + b*p1[1] - d) / -c
            p2[2] = (a*p2[0] + b*p2[1] - d) / -c
        
        w = [ p2[0]-p1[0],
              p2[1]-p1[1],
              p2[2]-p1[2] ]
        
        v = [ w[1]*c - w[2]*b,
              w[2]*a - w[0]*c,
              w[0]*b - w[1]*a ]
        
        w_norm = (w[0]**2 + w[1]**2 + w[2]**2)**0.5
        w = [ w[0]/w_norm,
              w[1]/w_norm,
              w[2]/w_norm ]
        
        v_norm = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
        v = [ v[0]/v_norm,
              v[1]/v_norm,
              v[2]/v_norm ]
        
        return [v[0], w[0], a,
                v[1], w[1], b,
                v[2], w[2], c]
    
    def getPosition(self):
        (a, b, c), d = self.geom.getParams()
        h = d/(a**2 + b**2 + c**2)
        return [a*h,b*h,c*h]

