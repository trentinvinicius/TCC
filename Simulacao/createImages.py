import numpy as np
from constants import *
from math import sin, cos, pi, exp
import pylab as plt
from scipy.stats import skewnorm, norm
from addNoise import addNoise
import cv2
from mpl_toolkits.mplot3d import Axes3D


def createImages(data, inputNum):
	'''
	create images for the 5 input channels
	'''
	
	Y  =  np.linspace(MINX, MAXX, IMAGEHEIGHT)
	X  =  np.linspace(MINY, MAXY,  IMAGEWIDTH)
	X, Y = np.meshgrid(X, Y)
	returnImages = 	[]

	if (inputNum == 1):
		'''
		Input 1:
			People    -   6 channels
			Animal    -   1 channel
			Crossroad -   1 channel
			Semaphore -   1 channel
		'''
		for people, animal, road in data: #data = peopleData, animalData, roadData
			imageData = np.zeros((IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS1))
			# add noise
			pD = addNoise(people, "people")
			aD = addNoise(animal, "animal")
			for p in pD:
				posY, _, posX =  p[0]
				v             =  p[1]
				o 	     	  =  p[2]
				g 		      =  p[3]
				a 		      =  p[4]
				data = image(X, Y, posY, posX, v, o)
				imageData[:,:,g*3 + a] += data.reshape(IMAGEHEIGHT, IMAGEWIDTH)
			if aD != None:
				for a in aD:
					posY, _, posX =  a[0]
					v             =  p[1]
					o 		      =  p[2]
					data = image(X, Y, posY, posX, v, o)
					imageData[:, :, 6] += data.reshape(IMAGEHEIGHT, IMAGEWIDTH)
			#numLanes, direction, laneMain, crossPos, statusSemaphore(0 verde para pedestres, vermelho carros  /  1 vermelho para pedestres, verde carros)
			if road[3] > 0:	# check if there is a crossroad
				if (road[2] <= road[0]/2.0):
					zPos = -(road[0]/2.0 - road[2] + 0.5) * ROADSIZE
				else:
					zPos = (road[2] - road[0]/2.0 -1 + 0.5) * ROADSIZE		  
				sides = [zPos + road[0]/2.0 * ROADSIZE, zPos - road[0]/2.0 * ROADSIZE]
				x_min, x_max = road[3] - 1, road[3] + 1
				crossroad = np.zeros((IMAGEHEIGHT, IMAGEWIDTH))
				crossroad[int(2*(abs(MINX) + x_min)) : int(2*(abs(MINX) + x_max)), int(2*(abs(MINY) + sides[1])) : int(2*(abs(MINY) + sides[0]))] = 1.0
				imageData[:,:,7]= cv2.GaussianBlur(crossroad ,(15,15), 35,75)
				signal = np.zeros((IMAGEHEIGHT, IMAGEWIDTH))
				if road[4] == 0: # semaphore is open for pedestrians
					signal[int(2*(abs(MINX) + x_min)) : int(2*(abs(MINX) + x_max)), int(2*(abs(MINY) + sides[1])) : int(2*(abs(MINY) + sides[0]))] = 1.0
					imageData[:,:,8]= cv2.GaussianBlur(signal ,(15,15), 35,75)
				else:
					signal[int(2*(abs(MINX) + x_min)) : int(2*(abs(MINX) + x_max)), int(2*(abs(MINY) + sides[1])) : int(2*(abs(MINY) + sides[0]))] = -1.0
					imageData[:,:,8]= cv2.GaussianBlur(signal ,(15,15), 35,75)
			imageData.reshape((-1, IMAGEWIDTH, IMAGEHEIGHT, INPUTCHANNELS1)).astype(np.float32)
			for i in range(7):
				soma = sum(sum(imageData[:, :, i]))
				if soma == 0:
					soma = 1
				imageData[:, :, i] /= soma
			
			
			returnImages.append(imageData)
			
	elif (inputNum == 2):
		'''
		Input 2:
				OtherCars  - 1 channel
		'''
		for ocD in data:
			imageData = np.zeros((IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS2))
			if ocD != None:
				for oc in ocD:
					posY, _, posX =  oc[0]
					d             =  oc[1]
					v 		      =  oc[2]
					if d == 1:
						o = 0
					else:
						o = 180
					data = image(X, Y, posY, posX, v, o, True)
					imageData[:, :, 0] += data.reshape(IMAGEHEIGHT, IMAGEWIDTH)
			imageData.reshape((-1, IMAGEWIDTH, IMAGEHEIGHT, INPUTCHANNELS2)).astype(np.float32)
			soma = sum(sum(imageData))
			if soma == 0:
				soma = 1
			imageData /= soma
			returnImages.append(imageData)
		'''
		for i in range(1):
										pI = imageData[:, :, i]
										plt.figure()
										plt.subplot()
										plt.ylim(0,400)
										plt.title(i)
										plt.imshow(pI, cmap = 'gray')
										ax = plt.gca()
										plt.colorbar()
										plt.show()
		'''
	elif (inputNum == 3):
		'''
		Input 3
				Tree/People  -  1 channel
				Road  		 -  1 channel
				River		 -	1 channel
		'''
		imageData = np.zeros((IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS3))

		for rD, tpD, riverD in data: # data = road, treepole
			#numLanes, direction, laneMain, crossPos, statusSemaphore(0 verde para pedestres, vermelho carros  /  1 vermelho para pedestres, verde carros)
			if (rD[2] <= rD[0]/2.0):
				zPos = -(rD[0]/2.0 - rD[2] + 0.5) * ROADSIZE
			else:
				zPos = (rD[2] - rD[0]/2.0 -1 + 0.5) * ROADSIZE		  
			sides = [zPos + rD[0]/2.0 * ROADSIZE, zPos - rD[0]/2.0 * ROADSIZE]
			ks = np.arange(sides[1], sides[0] + ROADSIZE, ROADSIZE)
			for k in ks:
				imageData[:, int(2*(abs(MINY) + k)), 0] = 1
			if tpD != None:
				for tp in tpD:
					Pos_x = tp[0]
					Pos_z = sides[tp[1]] + (1 - 2*tp[1])
					data = image(X, Y, Pos_x, Pos_z, 0, 0)
					if Pos_x <= 95:
						if not (tp[1] == 0 and (rD[3] - 10 < tp[0] < rD[3] + 3) and rD[3] > 0):
							imageData[:, :, 1] += data.reshape(IMAGEHEIGHT, IMAGEWIDTH)
				if (rD[3] > 0):
					imageData[:, :, 1] += image(X, Y, rD[3] - 1.5, sides[0] + 1,  0, 0).reshape(IMAGEHEIGHT, IMAGEWIDTH)
			if riverD[0] == True:
				riverPos = riverD[1]
				up, down = int(riverPos*2 + RIVERSIZE - 2*MINX), int(riverPos*2 - RIVERSIZE - 2*MINX)
				imageData[down : up, :, 2] = 1
				left, right = int(2*(abs(MINY) + ks[0]))-SIDEWALKSIZE, int(2*(abs(MINY) + ks[len(ks)-1]))+SIDEWALKSIZE
				imageData[down : up, left : right, 2] = 0

			imageData.reshape((-1, IMAGEWIDTH, IMAGEHEIGHT, INPUTCHANNELS3)).astype(np.float32)
			for i in range(INPUTCHANNELS3):
				soma = sum(sum(imageData[:, :, i]))
				if soma == 0:
					soma = 1
				imageData[:, :, i] /= soma
			
			returnImages.append(imageData)
		
	elif (inputNum == 4):
		'''
		Input 4
				MainCar Passengengers 	- 	1 channel
		'''
		for passNum in data:
			imageData = [5.0/IMAGEWIDTH if (IMAGEWIDTH/5.0)*(passNum - 1) <= pn <=(IMAGEWIDTH/5)*passNum else 0 for pn in range(IMAGEWIDTH)]
			imageData = np.array(imageData).astype(np.float32)
			imageData /= sum(imageData)
			returnImages.append(imageData)

	elif (inputNum == 5):
		'''
		Input 5
				MainCar Velocity 	- 	1 channel
		'''
		for mcV in data:
			imageData = [0.3989422804/VARIANCEMAINCARVELOCITY*exp(-0.5*((x - mcV*3.6)/VARIANCEMAINCARVELOCITY)**2) for x in range(IMAGEWIDTH*2)] #IMAGEWIDTH/MAXVELOCITY no lugar de 3.6
			imageData = np.array(imageData).astype(np.float32)
			imageData /= sum(imageData)
			returnImages.append(imageData)

	returnImages = np.array(returnImages).astype(np.float32)

	'''if len(returnImages.shape)>3 and inputNum==3:
		for i in range(returnImages.shape[0]):
			for j in range(returnImages.shape[3]):
				pI = returnImages[i,:,:,j]
				plt.figure()
				plt.subplot()
				plt.title(inputNum)
				plt.imshow(pI, cmap = 'gray')
				ax = plt.gca()
				plt.colorbar()
				plt.show()'''
	return returnImages

