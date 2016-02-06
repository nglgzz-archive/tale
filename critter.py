"""
	Critter class
	a critter is an intelligent creature equipped with a brain, 
	some energy and a learning algorithm
"""
from settings import Critter_s		# used for critter parameters and functions
from settings import Environment_s	# used for bounds control and for grid constants
from brain    import Brain 			# used for critter's brain


class Critter:
	def __init__(self, pos):
		"""
			Initializes a critter creating his brain, setting
			his energy and age using the settings functions
			and assigning it the given position

			Parameter pos is a tuple with the coordinates 
			of the critter in the world 
		"""
		self.brain  = Brain()
		self.energy = Critter_s.start_energy()
		self.age    = Critter_s.start_age()
		self.pos = pos

	def process(self, world, partners = None):
		"""
			Moves this critter, makes this critter learn and 
			returns list of children from the available partners that this
			critter decided to mate with

			Parameter world is a grid (environment.Grid) of the world
			Parameter partners is a list of critters available for mating
		"""
		sub = world.sub_grid(self.pos)

		inputs  = sub.values + [self.energy]		# list composed by what the critter sees plus its energy
		outputs = self.brain.process(inputs, 0)		# list of four values indicating the movement
		action  = parse_move(outputs)				# resulting movement vector obtained from the outputs 

		best = evaluate_move(sub, outputs)	# evaluate the best possible move
		self.brain.learn(inputs, best, 0)	# make the critter learn in case he took the wrong direction 

		# assign new position
		new_pos = [0, 0] 
		new_pos[0] = max(0, min(self.pos[0] + action[0], Environment_s.width -1))
		new_pos[1] = max(0, min(self.pos[1] + action[1], Environment_s.height -1))

		# decrease energy and increase age
		if new_pos != self.pos:
			self.energy -= Critter_s.move_cost
		else:
			self.energy -= Critter_s.stand_cost
		self.age += 1

		# move if the new position isn't occupied
		if world.access_value(new_pos[0], new_pos[1]) != Environment_s.grid_crit:
			self.pos = tuple(new_pos)
		#ToDo decide if stay, push or kill

		children = []
		if partners != None and self.age >= Critter_s.min_mate_age and self.energy >= Critter_s.mate_cost:				# if this critter is in condition to mate...
			for partner in partners:
				partner_constraints = partner.age >= Critter_s.min_mate_age2 and partner.energy >= Critter_s.mate_cost2

				inputs = [partner.energy, partner.age, self.energy]
				mate_decision = round(self.brain.process(inputs, 1)[0])

				if partner_constraints and mate_decision:																# ...the partner is in condition to mate,
					children.append(self.crossover(partner))															# and this critter wants to, then they mate 
		return children

	def crossover(self, partner):
		"""
			Returns the critters' child and decreases energy to
			this critter and the partner

			Parameter partner is the critter's partner
		"""
		self.energy    -= Critter_s.mate_cost
		partner.energy -= Critter_s.mate_cost2

		child = Critter(Critter_s.randpos())
		child.brain = self.brain.crossover(partner.brain)
		return child

	def copy(self):
		"""
			Returns a copy of this critter
		"""
		critter = Critter(self.pos)
		critter.brain  = self.brain.copy()
		critter.energy = self.energy
		critter.age    = self.age
		return critter

	def eat(self, food = Environment_s.def_food):
		"""
			Increases energy depending on the food type

			Parameter food is the food type, the constants are on the settings. Leave blank for deafult food
		"""
		self.energy += Critter_s.food_reward[food]

	def collide(self):
		"""
			Decreases energy on collision
		"""
		self.energy -= Critter_s.coll_cost
		# ToDo different kind of collisions 

	def is_dead(self):
		"""
			Checks this critter's pulse and returns whether or not his heart has stopped
		"""
		return self.energy <= 0

	def __str__(self):
		"""
			Override of the __str__ function
			used when printing or converting
			Critter to str
		"""
		return "age: " + str(self.age) + " energy: " + str(self.energy) + " position: " + str(self.pos)


def parse_move(outputs):
	"""
		Parses the outputs from the brain to a valid movement vector
	
		Parameter outputs is the list of outputs from 
		the movement neural network (e.g. [0.213, 0.943, 0.786, 0.162])
	"""
	actions = ((0,1), (0,-1), (1,0), (-1,0))
	res = [0, 0]

	for i in range(len(actions)):
		if round(outputs[i]):
			res[0] += actions[i][0]
			res[1] += actions[i][1]
	return res

def parse_action(action):
	"""
		Parses the movement vector to a list of outputs

		Parameter action is the movement vector
	"""
	res = [0, 0, 0, 0]

	if action[1] >= 0:
		res[0] = 1
	if action[1] <= 0:
		res[1] = 1

	if action[0] >= 0:
		res[2] = 1
	if action[0] <= 0:
		res[3] = 1

	return res

def evaluate_move(grid, outputs):
	"""
		Returns the best move the critter could have done

		Parameter grid is a grid (environment.Grid) of the critter's view 
		Parameter outputs is a list of outputs from the brain
	"""
	food = grid.get_type(Environment_s.grid_food)
	action = parse_move(outputs)

	pos = (Critter_s.sight, Critter_s.sight)
	new_pos = (action[0] + pos[0], action[1] + pos[1])

	if (new_pos in food) or (food == []):
		return outputs

	min_f = food[0]
	for f in food:
		if abs_manhattan(f,pos) < abs_manhattan(min_f, pos):
			min_f = f 

	best = [min_f[0] - pos[0], min_f[1] - pos[1]]
	best[0] = max(-1, min(1, best[0]))
	best[1] = max(-1, min(1, best[1]))
	return parse_action(best)

def abs_manhattan(pos0, pos1):
	"""
		Returns the absolute manhattan distance between two points

		Parameters pos0 and pos1 are tuples indicating a position
	"""
	return abs(pos0[0] - pos1[0]) + abs(pos0[1] - pos1[1])
