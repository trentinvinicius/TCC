from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import *

f = 1
x = np.linspace(0, 30, num = 1000)
#y = [0.001*cos(2*pi*f*x1)*sin(2*pi*f*x1) + 0.0001*sin(2*pi*f*x1)*atan(2*pi*f*x1)*exp(-x1) + pow(x1,4) for x1 in x]
#print max(y), min(y)



intrupt = randint(0,4)
lim = []

for i in range(intrupt):
   a = 20*random()
   b = 20*random()
   if a > b:
      lim.append((b,a))
   else:
   	  lim.append((a,b))
 

lim = np.array(lim)
print lim
y = []
A = 1
B = 0.2
C = -0.001
D = 0.0003
E = -0.23
F = 5
r = 0
for e,t in enumerate(x):
	a = 1
	for l in lim:
		if (t > l[0] and t < l[1]):
			a = 0
	if (a==1):
		r = A*sin(2*pi*F*t) + D*t**3 + E*t**2
		if (t != 1):
			print B*(1.0 - t)**(C*t)
		#print t, r
		y.append(r)
	else:
		y.append(r)
y = np.array(y)
#print y

plt.plot(x,y)
plt.show()