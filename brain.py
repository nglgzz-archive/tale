"""
	Brain class
	a brain is a container for neural networks with higher level
	functions, such as crossover, mutate, save and load
"""
from neural import NeuralNetwork	# used to create the neural networks contained in the brain
from settings import Brain_s		# used for neural networks creation and mutation parameters 
from random import choice			# used on mutation and crossover
from random import random			# used to randomly select weights and biases on mutation
from pickle import dump, load 		# used to save and load a brain


class Brain:
	def __init__(self):
		"""
			Initializes a brain creating the neural networks contained in it
		"""
		self.n_anns = Brain_s.n_anns
		self.anns = []

		for i in range(self.n_anns):
			self.anns.append(NeuralNetwork(Brain_s.sizes[i]))

	def process(self, inputs, index):
		"""
			Parameter inputs is a list of the inputs of the neural network
			Parameter index is the index of the neural network

			Returns the outputs of the neural network of index index
		"""
		outputs = self.anns[index].activate(inputs)
		return outputs

	def learn(self, inputs, targets, index):
		"""
			Updates the neural network using backpropagation

			Parameter inputs is a list of the inputs of the neural network
			Parameter targets is a list of the desired outputs from the inputs
			Parameter index is the index of the neural network
		"""
		self.anns[index].update_network(inputs, targets, Brain_s.learning_rate[index])

	def mutate(self):
		"""
			Mutates the weights and biases of all the networks in the brain
			based on the probabilities on the settings
		"""
		for i in range(self.n_anns):
			weights = self.anns[i].get_weights()

			for k in range(len(weights)):					# mutate weights
				if random() <= Brain_s.mut_prob[i]:
					weights[k] += random() * choice([-1, 1])
			self.anns[i].set_weights(weights)

			biases = self.anns[i].get_biases()

			for k in range(len(biases)):					# mutate biases
				if random() <= Brain_s.mut_prob[i]:
					biases[k] += random() * choice([-1, 1])
			self.anns[i].set_biases(biases)

	def copy(self):
		"""
			Returns a copy of this brain
		"""
		brain = Brain()					# create a new brain

		for i in range(self.n_anns):	# copy the neural networks
			weights = self.anns[i].get_weights()
			biases = self.anns[i].get_biases()




			brain.anns[i].set_weights(weights)
			brain.anns[i].set_biases(biases)
		return brain

	def crossover(self, partner):
		"""
			Returns the child from this brain and the partner
			the child has weights and biases from the parents and
			a mutation

			Parameter partner is the partner's Brain 
		"""
		brain = Brain()

		for i in range(self.n_anns):
			weights = [self.anns[i].get_weights(), partner.anns[i].get_weights()]
			biases  = [self.anns[i].get_biases() , partner.anns[i].get_biases() ]
			
			child_weights = []
			child_biases  = []

			for k in range(len(weights[0])):
				child_weights.append(weights[choice([0,1])][k])
			

			for k in range(len(biases[0])):
				child_biases.append(biases[choice([0,1])][k])

			brain.anns[i].set_weights(child_weights)
			brain.anns[i].set_biases (child_biases )
		brain.mutate()
		return brain

	def save(self, path):
		"""
			Saves this brain in the given path in the form
			of a list of tuples (weights, biases) of each neural 
			network

			Parameter path is a string indicating the save location
		"""
		try:
			dna = []
			for ann in self.anns:
				dna.append((ann.get_weights(), ann.get_biases()))

			file_obj = open(path, "w")
			dump(dna, file_obj)
			file_obj.close()
		except Exception:
				print "Couldn't save!"
				return Exception

	def load(self, path):
		"""
			Loads the brain from the given path to this brain

			Parameter path is a string inidvating the location 
			of the brain to load
		"""
		try:
			file_obj = open(path, "r")
			dna = load(file_obj)
			file_obj.close()

			for i in range(self.n_anns):
				self.anns[i].set_weights(dna[i][0])
				self.anns[i].set_biases(dna[i][1])
		except Exception:
			print "Couldn't load!"
			return Exception
