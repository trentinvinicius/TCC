import json
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


with open('velocTimeDist.txt') as data:
	velAndTime = json.load(data)				
tempo = []
distancia = []
vel = []
for vt in velAndTime:
	vel.append(vt[0])
	tempo.append(vt[1][0])
	distancia.append(vt[1][1])
plt.plot(vel, distancia)
interpol = interp1d(vel, distancia, kind='quadratic')
interpol2 = interpol(vel)
#plt.plot(vel, distancia)
plt.figure()
plt.plot(vel, distancia, 'ro', vel, interpol2, 'k--')
plt.show()