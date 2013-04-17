"""
BadGuy class will include attributes and methods for enemies and AI control of them

Children of BadGuy class will have additional abilities not containted in BadGuy
"""
from root import *
from EsAnimation import *
from EsSounds import *
from EsTimer import *
from EsFunctions import *

class BadGuy(pygame.sprite.Sprite):
	"""STATUS"""
	WALK, ATK, DEAD, BEATEN, STAND, FFUCKED, BFUCKED = range(7)
	RIGHT, LEFT = range(2)
	def __init__(self, pos, up, lo, level):
		#-----------------------INITIALIZATION---------------------------------
		pygame.sprite.Sprite.__init__(self)
		#filename = str((level-1) % 3) + '.png'
		self.images = loadSprites('0.png', -1, 80, 80)
		self.rect = self.images[0].get_rect()
		self.attack_sounds = []
		for i in range(4):
			name = 'punch' + str(i) + '.wav'
			self.attack_sounds.append(load_sound(name))
			self.attack_sounds[i].set_volume(sound_volume)
		self.sound_atk = []
		self.sound_atk.append(load_sound('attack0.wav'))
		self.sound_atk.append(load_sound('attack1.wav'))
		
		#-----------------------ATTRIBUTES-------------------------------------
		self.x, self.y = pos
		self.init_x, self.init_y = pos
		self.v_x, self.v_y = 0, 0
		self.a_x, self.a_y = 0, 0
		self.width, self.height = 80, 80
		self.status = None
		self.level = level
		self.direction = BadGuy.LEFT
		self.upperBound, self.lowerBound = up , lo
		self.damage = 0
		self.cd_atk = CDTimer(100)
		self.HP = 100 + 100 * (level - 1)
		self.rect_body = pygame.Rect(0, 0, 27, 57)
		self.cd_hit = CDTimer(20)
		self.cd_action = CDTimer(200)
		self.cd_action.start()
		self.dmg_period = CDTimer(1000)
		self.dmg_taken = 0
		self.deadFlag = False
		self.vec = EsVector(0, 0)
		self.velocity = v_w
		
		#-----------------------ANIMATIONS-------------------------------------
		animList = [self.images[6], self.images[7], self.images[8], \
					self.images[9]]
		self.anim_stand = Animation(animList, 10, True)
		self.anim_attack = []
		animList = [self.images[19], self.images[18]]
		self.anim_attack.append(Animation(animList, 10, False))
		animList = [self.images[17], self.images[16]]
		self.anim_attack.append(Animation(animList, 10, False))
		animList = [self.images[3], self.images[4], self.images[5]]
		self.anim_walk = Animation(animList, 10, True)
		self.anim_beaten = []
		anim = [self.images[10], self.images[11]]
		self.anim_beaten.append(Animation(anim, 16, False))
		anim = [self.images[12], self.images[13], self.images[14]]
		self.anim_beaten.append(Animation(anim, 24, False))
		anim = [self.images[39], self.images[38], self.images[37], self.images[36], \
			self.images[35], self.images[34], self.images[35], self.images[35], \
			self.images[35], self.images[35], self.images[35], self.images[35]]
		self.anim_front_fucked = Animation(anim, 20, False)
		anim = [self.images[49], self.images[48], self.images[47], self.images[46], \
			self.images[45], self.images[44], self.images[45], self.images[45], \
			self.images[45], self.images[45], self.images[45], self.images[45]]
		self.anim_back_fucked = Animation(anim, 20, False)

	def moveLeft(self):
		if self.isDead():
			return
		self.vec.sub(1, 0)
	
	def moveRight(self):
		if self.isDead():
			return
		self.vec.add(1, 0)
	
	def moveUp(self):
		if self.isDead():
			return
		self.vec.sub(0, 1)
	
	def moveDown(self):
		if self.isDead():
			return
		self.vec.add(0, 1)
	
	def isLeft(self):
		return self.direction == BadGuy.LEFT
	
	def isRight(self):
		return not self.isLeft()
	
	def newBound(self, nu, nl):
		self.upperBound, self.lowerBound = nu, nl
	
	def getVelocity(self):
		self.v_x = self.velocity * self.vec.x
		self.v_y = 0.8 * self.vec.y

	def setLevel(self, lv):
		self.level = lv
		self.HP = 100 + 100 * (lv - 1)

	def walk(self):
		if self.status == BadGuy.ATK:
			return
		self.status = BadGuy.WALK
		if not self.anim_walk.started():
			self.anim_walk.start()
	
	def attack(self):
		if self.isDead():
			return 
		if self.cd_atk.isStart() and not self.cd_atk.timeUp():
			return 
		if self.status == BadGuy.DEAD or self.status == BadGuy.ATK:
			return
		self.anim_atk = self.anim_attack[randint(0, 1)]
		self.anim_atk.reset()
		self.anim_atk.start()
		self.sound_atk[randint(0, 1)].play()
		self.status = BadGuy.ATK
		self.damage = 3 + randint(-2, 2) + self.level
		self.cd_atk.setTime(500)

	def stand(self):
		if self.status == BadGuy.STAND:
			return
		self.status = BadGuy.STAND
		self.anim_stand.reset()
		self.anim_stand.start()
		self.damage = 0

	def isMoving(self):
		if self.v_x == 0 and self.v_y == 0:
			return False
		return True

	def isAttack(self):
		if self.status != BadGuy.ATK:
			return False
		return True
	
	def isBeaten(self):
		if self.status == BadGuy.BEATEN:
			if not self.anim_beat.done():
				return True
		return False

	def isFucked(self):
		if self.status == BadGuy.FFUCKED or self.status == BadGuy.BFUCKED:
			if not self.anim_fucked.done():
				return True
		return False

	def isDead(self):
		if self.HP <= 0:
			return True
		return self.status == BadGuy.DEAD

	def isActing(self):
		if self.isBeaten():
			return True
		if self.isAttack():
			return True
		if self.isFucked():
			return True
		return False

	def beaten(self):
		if self.status == BadGuy.BEATEN:
			return 
		self.status = BadGuy.BEATEN
		self.anim_beat = self.anim_beaten[randint(0, 1)]
		self.anim_beat.reset()
		self.anim_beat.start()
		self.attack_sounds[randint(0, 3)].play()

	def die(self):
		self.status = BadGuy.DEAD

	def fucked(self, dir):
		if self.status == BadGuy.FFUCKED or self.status == BadGuy.BFUCKED:
			return
		self.status = dir
		self.anim_fucked = self.anim_front_fucked
		if self.status == BadGuy.BFUCKED:
			self.anim_fucked = self.anim_back_fucked
		self.anim_fucked.reset()
		self.anim_fucked.start()
		self.attack_sounds[randint(0, 3)].play()

	def hit(self, hitbox, damage, x):
		if self.isDead():
			return False
		if self.cd_hit.isStart() and not self.cd_hit.timeUp():
			return False
		self.cd_hit.start()
		if self.dmg_period.isStart() and self.dmg_period.timeUp():
			self.dmg_taken = 0
		self.rect_body.topleft = self.x + 23, self.y + 23
		if hitbox.colliderect(self.rect_body):
			if self.dmg_taken == 0:
				self.dmg_period.start()
			self.dmg_taken += damage
			self.HP -= damage
			if self.HP < 0:
				self.HP = 0
				self.status = BadGuy.DEAD
			if self.dmg_taken < 50 * self.level and self.HP > 0:
				self.beaten()
			else:
				if self.isLeft():
					if x < self.x:
						self.fucked(BadGuy.FFUCKED)
					else:
						self.fucked(BadGuy.BFUCKED)
				else:
					if x < self.x:
						self.fucked(BadGuy.BFUCKED)
					else:
						self.fucked(BadGuy.FFUCKED)
			return True
		return False
	
	def getHitBox(self):
		if self.status != BadGuy.ATK:
			return None
		hitBox = None
		
		if self.anim_atk.image == self.images[16] or self.anim_atk.image == self.images[18]:
			x = 1
			y = 35 + self.y
			if self.isRight():
				x = 80 - x - 12
			x += self.x
			hitBox = pygame.Rect(x, y, 12, 9)
		
		return hitBox
	
	def checkForTarget(self, target):
		if dist((self.x, self.y), (target.x, target.y)) <= self.eyeSight():
			return True
		return False
		#returns if target is near in terms of x and y directions
	def withinRange(self, rg, target):
		if dist((self.x, self.y), (target.x, target.y)) <= rg:
			return True
		return False
	
	def eyeSight(self):
		return 200 + (self.level - 1) * 1.1
	
	def setTarget(self, x, y):
		if x < 0:
			x = 0
		if y < self.upperBound - 80:
			y = self.upperBound - 80
		if x > width - 45:
			x = width - 45
		if y > self.lowerBound - 80:
			y = self.lowerBound - 80
		self.targetX = x; self.targetY = y
	
	def moveToTarget(self):
		self.vec.reset(0, 0)
		if self.x < self.targetX:
			self.moveRight()
		if self.x > self.targetX:
			self.moveLeft()
		if self.y < self.targetY:
			self.moveDown()
		if self.y > self.targetY:
			self.moveUp()
	
	def turnFace(self, target):
		if self.isDead():
			return 
		if target.x < self.x:
			self.direction = BadGuy.LEFT
		elif target.x > self.x:
			self.direction = BadGuy.RIGHT
	
	def aiMove(self, target):
		self.turnFace(target)
		if self.withinRange(48, target):
			self.setTarget(self.x, self.y)
			if self.cd_action.timeUp():
				P = 50
				if randint(1, 100) <= P:
					self.attack()
				self.cd_action.start()
		elif self.checkForTarget(target):
			self.setTarget(target.x, target.gnd_y)
		else:
			self.setTarget(self.x, self.y)
		self.moveToTarget()
	
	def resurge(self):
		self.HP = 100 + 100 * (self.level - 1)
		self.deadFlag = False
	
	def move(self):
		if self.isBeaten():
			return
		if self.isFucked():
			if self.anim_fucked._frame >= 4:
				return
			if self.status == BadGuy.FFUCKED:
				if self.direction == BadGuy.LEFT:
					self.x += 3
				else:
					self.x -= 3
			else:
				if self.direction == BadGuy.LEFT:
					self.x -= 3
				else:
					self.x += 3
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

	def turn(self):
		if self.v_x > 0:
			self.direction = BadGuy.RIGHT
		elif self.v_x < 0:
			self.direction = BadGuy.LEFT

	def update(self):
		#print self.status
		if self.status == BadGuy.WALK:
			self.image = self.anim_walk.image
			self.anim_walk.update( pygame.time.get_ticks() )

		if self.status == BadGuy.STAND:
			self.image = self.anim_stand.image
			self.anim_stand.update( pygame.time.get_ticks() )

		if self.status == BadGuy.ATK:
			self.image = self.anim_atk.image
			self.anim_atk.update( pygame.time.get_ticks() )
		
		if self.status == BadGuy.BEATEN:
			self.image = self.anim_beat.image
			self.anim_beat.update(pygame.time.get_ticks())
		
		if self.status == BadGuy.FFUCKED or self.status == BadGuy.BFUCKED:
			self.image = self.anim_fucked.image
			self.anim_fucked.update(pygame.time.get_ticks())
		
		if self.isRight():
			self.image = pygame.transform.flip(self.image, 1, 0)

		if not self.isActing() and not self.isDead():
			self.stand()
		if self.isMoving() and not self.isActing() and not self.isDead():
			self.walk()
		if self.isAttack() and self.anim_atk.done() and not self.isDead():
			self.stand()
			self.cd_atk.start()
		
		
		self.turn()
		self.getVelocity()
		self.move()
		if self.isDead():
			return 
		self.rect.topleft = self.x, self.y
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)


