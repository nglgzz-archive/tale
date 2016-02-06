"""
	Grid and Food classes
	grid is a rappresentation of the space in the world, or part of it
	food is a class to store and manage the sources of energy of the critters
"""
from settings import Environment_s	# used for food position calculaiton, food and grid constants
from settings import Critter_s		# used for critters sight range on subgrid


class Grid:
	def __init__(self, width, height):
		"""
			Initializes a grid of given sizes with the constant for void found on settings

			Parameter width is the width of the grid
			Parameter height is the height of the grid
		"""
		self.width  = width
		self.height = height
		self.values = [Environment_s.grid_void] * width * height

	def get_type(self, t):
		"""
			Returns a list of all the positions (tuples) containing
			the given type

			Parameter t is the type to search through the grid 
		"""
		l = []
		for i, x in enumerate(self.values):
			if x == t:
				l.append(self.index_to_pos(i))
		return l

	def set_value(self, x, y, value):
		"""
			Sets the given value on the given position in the grid

			Parameter pos is a tuple expressing the position
			Parameter value is the value to assign
		"""
		self.values[self.pos_to_index((x, y))] = value

	def access_value(self, x, y):
		"""
			Returns the value on the given position

			Parameter pos is a tuple expressing a position
		"""
		return self.values[self.pos_to_index((x, y))]

	def sub_grid(self, pos):
		"""
			Returns a grid representing the view of the critter

			Parameter pos is a tuple representing the position of the critter
		"""
		length =Critter_s.sight * 2 + 1
		start = [pos[0]-Critter_s.sight, pos[1]-Critter_s.sight]
		sub = Grid(length, length)

		for i in range(length):
			for k in range(length):
				if (start[0]+k < 0) or (start[0]+k > self.width-1) or (start[1]+i < 0) or (start[1]+i > self.height-1):
					value = Environment_s.grid_out
				else:
					value = self.access_value(start[0]+k, start[1]+i)
				sub.set_value(k, i, value)
		return sub

	def index_to_pos(self, index):
		"""
			Converts the index of a list in a tuple expressing
			a posiiton 

			Parameter index is the index to convert
		"""
		return (index%self.width, index/self.width)

	def pos_to_index(self, pos):
		"""
			Converts a tuple expressing a position to the index
			of a list

			Parameter pos is the tuple to convert
		"""
		return pos[0] + pos[1] * self.width

	def __str__(self):
		"""
			Override of the __str__ function
			used when printing or converting
			Grid to str
		"""
		s = ""
		for i in range(self.height):
			for k in range(self.width):
				s += Environment_s.grid_print[self.access_value(k, i)]
			s += "\n"
		return s


class Food:
	def __init__(self, quantity):
		"""
			Initializes food creating a dictionary with tuple positions as keys and 
			food types as values

			Parameter quantity is the ammount of food to generate
		"""
		self.food = {}

		for i in range(quantity):
			self.food[Environment_s.foodpos()] = Environment_s.def_food

	def add(self, quantity, position = None, world_age = None, food_type = Environment_s.def_food):
		"""
			Generates one of food in a determined position or [quantity] of the given type
			on the position returned by the function on the settings
		"""
		if position != None:
			self.food[position] = food_type
			return

		for i in range(quantity):
			position = Environment_s.foodpos(world_age)
			self.food[position] = food_type