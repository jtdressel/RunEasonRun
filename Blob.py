from root import *
from EsAnimation import *
from EsSounds import *
from EsTimer import *
from EsFunctions import *

class Blob(pygame.sprite.Sprite):

	def __init__(self, pos, width):

		pygame.sprite.Sprite.__init__(self)
		self.images = loadSprites('digits.png', -1, 26, 420)
		self.rect = self.images[0].get_rect()
		self.image = self.images[0]

		self.x, self.y = pos
		self.v_x, self.v_y = 0, 0
		self.a_x, self.a_y = 0, 0
		self.width = width
		self.vec = EsVector(0, 0)
		self.velocity = v_w

		self.circuit = False

	def isRight(self):
		if self.x == self.width:
			return True
		return False

	def isLeft(self):
		if self.x == 0:
			return True
		return False

	def moveLeft(self):
		if self.isRight():
			self.reset()
			self.vec.add(-2, 0)
	
	def moveRight(self):
		if self.isLeft():
			self.reset()
			self.vec.add(2, 0)

	def reset(self):
		self.vec.reset(0,0)

	def getVelocity(self):
		self.moveLeft()
		self.moveRight()
		self.v_x = self.velocity * self.vec.x

	def move(self):
		t = 1
		s_x = self.v_x * t + self.a_x * t * t / 2
		s_y = self.v_y * t + self.a_y * t * t / 2
		self.v_x = self.v_x + self.a_x * t
		self.v_y = self.v_y + self.a_y * t
		self.y += s_y
		self.x += s_x

	def update(self):

		self.getVelocity()
		self.move()
		self.rect.topleft = self.x, self.y

	def draw(self, screen):
		screen.blit(self.image, self.rect)