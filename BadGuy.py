"""
BadGuy class will include attributes and methods for enemies and AI control of them

Children of BadGuy class will have additional abilities not containted in BadGuy
"""
from root import *
from EsAnimation import *
from EsSounds import *
from EsTimer import *

class BadGuy(pygame.sprite.Sprite):
	"""STATUS"""
	WALK, ATK, DEAD, HIT, STAND = range(5)
	RIGHT, LEFT = range(2)
	def __init__(self, pos, up, lo):
		#-----------------------INITIALIZATION---------------------------------
		pygame.sprite.Sprite.__init__(self)
		self.images = loadSprites('0.png', -1, 80, 80)
		self.rect = self.images[0].get_rect()
		
		#-----------------------ATTRIBUTES-------------------------------------
		self.x, self.y = pos
		self.init_x, self.init_y = pos
		self.v_x, self.v_y = 0, 0
		self.a_x, self.a_y = 0, 0
		self.width, self.height = 80, 80
		self.status = None 
		
		#-----------------------ANIMATIONS-------------------------------------
		animList = [self.images[6], self.images[7], self.images[8], \
					self.images[9]]
		self.anim_stand = Animation(animList, 10, True)
		animList = [self.images[19], self.images[18], self.images[17], \
					self.images[16]]
		self.anim_attack = Animation(animList, 10, False)
		animList = [self.images[36], self.images[37], self.images[34], \
					self.images[35]]
		self.anim_dead = Animation(animList, 10, False)
		animList = [self.images[0], self.images[1], self.images[2]]
		self.anim_run = Animation(animList, 10, True)

		self.direction = BadGuy.RIGHT
		self.upperBound, self.lowerBound = up , lo

	def newBound(self, nu, nl):
		self.upperBound, self.lowerBound = nu , nl
	
	def setVelocity(self, vx = None, vy = None):
		if vx != None:
			self.v_x += vx
		if vy != None:
			self.v_y += vy

	def walk(self):
		if self.status == BadGuy.ATK:
			return
		self.status = BadGuy.WALK
		if not self.anim_run.started():
			self.anim_run.start()
		if self.v_x > 0:
			self.direction = BadGuy.RIGHT
		elif self.v_x < 0:
			self.direction = BadGuy.LEFT

	def stand(self):
		if self.status == BadGuy.STAND:
			return
		self.status = BadGuy.STAND
		self.v_x, self.v_y = 0, 0
		self.anim_stand.reset()
		self.anim_stand.start()

	def isMoving(self):
		if self.v_x == 0 and self.v_y == 0:
			return False
		return True

	def isAttack(self):
		if self.status != BadGuy.ATK:
			return False
		return True

	def checkForTarget(self, target):
		pass
		#returns if target is near in terms of x and y directions


	def aiMove(self, target):
		#horizontal = [v_w, -v_w]
		#vertical = [0.8, -0.8]\
		v_x, v_y = None, None
		if self.x < target.x:
			v_x = v_w
		if self.x > target.x:
			v_x = -v_w
		if self.y < target.y:
			v_y = 0.5
		if self.y > target.y:
			v_y = -0.5

		self.setVelocity(v_x, v_y)
	
	def move(self):
		if self.status == BadGuy.ATK:
			return
		t = 1
		s_x = self.v_x * t + self.a_x * t * t / 2
		s_y = self.v_y * t + self.a_y * t * t / 2
		self.v_x = self.v_x + self.a_x * t
		self.v_y = self.v_y + self.a_y * t
		self.y += s_y
		self.x += s_x
		if self.x < -40:
			self.x = -40
		if self.x > width - 40:
			self.x = width - 40
		if self.y > self.lowerBound - 80:
			self.y = self.lowerBound - 80
		if self.y < self.upperBound - 80:
			self.y = self.upperBound - 80

	def update(self):
		#print self.status
		if self.status == BadGuy.WALK:
			self.image = self.anim_run.image
			if self.direction == BadGuy.LEFT:
				self.image = pygame.transform.flip(self.image, 1, 0)
			self.anim_run.update( pygame.time.get_ticks() )

		if self.status == BadGuy.STAND:
			self.image = self.anim_stand.image
			if self.direction == BadGuy.LEFT:
				self.image = pygame.transform.flip(self.image, 1, 0)
			self.anim_stand.update( pygame.time.get_ticks() )

		if self.status == BadGuy.ATK:
			self.image = self.anim_punch.image
			if self.anim_punch.done():
				self.status = BadGuy.STAND
			if self.direction == BadGuy.LEFT:
				self.image = pygame.transform.flip(self.image, 1, 0)
			self.anim_punch.update( pygame.time.get_ticks() )

		if not self.isMoving() and not self.isAttack():
			self.stand()
		else:
			if math.fabs(self.v_x) == v_w:
				self.walk()
			if math.fabs(self.v_x) == v_r:
				self.run()
			if self.v_y:
				if math.fabs(self.v_x) == v_r:
					self.run()
				else:
					self.walk()
		self.move()
		self.rect.topleft = self.x, self.y


