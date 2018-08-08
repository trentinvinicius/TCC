import tensorflow as tf
import pickle
import sys
import os
from constants import *
from random import randint, shuffle
import numpy as np
import json
from createImages import createImages

def createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, riverInfo, name, visualization, test, parameters = [0, 0, 0, 0, 0]):
	msg = {"mainCarInfo": mainCarInfo, "roadInfo": roadInfo, "peopleInfo": peopleInfo, "otherCarsInfo": otherCarsInfo, "treepoleInfo": treepoleInfo, \
		   "animalInfo": animalInfo, "parameters": parameters, "name": name, "test" : test, "visualization" : visualization, 'riverInfo': riverInfo}
	return json.JSONEncoder().encode(msg)

class CNN():
	def __init__(self, filename):
		self.foldername = 'Generalizations/' + filename
		comand = 'mkdir ' + 'Generalizations/' + filename
		os.system(comand)
		self.folder_to_save_validations = 'Generalizations/' + filename + '/Validation'
		comand = 'mkdir ' + self.folder_to_save_validations
		os.system(comand)
		self.load_filename = 'Solutions/' + filename
		self.save_modelname = 'Generalizations/' + filename + '/' + filename + '.ckpt'
		self.save_loss = 'Generalizations/' + filename + '/' + filename + '_lossesVector.txt'
		self.validation_vector_file = 'Generalizations/' + filename + '/' + 'validationvector.txt'
		self.saveLogs = 'Generalizations' + filename + '/data/logs/v1'
		self.training_dataset = {}
		self.validation_dataset = {}
		try:
		   with open(self.save_loss, 'rb') as inputfile:
		      self.loss_values = pickle.load(inputfile)
		except:
		   self.loss_values = []
		self.loadData()

	def loadData(self):
		try:
			with open(self.load_filename, 'rb') as inputFile:
				solutions = pickle.load(inputFile)
		except:
			print "Sorry, could not load file."
			sys.exit()
		aux_dataset = {}
		aux_tr = 0
		aux_va = 0
		for value in solutions:
			try:
				solution = [float(value['solution'][0])/MAXBRAKEFORCE, float(value['solution'][1])/MAXAMPLITUDE, float(value['solution'][2])/MAXFREQUENCY, value['solution'][3], float(value['solution'][4])/MAXDELAY] if value['solution'] is not None else None
				dict_aux = {'simData': value['simData'], 'solution': solution}
				if value['simName'] == 'ValidationAndTest':
					self.validation_dataset[aux_va] = dict_aux				
					aux_va += 1
				else:		
					self.training_dataset[aux_tr] = dict_aux
					aux_tr += 1
			except:
				pass
		self.validationsize = aux_va
		try:
			with open(self.validation_vector_file, 'rb') as val_file:
				self.validation_vector = pickle.load(val_file)
		except: 
			self.validation_vector = []
			while len(self.validation_vector) < 10:
				x = randint(0, aux_va)
				if x not in self.validation_vector:
					self.validation_vector.append(x)
			with open(self.validation_vector_file, 'wb') as val_file:
				pickle.dump(self.validation_vector, val_file)
			  			
	def separateDataset(self, dataset, image):
		'''
		Input 1:
				people, animal, crosswalk, semaphore status - 9 channels
		Input 2:
				otherCars - 1 channel
		Input 3:
				road, treepole  -  2 channels
		Input 4:
				mainCar passengers  -  1 channel
		Input 5:
				mainCar velocity  -  1 channel
		'''
		input1, input2, input3, input4, input5, labels = [], [], [], [], [], []

		for e, k in enumerate(dataset):
			try:
				mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo, riverInfo = dataset[k]['simData']
			except:
				mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo = dataset[k]['simData']
				riverInfo = [False, 0]
			input1.append([peopleInfo, animalInfo, roadInfo])
			input2.append(otherCarsInfo)
			input3.append([roadInfo, treepoleInfo, riverInfo])
			input4.append(mainCarInfo[0])
			input5.append(mainCarInfo[1])
			labels.append(dataset[k]['solution'])

		if (image):
			return createImages(input1, 1), createImages(input2, 2), createImages(input3, 3), createImages(input4, 4), createImages(input5, 5), labels
		else:
			return input1, input2, input3, input4, input5, labels

	def accuracy(self, predictions, names, type, step):
		if type == 'training':
			dataset = self.training_dataset
		else:
			dataset = self.validation_dataset
		acc = 0
		solution_file = []
		for j in range(BATCHSIZE):
			parameters = [max(predictions[j][0]*MAXBRAKEFORCE, MAXBRAKEFORCE), max(predictions[j][0]*MAXAMPLITUDE, MAXAMPLITUDE), max(predictions[j][0]*MAXFREQUENCY, MAXFREQUENCY), 0 if predictions[j][3] < 0.5 else 1, max(predictions[j][4]*MAXDELAY, MAXDELAY)]
			simData = dataset[names[j]]['simData']
			solution_file.append({'simData': simData, 'parameters': parameters})
			acc +=  self.evaluate(simData, parameters)
		file = self.folder_to_save_validations + '/validation_step_' + str(step)
		with open(file, "wb") as out:
			pickle.dump(solution_file, out)
  		return acc/BATCHSIZE

  	def evaluate(self, simData, parameters):
		try:
			mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo, riverInfo = simData
		except:
			mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo = simData
			riverInfo = [False, 0]
		try:
			jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, riverInfo, 'Test', False, False, parameters)
			FILEWRITE = 'jsonParamatersnn' + '.txt'
			FILEREAD = 'fitnessnn' + '.txt'
			with open(FILEWRITE, 'w') as outfile:
				json.dump(jsonParameters, outfile)
			call = 'python callSim.py ' + 'nn'
			os.system(call)
			with open(FILEREAD) as data:
				jsonResult = json.load(data)
			result = json.JSONDecoder().decode(jsonResult)
			colissions, _, _, __ = result
			done = True
			for c in colissions:
				if ("Person" in c['geomName']):
					done = False
			return 1 if done else 0
		except:
			return 0

	def run(self):
		#training
		training_dataset_input1, training_dataset_input2, training_dataset_input3, training_dataset_input4, \
		training_dataset_input5, training_labels = self.separateDataset(self.training_dataset, False)

		#validation
		valid_input1, valid_input2, valid_input3, valid_input4, valid_input5, valid_labels = self.separateDataset(self.validation_dataset, False)

		DESVIO = 0.01

		graph = tf.Graph()

		with graph.as_default():

		  # Input data
		  # Placeholders for the training set
		  tf_train_input1 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS1), name = "tf_train_input1")
		  tf_train_input2 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS2), name = "tf_train_input2")
		  tf_train_input3 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS3), name = "tf_train_input3")
		  tf_train_input4 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEWIDTH), name = "tf_train_input4")
		  tf_train_input5 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEWIDTH*2), name = "tf_train_input5")
		  tf_train_labels = tf.placeholder(tf.float32, shape=(BATCHSIZE, 5), name = "tf_train_labels")

		  # Placeholders for the validation set
		  tf_valid_input1 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS1))
		  tf_valid_input2 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS2))
		  tf_valid_input3 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEHEIGHT, IMAGEWIDTH, INPUTCHANNELS3))
		  tf_valid_input4 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEWIDTH))
		  tf_valid_input5 = tf.placeholder(tf.float32, shape=(BATCHSIZE, IMAGEWIDTH*2))	
		  
		  # Variables
		  # input1 - people, animal, crosswalk, status semaphore
		  with tf.name_scope("variaveis_entrada1") as scope:
			  layer1_input1_weights = tf.Variable(tf.truncated_normal([KERNEL1, KERNEL1, INPUTCHANNELS1, DEPTH4], stddev = DESVIO), name = 'w1')
			  layer1_input1_biases = tf.Variable(tf.zeros([DEPTH4]), name = 'b1')
			  layer2_input1_weights = tf.Variable(tf.truncated_normal([KERNEL2, KERNEL2, DEPTH4, DEPTH5], stddev = DESVIO), name = 'w2')
			  layer2_input1_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH5]), name = 'b2')
			  layer3_input1_weights = tf.Variable(tf.truncated_normal([KERNEL3, KERNEL3, DEPTH5, DEPTH6], stddev = DESVIO), name = 'w3')
			  layer3_input1_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH6]), name = 'b3')
			  layer4_input1_weights = tf.Variable(tf.truncated_normal([KERNEL4, KERNEL4, DEPTH6, DEPTH7], stddev = DESVIO), name = 'w4')
			  layer4_input1_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH7]), name = 'b4')
			  layer5_input1_weights = tf.Variable(tf.truncated_normal([3072, NUMHIDDEN1], stddev = DESVIO), name = 'w5') #26880
			  layer5_input1_biases = tf.Variable(tf.constant(1.0, shape=[NUMHIDDEN1]), name = 'b5')
		  # input2 - otherCars
		  with tf.name_scope("variaveis_entrada2") as scope:
			  layer1_input2_weights = tf.Variable(tf.truncated_normal([KERNEL1, KERNEL1, INPUTCHANNELS2, DEPTH1], stddev = DESVIO), name = 'w1')
			  layer1_input2_biases = tf.Variable(tf.zeros([DEPTH1]), name = 'b1')
			  layer2_input2_weights = tf.Variable(tf.truncated_normal([KERNEL2, KERNEL2, DEPTH1, DEPTH2], stddev = DESVIO), name = 'w2')
			  layer2_input2_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH2]), name = 'b2')
			  layer3_input2_weights = tf.Variable(tf.truncated_normal([KERNEL3, KERNEL3, DEPTH2, DEPTH3], stddev = DESVIO), name = 'w3')
			  layer3_input2_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH3]), name = 'b3')
			  layer4_input2_weights = tf.Variable(tf.truncated_normal([KERNEL4, KERNEL4, DEPTH3, DEPTH4], stddev = DESVIO), name = 'w4')
			  layer4_input2_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH4]), name = 'b4')
			  layer5_input2_weights = tf.Variable(tf.truncated_normal([384, NUMHIDDEN2], stddev = 0.1), name = 'w5') #3360
			  layer5_input2_biases = tf.Variable(tf.constant(1.0, shape=[NUMHIDDEN2]), name = 'b5')
		  # input3 - road, treepole
		  with tf.name_scope("variaveis_entrada3") as scope:
			  layer1_input3_weights = tf.Variable(tf.truncated_normal([KERNEL1, KERNEL1, INPUTCHANNELS3, DEPTH2], stddev = DESVIO), name = 'w1')
			  layer1_input3_biases = tf.Variable(tf.zeros([DEPTH2]), name = 'b1')
			  layer2_input3_weights = tf.Variable(tf.truncated_normal([KERNEL2, KERNEL2, DEPTH2, DEPTH3], stddev = DESVIO), name = 'w2')
			  layer2_input3_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH3]), name = 'b2')
			  layer3_input3_weights = tf.Variable(tf.truncated_normal([KERNEL3, KERNEL3, DEPTH3, DEPTH4], stddev = DESVIO), name = 'w3')
			  layer3_input3_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH4]), name = 'b3')
			  layer4_input3_weights = tf.Variable(tf.truncated_normal([KERNEL4, KERNEL4, DEPTH4, DEPTH5], stddev = DESVIO), name = 'w4')
			  layer4_input3_biases = tf.Variable(tf.constant(1.0, shape=[DEPTH5]), name = 'b4')
			  layer5_input3_weights = tf.Variable(tf.truncated_normal([768, NUMHIDDEN3], stddev = DESVIO), name = 'w5') #6720
			  layer5_input3_biases = tf.Variable(tf.constant(1.0, shape=[NUMHIDDEN3]), name = 'b5')		 
		  # general
		  with tf.name_scope("variaveis_totalmente_conectada") as scope:
			  layer1_weights = tf.Variable(tf.truncated_normal([NUMHIDDEN1 + NUMHIDDEN2 + NUMHIDDEN3 + 3 * IMAGEWIDTH, NUMHIDDEN4], stddev = DESVIO), name = 'w')
			  layer1_biases = tf.Variable(tf.constant(1.0, shape=[NUMHIDDEN4]), name = 'b')
		  #output
		  with tf.name_scope("variaveis_saida") as scope:
		  	  output_weights = tf.Variable(tf.truncated_normal([NUMHIDDEN4, 5], stddev = DESVIO), name = 'output_weights')
			  output_biases = tf.Variable(tf.constant(1.0, shape=[5]), name = 'output_biases')
			  	
		  #keep prob dropout
		  keep_prob = tf.placeholder(tf.float32, name = 'keep_prob')
		  global_step = tf.Variable(-1, name = 'global_step', trainable = False)

		  # Model
		  def model(input1Data, input2Data, input3Data, passengerData, velocityData):
		  	# input1
		  	with tf.name_scope("entrada_1") as scope:
				conv = tf.nn.conv2d(input1Data, layer1_input1_weights, [1, 1, 1, 1], padding='VALID'	, name = 'conv1')
				hidden = tf.nn.relu(tf.add(conv, layer1_input1_biases, name = 'add'), name = 'relu1')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool1')

				conv = tf.nn.conv2d(pool, layer2_input1_weights, [1, 1, 1, 1], padding='VALID', name = 'conv2')
				hidden = tf.nn.relu(conv + layer2_input1_biases, name = 'relu2')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool2')

				conv = tf.nn.conv2d(pool, layer3_input1_weights, [1, 1, 1, 1], padding='VALID', name = 'conv3')
				hidden = tf.nn.relu(conv + layer3_input1_biases, name = 'relu3')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool3')

				conv = tf.nn.conv2d(pool, layer4_input1_weights, [1, 1, 1, 1], padding='VALID', name = 'conv4')
				hidden = tf.nn.relu(conv + layer4_input1_biases, name = 'relu4')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool4')

				shape = pool.get_shape().as_list()
				reshape = tf.reshape(pool, [shape[0], shape[1] * shape[2] * shape[3]])
				hiddenInput1 = tf.nn.relu(tf.matmul(reshape, layer5_input1_weights, name = 'fc') + layer5_input1_biases, name = 'relu5')
			
			# input2
			with tf.name_scope("entrada_2") as scope:
				conv = tf.nn.conv2d(input2Data, layer1_input2_weights, [1, 1, 1, 1], padding='VALID', name = 'conv1')
				hidden = tf.nn.relu(tf.add(conv, layer1_input2_biases, name = 'add'), name = 'relu1')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool1')

				conv = tf.nn.conv2d(pool, layer2_input2_weights, [1, 1, 1, 1], padding='VALID', name = 'conv2')
				hidden = tf.nn.relu(conv + layer2_input2_biases, name = 'relu2')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool2')

				conv = tf.nn.conv2d(pool, layer3_input2_weights, [1, 1, 1, 1], padding='VALID', name = 'conv3')
				hidden = tf.nn.relu(conv + layer3_input2_biases, name = 'relu3')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool3')

				conv = tf.nn.conv2d(pool, layer4_input2_weights, [1, 1, 1, 1], padding='VALID', name = 'conv4')
				hidden = tf.nn.relu(conv + layer4_input2_biases, name = 'relu4')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'pool4')

				shape = pool.get_shape().as_list()
				reshape = tf.reshape(pool, [shape[0], shape[1] * shape[2] * shape[3]])
				hiddenInput2 = tf.nn.relu(tf.matmul(reshape, layer5_input2_weights, name = 'fc') + layer5_input2_biases, name = 'relu5')

			# input3
			with tf.name_scope("entrada_3") as scope:
				conv = tf.nn.conv2d(input3Data, layer1_input3_weights, [1, 1, 1, 1], padding='VALID', name = 'conv1')
				hidden = tf.nn.relu(tf.add(conv, layer1_input3_biases, name = 'add'), name = 'relu1')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'poo1')

				conv = tf.nn.conv2d(pool, layer2_input3_weights, [1, 1, 1, 1], padding='VALID', name = 'conv2')
				hidden = tf.nn.relu(conv + layer2_input3_biases, name = 'relu2')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'poo2')

				conv = tf.nn.conv2d(pool, layer3_input3_weights, [1, 1, 1, 1], padding='VALID', name = 'conv3')
				hidden = tf.nn.relu(conv + layer3_input3_biases, name = 'relu3')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'poo3')

				conv = tf.nn.conv2d(pool, layer4_input3_weights, [1, 1, 1, 1], padding='VALID', name = 'conv4')
				hidden = tf.nn.relu(conv + layer4_input3_biases, name = 'relu4')
				pool = tf.nn.max_pool(hidden, [1, 2, 2, 1], [1, 2, 2, 1], padding = 'VALID', name = 'poo4')

				shape = pool.get_shape().as_list()
				reshape = tf.reshape(pool, [shape[0], shape[1] * shape[2] * shape[3]])
				hiddenInput3 = tf.nn.relu(tf.matmul(reshape, layer5_input3_weights, name = 'fc') + layer5_input3_biases, name = 'relu5')
			
			#general
			with tf.name_scope("totalmente_conectada") as scope:
				hidden = tf.concat([hiddenInput1, hiddenInput2, hiddenInput3, passengerData, velocityData], 1, name = 'concat')
				dropout1 = tf.nn.dropout(hidden, keep_prob, name = 'dropout1')
				hidden2 = tf.nn.relu(tf.matmul(dropout1, layer1_weights, name = 'fc') + layer1_biases, name = 'relu')
				dropout2 = tf.nn.dropout(hidden2, keep_prob, name = 'dropout2')

			#output
			with tf.name_scope("saida") as scope:
				output = tf.nn.sigmoid(tf.matmul(dropout2, output_weights, name = 'fc') + output_biases, name = 'sigmoid')
			return output


			
		  # Training computation
		  train_output = model(tf_train_input1, tf_train_input2, tf_train_input3, tf_train_input4, tf_train_input5)
		  
		  with tf.name_scope("MSE") as scope:
		  	loss = tf.losses.mean_squared_error(labels=tf_train_labels, predictions = train_output)
		  tf.summary.scalar('loss', loss)

		  # Optimizer
		  with tf.name_scope("trainer") as scope:
			learning_rate = tf.train.exponential_decay(STARTING_LEARNING_RATE, global_step, 1000, 0.96, staircase=True)
			optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step = global_step)
		  
		  with tf.name_scope("validation") as scope:
		  	validation_output = model(tf_valid_input1, tf_valid_input2, tf_valid_input3, tf_valid_input4, tf_valid_input5)
			  
		  saver = tf.train.Saver()
		  writer = tf.summary.FileWriter(self.saveLogs)
		  merged = tf.summary.merge_all()


		with tf.Session(graph=graph) as session:
		  summary_writer = tf.summary.FileWriter(self.saveLogs, session.graph)
		  tf.global_variables_initializer().run()
		  #print np.sum([np.prod(v.get_shape().as_list()) for v in tf.trainable_variables()])

		  try:
		  	print "Restoring..."
  			saver.restore(session, self.save_modelname)
  			step = global_step.eval()
  			print("Model restore finished, current global step: %d" % step)
		  	writer.add_graph(session.graph)
		  except Exception as e:
		  	step = 0

		  print('Initialized')
		  while step < NUMSTEPS:
			offset = (step * BATCHSIZE) % (len(self.training_dataset) - BATCHSIZE)
			batch_input1 = createImages(training_dataset_input1[offset:(offset + BATCHSIZE)], 1)
			batch_input2 = createImages(training_dataset_input2[offset:(offset + BATCHSIZE)], 2)
			batch_input3 = createImages(training_dataset_input3[offset:(offset + BATCHSIZE)], 3)
			batch_input4 = createImages(training_dataset_input4[offset:(offset + BATCHSIZE)], 4)
			batch_input5 = createImages(training_dataset_input5[offset:(offset + BATCHSIZE)], 5)
			batch_labels = training_labels[offset:(offset + BATCHSIZE)]
			batch_names  = [x for x in range(offset,(offset + BATCHSIZE))]
			feed_dict = {tf_train_input1 : batch_input1, tf_train_input2 : batch_input2, tf_train_input3 : batch_input3 , \
						 tf_train_input4 : batch_input4, tf_train_input5 : batch_input5, tf_train_labels : batch_labels , \
						 keep_prob : DROPOUT_PROB}
			summary, _, l, train_out = session.run([merged, optimizer, loss, train_output], feed_dict=feed_dict)
			print "Loss at step ", step, ": ", l		
			print batch_labels[12], train_out[12]			

			
			if (step % 10 == 0):
				#summary, _ = session.run([merged,optimizer], feed_dict = feed_dict)
				summary_writer.add_summary(summary, step)
				# Saving files
				try:
				  	print "Saving..."
					saver.save(session, self.save_modelname)
				  	print "...done"
				except Exception as e:
				  	print 'Error saving files: ', e
			
			if (step % 500 == 0):
				  validation_accuracy = 0
				  vector = self.validation_vector
				  while len(vector) < BATCHSIZE:
				  	x = randint(0, self.validationsize)
				  	if x not in vector:
				  		vector.append(x)
				  aux1, aux2, aux3, aux4, aux5 = [], [], [], [],[]
				  for v in vector:
				  	aux1.append(valid_input1[v])
				  	aux2.append(valid_input2[v])
				  	aux3.append(valid_input3[v])
				  	aux4.append(valid_input4[v])
				  	aux5.append(valid_input5[v])
				  
			  	  batch_input1 = createImages(aux1, 1)
			  	  batch_input2 = createImages(aux2, 2)
			  	  batch_input3 = createImages(aux3, 3)
			  	  batch_input4 = createImages(aux4, 4)
			  	  batch_input5 = createImages(aux5, 5)
				  batch_names  = vector
				  feed_dict = {tf_valid_input1 : batch_input1, tf_valid_input2 : batch_input2, tf_valid_input3 : batch_input3 , \
					     		  tf_valid_input4 : batch_input4, tf_valid_input5 : batch_input5, keep_prob : 1.0}
				  validation_accuracy = self.accuracy(session.run(validation_output, feed_dict = feed_dict), batch_names, 'valid', step)
				  print('Validation accuracy: %.1f%%' % validation_accuracy)
			step += 1
			  

if __name__ == '__main__':
	try:
		cnn = CNN('solutions_no_hit_withValidation')
		cnn.run()
	except KeyboardInterrupt:
		print "Ending"