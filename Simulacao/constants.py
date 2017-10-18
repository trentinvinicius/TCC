from math import pi

#simulation
FRAMES			=	 30.0
TIMESTEP		=	 1/FRAMES
MAXSIMTIME		=	 30.0
GRAVITY			=	 (0, -9.81, 0)
WINDOWSIZE		=	 800,600
BACKGROUND		=	 50./255, 153./255, 204./255
BASEHEIGHT		=	 1.0
BASEDENSITY		=	 1.0
BASEWIDTH		=	 50.0
BASELENGTH		=	 1000.0

#wheel
WHEELRADIUS 	= 	 0.20
WHEELWIDTH  	=	 0.15
WHEELCOLOR		=	 0, 1, 0
WHEELWEIGHT		=	 10
MAXSTEERANGLE 	= 	 30.0 #pi/6
MINSTEERANGLE 	=  	-30.0 #-pi/6

#car
CARLENGTH		=	 3.0
CARWIDTH		=	 1.5
MAINCARCOLOR	=	 0, 0, 1
CARCOLOR		=	 1, 0, 0
CARHEIGHT		=	 1.5
CARWEIGHT		=	 1500.0
MAXTORQUE		=	 1000
CARGOINGFILE	=	 'Images/carindo.stl'
CARCOMINGFILE	=	 'Images/carvindo.stl'

#person
PERSONWEIGHT	=	 75
PERSONCOLOR 	=	 146.0/255, 54.0/255, 252.0/255
PERSONHEIGHT	=	 1.8
PERSONRADIUS	=	 0.4
PERSONDENSITY  	=	 1062.0
SPHERERADIUS	=	 0.15
PERSONFILE		=	 "Images/LegoMan-modified.stl"

#road
ROADSIZE		=	 3.0
ROADCOLOR		= 	 53.0/255, 55.0/255, 60.0/255
ROADDENSITY		=	 2000.0
ROADHEIGHT		=	 0.1
ROADLENGTH		=	 1000.0

#tree
TREECOLOR		=	 0,1,0#125.0/255, 65.0/255, 39.0/255
TREEDENSITY		=	 600
TREEPOLEHEIGHT	=	 2.5
TREEPOLERADIUS	=	 0.3
TREEFILE		=	 "Images/tree.stl"

#pole
POLECOLOR		=	 211.0/255, 211.0/255, 211.0/255
POLEDENSITY		=	 2500