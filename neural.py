"""
	Neural network class
	source for backpropagation and network weights' update (http://neuralnetworksanddeeplearning.com/chap1.html) 
"""
from settings import Neural_s		# used to calculate random weights and biases
import numpy						# used for exp function in sigmoid and to do operations between arrays


class NeuralNetwork:
	def __init__(self, sizes):
		"""
			Initializes a neural network with len(sizes) layers of the given sizes. 
			Weights and biases are set randomly.
			[input, hidden... hidden, output]
		"""
		self.sizes = sizes
		self.n_layers = len(sizes)
		self.biases  = [Neural_s.randbias(y, 1) for y in sizes[1:]]
		self.weights = [Neural_s.randweight(y, x) for x, y in zip(sizes[:-1], sizes[1:])]

	def get_weights(self):
		"""
			Returns list of weights
		"""
		weights = []
		for layer in self.weights:
			shape = (1, layer.shape[0]*layer.shape[1])		# shape of current layer
			weights += (layer.reshape(shape)[0]).tolist()	# convert current layer's weights to list
		return weights

	def set_weights(self, weights):
		"""
			Parameter weights is a list of numbers
		"""
		tmp_weights = []
		start = 0
		for layer in self.weights:
			stop = start + len(layer.reshape((1, layer.shape[0]*layer.shape[1]))[0].tolist())
			tmp = numpy.array(weights[start:stop])			# weights in current layer
			tmp_weights.append(tmp.reshape(layer.shape))	
			start = stop
		self.weights = tmp_weights

	def get_biases(self):
		"""
			Returns list of biases
		"""
		biases = []
		for layer in self.biases:
			shape = (1, layer.shape[0]*layer.shape[1])		# shape of current layer
			biases += (layer.reshape(shape)[0]).tolist()	# convert current layer's biases to list
		return biases

	def set_biases(self, biases):
		"""
			Parameter biases is a list of biases
		"""
		tmp_biases = []
		start = 0
		for layer in self.biases:
			stop = start + len(layer.reshape((1, layer.shape[0]*layer.shape[1]))[0].tolist())
			tmp = numpy.array(biases[start:stop])			# biases in current layer
			tmp_biases.append(tmp.reshape(layer.shape))
			start = stop
		self.biases = tmp_biases

	def activate(self, a):
		"""
			Parameter a is a list of inputs
			The function returns a list of outputs
		"""
		a = numpy.rot90(numpy.array([a]))	# create numpy array with the inputs and rotate it to form a 1*n matrix
		for b, w in zip(self.biases, self.weights):
			a = sigmoid(numpy.dot(w, a)+b)	# output of current layer
		a = numpy.rot90(a).tolist()[0]		# rotates the 1*n matrix to n*1 and then convert it to list
		return a

	def update_network(self, x, y, eta):
		"""
			Updates the weights and biases on the network using backpropagation

			Parameter x is a list of inputs
			Parameter y is a list of desired outputs from x
			Parameter eta is a number representing the learning rate
		"""
		x = numpy.rot90(numpy.array([x]))
		y = numpy.rot90(numpy.array([y]))
		nabla_b = [numpy.zeros(b.shape) for b in self.biases]
		nabla_w = [numpy.zeros(w.shape) for w in self.weights]
		
		delta_nabla_b, delta_nabla_w = self.backprop(x, y)

		nabla_b = [nb+dnb for nb,dnb in zip(nabla_b, delta_nabla_b)]
		nabla_w = [nw+dnw for nw,dnw in zip(nabla_w, delta_nabla_w)]

		self.weights = [w-(eta*nw) for w,nw in zip(self.weights, nabla_w)]
		self.biases = [b-(eta*nb) for b,nb in zip(self.biases, nabla_b)]

	def backprop(self, x, y):
		"""
			Returns the difference between the actual weights (and biases) and the 
			weights (and biases) that would return the desired outputs
			
			Parameter x is a numpy array of inputs
			Parameter y is a numpy array of desired outputs from x
		"""
		nabla_b = [numpy.zeros(b.shape) for b in self.biases]
		nabla_w = [numpy.zeros(w.shape) for w in self.weights]
		
		activation = x
		activations = [x]
		zs = []
		for b, w in zip(self.biases, self.weights):
			z = numpy.dot(w, activation)+b # activation number for each layer
			zs.append(z)
			activation = sigmoid(z)			# output for each layer
			activations.append(activation)

		delta = (activations[-1] - y) * sigmoid_prime(zs[-1])
		nabla_b[-1] = delta
		nabla_w[-1] = numpy.dot(delta, activations[-2].transpose())

		for l in xrange(2, self.n_layers):
			z = zs[-l]
			sp = sigmoid_prime(z)
			delta = numpy.dot(self.weights[-l+1].transpose(), delta) * sp
			nabla_b[-l] = delta
			nabla_w[-l] = numpy.dot(delta, activations[-l-1].transpose())
		return (nabla_b, nabla_w)


def sigmoid(activation):
    """
    	Sigmoid function
    	activation function for the neurons' output
    """
    return 1.0/(1.0+numpy.exp(-activation))

def sigmoid_prime(z):
	"""
		Derivative of the sigmoid function
		used in backpropagation
	"""
	return sigmoid(z)*(1-sigmoid(z))
