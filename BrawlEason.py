"""
Copy all attributes of BrawlEason to BrawlEason, including animations and sounds
"""
from Eason import *

class BrawlEason(Eason):
	'''REMEMBER EVERY TIME ADD ONE STATUS, ADD ONE NUMBER'''
	RUN, JUMP, ATK, DEAD, DROP, STAND = range(6) #CHANGE/ADD ACTIONS  
	def __init__(self, pos):

		Eason.__init__(self, pos)
		##loads sounds and images from Eason

		#---------------- BRAWL EASON STATS -------------------------------------

		self.v_x = 0
		self.status = BrawlEason.STAND
		self.health = 3
		self.atkDone = True
		#add a special attack atribute later

		#------------------ ADDITIONAL BRAWL ANIMATIONS -------------------------

		self.images = loadSprites('eason0.png', -1, 80, 80) #the other sprite sheet
		animList = [self.images[0], self.images[1], self.images[2], self.images[3]]
		self.anim_stand = Animation(animList, 20, True)

	"""
	Any methods not changed are the same as BrawlEason
	"""

	def reset(self):
		self.setLevel(1)
		self.exp = 0
		self.setPos(pos)
		self.atkDone = True
		self.v_x, self.v_y = 0, 0
		self.a_x, self.a_y = 0, 0

	def run(self, movement): #movement = (v_x , v_y)
		self.status == BrawlEason.RUN
		self.v_x , self.v_y = movement

	def drop(self):
		pass

	def resetStatus(self):
		self.status = BrawlEason.STAND
		self.v_y = 0
		self.a_y = JMP_ACC

	def move(self):
		t = 1
		self.s_x = self.v_x * t + self.a_x * t * t / 2
		s_y = self.v_y * t + self.a_y * t * t / 2
		self.v_x = self.v_x + self.a_x * t
		self.v_y = self.v_y + self.a_y * t
		self.y += s_y
		if self.status == BrawlEason.DEAD:
			return

	def stepOn(self):
		""" Check to see if BrawlEason steps beyond x,y bounds """
		x, y = width, height
		if self.rect.top < y/3 or self.rect.bottom > y:
			return False
		if self.rect.left < 0 or self.rect.right > x:
			return False
		return True

	def stand(self):
		self.status = BrawlEason.STAND
		self.v_x = 0
		self.v_y = 0
		self.a_x = 0
		self.a_y = 0

	def fall(self):
		pass

	def isDead(self):
		return self.status == BrawlEason.DEAD

	def gameOver(self):
		if self.status == BrawlEason.DEAD:
			return
		self.sound_gameover.play()
		self.stop()
		self.status = BrawlEason.DEAD
		self.anim_dead.reset()
		self.anim_dead.start()

	def attack(self):
		pass

	def fixPos(self, y):
		pass

	def atkMove(self):
		if self.x - self.init_x < self.atk_range and not self.atkDone:
			self.x += 19 + self.level
		else:
			self.atkDone = True
			if self.kick:
				self.status = BrawlEason.JUMP
			else:
				self.status = BrawlEason.RUN

	def acting(self):
		if self.status == BrawlEason.ATK:
			return True
		return False

	def hit(self, target):
		if self.status != BrawlEason.ATK and self.status != BrawlEason.DROP:
			return False
		hitbox = self.rect.inflate(-30, -10)
		return hitbox.colliderect(target.rect.inflate(-20, -5)) #Ask Eason about these Values

	def update(self):
		if self.status == BrawlEason.RUN:
			self.image = self.anim_run.image
			self.anim_run.update(pygame.time.get_ticks())

		if self.status == BrawlEason.STAND:
			self.image = self.anim_stand.image
			self.anim_stand.update(pygame.time.get_ticks())
        	    
		if self.status == BrawlEason.JUMP:
			if self.jmp_cnt == 1:
				self.image = self.anim_jmp.image
				self.anim_jmp.update(pygame.time.get_ticks())
			elif self.jmp_cnt == 2:
				self.image = self.anim_jmp2.image
				self.anim_jmp2.update(pygame.time.get_ticks())
        
		if self.status == BrawlEason.DROP:
			self.image = self.anim_DROP.image
			self.anim_DROP.update(pygame.time.get_ticks())
            
		if self.status == BrawlEason.ATK:
			self.image = self.anim_atk.image
			self.anim_atk.update(pygame.time.get_ticks())
			self.atkMove()
            
		if self.status == BrawlEason.DEAD:
			self.image = self.anim_dead.image
			self.anim_dead.update(pygame.time.get_ticks())
        
		if self.status != BrawlEason.DEAD and self.CDtimer.timeUp():
			self.sound_cd.play()
        
		#self.move()
		#self.rect.topleft = self.x, self.y

	