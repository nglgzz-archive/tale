"""
	Simulation class
	a simulation is a way to connect the environment and a population of critters, so that
	they can be managed both at the same time and at a higer level. It also provides methods
	to help making statistics on the population 
"""
from settings import Simulation_s	# used for siulation parameters (i.e. number of critters and food ammount)
from settings import Environment_s	# used for world dimensions and for grid constants
from settings import Critter_s		# used to generate critters' position and for critters' sight range
from environment import Grid 		# used to create the world
from environment import Food 		# used to generate, store and manage food
from critter import Critter 		# used to populate the world


class Simulation:
	def __init__(self):
		"""
			Initializes a simulation creating the world (which is a grid),
			creating a dictionary of critters, the keys are tuples representing the positions
			and the values are the critters, spawning food and then syncing everything with the
			world
		"""
		self.world = Grid(Environment_s.width, Environment_s.height)
		self.world_age = 0

		self.population = {}
		for i in range(Simulation_s.n_crit):
			c = Critter(Critter_s.randpos())
			self.population[c.pos] = c

		self.food = Food(Simulation_s.n_food)
		self.sync()

	def sync(self):
		"""
			Overlaps the current grid world with the updated one
		"""
		self.world = Grid(Environment_s.width, Environment_s.height)

		for pos in self.food.food:
			self.world.set_value(pos[0], pos[1], Environment_s.grid_food)

		for pos in self.population.keys():
			self.world.set_value(pos[0], pos[1], Environment_s.grid_crit)

	def step(self):
		"""
			Makes the population move by one step, reproduce according to the constraints and
			will, increase world's age, spawn new food and update the world
		"""
		children = []
		critters = self.population.values()
		old_pos  = self.population.keys()
		
		for crit in critters:
			self.world.set_value(crit.pos[0], crit.pos[1], Environment_s.grid_void)	# clear the space on the world 
			
			sub = self.world.sub_grid(crit.pos)						# critter's view
			partners_pos = sub.get_type(Environment_s.grid_crit)	# relative position of the potential partners
			partners = []											# potential partners

			for pos in partners_pos:
				pos = (crit.pos[0]+pos[0] - Critter_s.sight, crit.pos[1]+pos[1] - Critter_s.sight)	# absolute position of the partner
				partners.append(self.population[pos])

			old_pos  = crit.pos
			children += crit.process(self.world, partners)

			if self.food.food.has_key(crit.pos):
				crit.eat(self.food.food.pop(crit.pos))	# removes the food from the food list and increments the energy of the critter
				self.world.set_value(crit.pos[0], crit.pos[1], Environment_s.grid_void) # removes the food from the world

			self.population.pop(old_pos)	# removes critter from old position
			if not crit.is_dead():
				if self.population.has_key(crit.pos):
					crit.pos = old_pos				# if the new position is occupied by another critter don't move
				self.population[crit.pos] = crit 	# set critter in the new (or old) position
				self.world.set_value(crit.pos[0], crit.pos[1], Environment_s.grid_crit)	# updates the world 

		self.add_children(children)				# add children in the population list
		self.world_age += 1						# increments world's age
		self.food.add(1, None, self.world_age)	# spawns randomly 1 food
		self.sync()

	def add_children(self, children):
		"""
			Adds the given children on the population list of the simulation

			Parameter children is a list of critters
		"""
		for child in children:
			if not self.population.has_key(child.pos):
				self.population[child.pos] = child

	def min_stat(self, field):
		"""
			Returns the critter with the lowest value of field
			or None if the population is empty

			Parameter field is a string indicating the attribute to compare
		"""
		l = [(getattr(c, field), c) for c in self.population.values()] # tuples with (value, critter)
		return min((l, [(None, None)])[l == []])[1]

	def max_stat(self, field):
		"""
			Returns the critter with the highest value of field
			or None if the population is empty

			Parameter field is a string indicating the attribute to compare
		"""
		l = [(getattr(c, field), c) for c in self.population.values()] # tuples with (value, critter)
		return max((l, [(None, None)])[l == []])[1]
		
	def sum_stat(self, field):
		"""
			Returns the sum of the values in field of the whole population 
			or 0 if the population is empty

			Parameter field is a string indicating the attribute to sum
		"""
		l = [getattr(c, field) for c in self.population.values()] # list of values
		return sum((l, [0])[l == []])
		
	def average_stat(self, field):
		"""
			Returns the average of the values in field of the whole population
			or 0 if the population is empty

			Parameter field is a string indicating the attribute to average
		"""
		return float(self.sum_stat(field))/(len(self.population), 1)[len(self.population) == 0]

#########temporary until new gui#############
	def stats(self):
		"""
			Statistics sample
			Returns a string with some informations about the world and about the population
		"""
		max_energy = self.max_stat("energy")
		min_energy = self.min_stat("energy")
		oldest = self.max_stat("age")
		average_age = self.average_stat("age")
		average_energy = self.average_stat("energy")
	
		if max_energy == None or min_energy == None or oldest == None:
			return ["World age: " + str(self.world_age), 
				 	"Food quantity: " + str(len(self.food.food))]
		stats = [str(len(self.population)) + " critters.",
				 "World age: " + str(self.world_age), 
				 "Food quantity: " + str(len(self.food.food)),
				 "Max energy critter[" + str(max_energy) + "]",
				 "Min energy critter[" + str(min_energy) + "]",
				 "Oldest critter[" + str(oldest) + "]",
				 "Average age: " + str(average_age),
				 "Average energy: " + str(average_energy)
				 ]
		return stats
