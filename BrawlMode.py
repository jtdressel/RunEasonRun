"""
BrawlMode class
"""

from root import *
from modes import *
from EsAnimation import *
from BrawlEason import *
from Floor import *
from Stupid import *
from Board import *
from Background import *

class BrawlMode(GameMode):
	background = pygame.Surface(size)
	attack_sounds = []

	def __init__(self):
		GameMode.__init__(self)
		self.eason = BrawlEason( (300,300) )
		self.background = Background('demoStreet.png')
		for i in range(4):
			name = 'punch' + str(i) + '.wav'
			BrawlMode.attack_sounds.append(load_sound(name))
			BrawlMode.attack_sounds[i].set_volume(sound_volume)
		self.enemies_defeated = 0
		self.eason.stand()

	def enter(self):
		## initializations when entering this mode

		#load music here
		self.eason.reset()

		#don't need floors?
		self.joes = []
		self.eason.stand()
		self.eason.update()

	def exit(self):
		#kills music whenever we set it up
		self.joes = []
		pygame.mouse.set_visible(True)

	def key_down(self, event):
		##check for input
		##WASD input for movement
		moveSpeed = 5
		x = 0
		y = 0
		if event.key == K_ESCAPE:
			self.switch_to_mode('menu_mode')
		keys = pygame.key.get_pressed()
		if keys[K_w]:
			y = -moveSpeed
		if keys[K_a]:
			x = -moveSpeed
		if keys[K_d]:
			x = moveSpeed
		if keys[K_s]:
			y = moveSpeed
		else:
			self.eason.stand()

		movement = (x,y)
		self.eason.run(movement)

	def spawn_enemy(self):
		pass

	def battle(self):
		for i in self.joes:
			if (not i.isDead() ) and self.eason.hit(i):
				i.die()
				self.eason.expUp()
			if (not i.isDead() ) and i.hit(self.eason):
				if not self.eason.isDead():
					i.attack()
					self.eason.gameOver()

	def check_death(self, clock):
		if self.eason.isDead():
			self.eason.gameOver()

	def update(self, clock):
		self.battle()
		self.check_death(clock)
		self.eason.update()
		#self.background.update()

	def draw(self, screen):
		self.background.draw(screen)
		# for i in self.joes:
		# 	screen.blit(i.image, i.rect)
		screen.blit(self.eason.image, self.eason.rect)
		pygame.display.flip()