def image(X, Y, xo, yo, v, o, car = False):
	a = v
	if car:
		std = (1.5 + 0.9*v)
	else:
		std = 1*(1 + 1.5*v)
	Z1 = skewnorm.pdf(Y, a, scale = std, loc = (MINX + MAXX)/2)
	Z2 = norm.pdf(X, scale = 1, loc = (MAXY + MINY)/2)
	Z = np.multiply(Z1, Z2)
	num_cols, num_rows = IMAGEWIDTH, IMAGEHEIGHT
	xs, ys = (MAXY + MINY) + 2*yo, 2*xo - (MINX + MAXX)
	rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), o, 1)
	img_rotation = cv2.warpAffine(Z, rotation_matrix, (num_cols, num_rows))
	translation_matrix = np.float32([[1, 0, xs], [0, 1, ys]])
	img_translation = cv2.warpAffine(img_rotation, translation_matrix, (num_cols, num_rows))
	soma = sum(sum(img_translation))
	if soma == 0:
		soma = 1
	image = img_translation/soma
	if car:
		gain = 0.01/image.max()
		image *= gain
	return image #img_translation/soma

'''
fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(X, Y, 20*img_translation, color='b', antialiased=True)
	plt.show()
	return image #img_translation/soma



Y  =  np.linspace(MINX, MAXX, 1000)
X  =  np.linspace(MINY, MAXY,  1000)
X, Y = np.meshgrid(X, Y)
image(X, Y, -10, 20, 10, 60)
'''