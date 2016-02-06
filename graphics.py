from simulation import Simulation 		# used for all the logic part
from settings import Graphics_s			# used for graphical parameters
from settings import Environment_s		# used for world dimensions
from time import sleep 					# used for delay between steps
import pygame

class Display:
	def __init__(self):
		self.width = Environment_s.width * Graphics_s.tile_length
		self.height = Environment_s.height * Graphics_s.tile_length
		self.restart = True

		while self.restart:
			self.sim = Simulation()
			self.restart = False
			self.bg_rendered = False
			self.start()

	def start(self):
		pygame.init()
		screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(Graphics_s.window_title)
		clock = pygame.time.Clock()

		status_exit = False
		move = False
		sleep_time = 0.05
		old_crits = []
		old_food = []

		while not status_exit:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					status_exit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						status_exit  =True
					elif event.key == pygame.K_BACKSPACE:
						self.restart = True
						status_exit = True
					elif event.key == pygame.K_SPACE:
						move = (True, False)[move]
					elif event.key == pygame.K_TAB:
						for line in self.sim.stats():
							print line
						print "\n"
					elif event.key == pygame.K_PLUS:
						sleep_time += 0.05
						print sleep_time
					elif event.key == pygame.K_MINUS:
						sleep_time -= (0.05, 0)[sleep_time < 0.1]
						print sleep_time
					elif event.key == pygame.K_RIGHT:
						old_crits = self.sim.population.keys()
						old_food = self.sim.food.food.keys()
						self.sim.step()
					elif event.key == pygame.K_BACKSLASH:
						cmd = raw_input("insert command:")
						parse_cmd(cmd)
						print cmd
					elif event.key == pygame.K_s:
						for i, critter in enumerate(self.sim.population.values()):
							critter.brain.save(Graphics_s.brain_path + str(i) + Graphics_s.brain_ext)
						print "Saved"
					elif event.key == pygame.K_l:
						for i, critter in enumerate(self.sim.population.values()):
							critter.brain.load(Graphics_s.brain_path + str(i) + Graphics_s.brain_ext)
						print "Loaded"

			if move:
				old_crits = self.sim.population.keys()
				old_food = self.sim.food.food.keys()
				sleep(sleep_time)
				self.sim.step()

			render(screen, self.sim, old_crits, old_food, self.bg_rendered)
			if not self.bg_rendered:
				self.bg_rendered = True 
			pygame.display.update()

		pygame.quit()

def parse_cmd(cmd):
	print "command parsed, lol!"

def render(screen, simulation, old_crits=[], old_food=[], bg_rendered = False):
	tile_rect = (Graphics_s.tile_length, Graphics_s.tile_length)
	if not bg_rendered:
		for i in range(Environment_s.height):
			for k in range(Environment_s.width):
				x_shift = k * Graphics_s.tile_length
				y_shift = i * Graphics_s.tile_length

				image = pygame.transform.scale(Graphics_s.img_bg, tile_rect)
				blit_image(screen, image, x_shift, y_shift)
		print "bg rendered!"

	for pos in old_crits:
		x_shift = pos[0] * Graphics_s.tile_length
		y_shift = pos[1] * Graphics_s.tile_length
		
		image = pygame.transform.scale(Graphics_s.img_bg, tile_rect)
		blit_image(screen, image, x_shift, y_shift)

	for pos, food in zip(simulation.food.food.keys(), simulation.food.food.values()):
		x_shift = pos[0] * Graphics_s.tile_length
		y_shift = pos[1] * Graphics_s.tile_length

		image = pygame.transform.scale(Graphics_s.img_food[food], tile_rect)
		blit_image(screen, image, x_shift, y_shift)

	for pos, crit in zip(simulation.population.keys(), simulation.population.values()):
		x_shift = pos[0] * Graphics_s.tile_length
		y_shift = pos[1] * Graphics_s.tile_length

		if crit.age < 19:
			image = Graphics_s.img_crit[0]
		elif crit.age < 40:
			image = Graphics_s.img_crit[(1,2)[crit.energy < 50]]
		else:
			image = Graphics_s.img_crit[(3,4)[crit.energy < 50]]
		image = pygame.transform.scale(image, tile_rect)
		blit_image(screen, image, x_shift, y_shift)

def blit_image(screen, img, x, y):
	rect = img.get_rect()
	screen.blit(img, (rect[0]+x, rect[1]+y))


if __name__ == '__main__':
	d = Display()
	quit()
