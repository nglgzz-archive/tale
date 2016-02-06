from random import random, randint  # used on randweight, start age and energy
from pygame import image 			# used for images on graphics
import numpy						# used for creating weights

class Graphics_s:
	tile_length = 20
	window_title = "Evolution"
	
	brain_path = "./brains/"
	brain_ext = ".brn"

	img_dir = "images/"
	img_ext = ".png"

	img_crit = [image.load(img_dir + "00" + img_ext), image.load(img_dir + "01" + img_ext), image.load(img_dir + "02" + img_ext), image.load(img_dir + "03" + img_ext), image.load(img_dir + "04" + img_ext)]
	img_food = [image.load(img_dir + "f00" + img_ext), image.load(img_dir + "f01" + img_ext)]
	img_bg = image.load(img_dir + "terrain_bg" + img_ext)

class Simulation_s:
	n_food = 50
	n_crit = 40

class Environment_s:
	width  = 40
	height = 35
	n_crit = 50
	n_food = 35

	grid_crit = 1#0
	grid_food = 2#-10
	grid_void = 3#2
	grid_out  = 4#10
	grid_print = {grid_crit:"O", grid_food:"+", grid_void:" ", grid_out:"#"}
	def_food = 0
	
	@staticmethod
	def foodpos(world_age = None):
		if world_age == None:
			x = randint(0, Environment_s.width-1)
			y = randint(0, Environment_s.height-1)
			return (x, y)
		
		s = ((world_age/250)%4)+1

		if s == 1:
			x = randint(Environment_s.width/2, Environment_s.width-1)
			y = randint(Environment_s.height/2, Environment_s.height-1)
		elif s == 2:
			x = randint(0, Environment_s.width/2)
			y = randint(Environment_s.height/2, Environment_s.height-1)
		elif s == 3:
			x = randint(0, Environment_s.width/2)
			y = randint(0, Environment_s.height/2)
		elif s == 4:
			x = randint(Environment_s.width/2, Environment_s.width-1)
			y = randint(0, Environment_s.height/2)
		return (x, y)

class Critter_s:
	sight = 4
	
	move_cost = 5
	stand_cost = 1
	food_reward = [100, 20]
	coll_cost = 15 # to use

	decision_multiplier = 2	
	min_mate_age = 12
	min_mate_age2 = 5
	mate_cost  = 40 
	mate_cost2 = 20

	@staticmethod
	def start_energy():
		return randint(60,110)
	@staticmethod
	def start_age():
		return randint(0,12)
	@staticmethod
	def randpos():
		return (randint(0,Environment_s.width-1),randint(0,Environment_s.height-1)) #todo fix hardcoded variables

class Brain_s:
	n_anns = 2
	sizes = [[((Critter_s.sight*2+1)**2+1), 5, 4],[3, 2, 1]]
	mut_prob = [0.3,	0.5] 
	learning_rate = [0.6,	0.2]

class Neural_s:
	@staticmethod
	def randweight(y=None, x=None):
		if y == None or x == None:
			return numpy.random.randn()
		return numpy.random.randn(y,x)
	@staticmethod
	def randbias(y=None, x=None):
		if y == None or x == None:
			return numpy.random.randn()
		return numpy.random.randn(y,x)
