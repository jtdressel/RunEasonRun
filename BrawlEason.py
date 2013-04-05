"""
Copy all attributes of Eason to BrawlEason, including animations and sounds
"""
from Eason import *

class BrawlEason(Eason):
	RUN, JUMP, ATK, DEAD, DROP, STAND = range(6) #CHANGE/ADD ACTIONS  
	def __init__(self):

		Eason.__init__(self, pos)

		self.v_x = 0
		self.status = BrawlEason.STAND
		self.health = 3
		self.atkDone = True
		#add a special attack atribute later

		#-----------------------BRAWL ANIMATIONS-------------------------


	"""
	Any methods not changed are the same as Eason
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
		""" Check to see if Eason steps beyond x,y bounds """
		x, y = width, height
		if self.rect.top < y/3 or self.rect.bottom > y:
			return False
		if self.rect.left < 0 or self.rect.right > x:
			return False
		return True

	def stand(self):
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

	