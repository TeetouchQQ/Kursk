import random
import pygame
import math

from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import gfxdraw
from pygame import font

from config import width, height
from entity import Entity
from hitscanner import SniperShot, Beam
from projectile import *

from config import Player
#from Plane import plane
class Weapon:

	def control(self, entity, target, point, buttons):
		pass

	def draw(self, screen, x, y, active):
		width = 140
		draw.rect(screen, (80, 0, 0), (x, y, width, 20))
		if active:
			draw.rect(screen, (255, 0, 0), (x, y, width, 20))
		my_font = pygame.font.Font(None, 20)
		name = my_font.render(self.name, 1, (50, 255, 50))
		pygame.Surface.blit(screen, name, (x + 7, y + 5))


   
class BasicGun(Weapon):

	def __init__(self, cooldown=50):
		self.max_cooldown = cooldown
		self.cooldown = 20
		self.name = 'Basic Gun'
		self.sound = pygame.mixer.Sound(sound.baiscgun)
		self.sound.set_volume(sound.baiscgun_vol)
  
	def control(self, entity, target, point, buttons):
		self.cooldown -= 1
		direction = (target - entity.position).normalize()
		button1, button2, button3 = buttons
		
		if button1 and self.cooldown <= 0:
			self.sound.play()
			bullet = Bullet(entity.position + Vector2(entity.width / 2, entity.height / 2) +direction*35, (target - entity.position).normalize(), entity, damage=10, size=5)
			entity.spawn.append(bullet)
			self.cooldown = self.max_cooldown

class ShieldCreater(Weapon):
	def __init__(self,cooldown=20):
		self.cooldown = cooldown
		self.max_cooldown = cooldown   
		
  
	def control(self,entity,entitites):
		self.cooldown -=1
		self.shield_cnt = 0
		#print(entitites)
		for ent in entitites:
			if (isinstance(ent,Shield)) == True:
				self.shield_cnt +=1
		#print(self.shield_cnt)
		if self.cooldown <= 0 and self.shield_cnt < entity.max_Shield:
			shield = Shield((0,0), (0,0), entity, damage=10, size=5,speed = ((entity.max_Shield/10)*0.1))
			self.cooldown = self.max_cooldown
			entity.spawn.append(shield)
   
class PlaneBomber(Weapon):
	def __init__(self, cooldown=500):
		self.cooldown = cooldown
		self.max_cooldown = cooldown
		self.name = 'Plane Bomber'
		self.axis = 1
	def control(self, entity):
		self.cooldown -= (1 + (entity.planeLevel*0.1))
		if self.cooldown <= 0:
			if self.axis == 1:
				plane = Plane((entity.position.x,entity.position.y), (1,1), entity, damage=10, size=5)
			self.cooldown = self.max_cooldown
			entity.spawn.append(plane)
   
class BurstGun(Weapon):

	def __init__(self, cooldown=100, burst_cooldown=2, burst_deviation=1):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.bullets_left = 0
		self.max_burst_cooldown = burst_cooldown
		self.burst_cooldown = 0
		self.spread = burst_deviation

		self.secondary_bullets_left = 0
		self.name = 'Burst Gun'
  
		self.sound = pygame.mixer.Sound(sound.baiscgun)
		self.sound.set_volume(sound.burstgun_vol)
	def control(self, entity, target, point, buttons):
		self.cooldown -= 1
		self.burst_cooldown -= 1

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			self.sound.play()
			self.secondary_bullets_left = Player.max_secondary_bullets
			self.cooldown = self.max_cooldown

		if self.secondary_bullets_left > 0 and self.burst_cooldown <= 0:
			#self.sound.play()
			direction = (target - entity.position).normalize()
			bullet = Bullet(entity.position + Vector2(entity.width / 2, entity.height / 2) + direction*35 , direction.rotate(random.uniform(-self.spread, self.spread)), entity,
				damage=2.5, size=2, speed=13)
			entity.spawn.append(bullet)
			self.secondary_bullets_left -= 1
			self.burst_cooldown = self.max_burst_cooldown


class Shotgun(Weapon):

	def __init__(self, cooldown=80, spread=5, pellets=5):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.spread = spread
		self.pellets = pellets

		self.name = 'Shotgun'
		self.sound = pygame.mixer.Sound(sound.shotgunShoot)
		self.sound.set_volume(sound.shotgunShoot_vol)
		
		self.reload = pygame.mixer.Sound(sound.shotgunReload)
		self.reload.set_volume(sound.shotgunReload_vol)
  
		self.reload_play = False
		self.reload_cnt = 30
	def control(self, entity, target, point, buttons):
		self.cooldown -= 1

		button1, button2, button3 = buttons
		if self.reload_play:
			self.reload_cnt -=1
			if self.reload_cnt <= 0:
				self.reload.play()
				self.reload_play = False	
				self.reload_cnt = 30
		if button1 and self.cooldown <= 0:
			self.sound.play()
			self.reload_play = True
			for i in range(self.pellets):
				direction = (target - entity.position).normalize()
				pellet = Pellet(entity.position + Vector2(entity.width / 2, entity.height / 2) + direction*32, direction.rotate(random.uniform(-self.spread, self.spread)), entity,
					damage=2, speed=random.uniform(11, 13))
				entity.spawn.append(pellet)
			self.cooldown = self.max_cooldown
   
		


class MachineGun(Weapon):

	def __init__(self, cooldown=4, max_deviation=10):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.spread = 0
		self.max_deviation = max_deviation

		self.name1 = 'Machine Gun (%d%%)' % int((self.spread / self.max_deviation) * 100)
		self.name = "Machine Gun"
  
		self.sound = pygame.mixer.Sound(sound.machinegun)
		self.sound.set_volume(sound.machinegun_vol)
	def control(self, entity, target, point, buttons):
		self.name1 = 'Machine Gun (%d%%)' % int((self.spread / self.max_deviation) * 100)
		self.cooldown -= 1
		self.spread = max(self.spread - 0.2, 0)

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			self.sound.play()
			direction = (target - entity.position).normalize()
			bullet = Bullet(entity.position + Vector2(entity.width/2, entity.height/2) + direction*35, direction.rotate(random.uniform(-self.spread, self.spread)), entity,
				damage=1.5, size=1, speed=12)
			entity.spawn.append(bullet)
			self.spread = min(self.spread + 1.2, self.max_deviation)
			self.cooldown = self.max_cooldown
		#self.sound.stop()

class SniperRifle(Weapon):

	def __init__(self, cooldown=20):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name1 = 'Sniper Rifle (%d)' % self.cooldown
		self.name = "Mega Beam"
		self.sound = pygame.mixer.Sound(sound.megaBEAM)
		self.sound.set_volume(sound.megaBEAM_vol)
	def control(self, entity, target, point, buttons):
		self.name1 = 'Sniper Rifle (%d)' % self.cooldown
		self.cooldown = max(self.cooldown - 1, 0)

		button1, button2, button3 = buttons

		if button1 and self.cooldown <= 0:
			self.sound.play()
			shot = SniperShot(entity.position + Vector2(entity.width/2, entity.height/2), (target - entity.position).normalize(), entity,
			    damage=40)
			entity.spawn.append(shot)
			self.cooldown = self.max_cooldown


class BeamGun(Weapon):

	def __init__(self, cooldown=1):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Beam Gun'

		self.sound1 = pygame.mixer.Sound(sound.laser1)
		self.sound1.set_volume(sound.laser_Vol)
  
		self.sound2 = pygame.mixer.Sound(sound.laser1)
		self.sound2.set_volume(sound.laser_Vol)
  
		self.laserBase = pygame.mixer.Sound(sound.laserBase)
		self.laserBase.set_volume(sound.laser_Vol)
  
		self.laser1 = True
		self.laser2 = False
  
		self.base_cooldown = 25
		self.base2_cooldown = 15
  
		self.sound_cooldown = 40
	def control(self, entity, target, point, buttons):
		self.cooldown = max(self.cooldown - 1, 0)

		button1, button2, button3 = buttons
		direction = (target - entity.position).normalize()
		if button1 and self.cooldown <= 0:
			self.sound_cooldown -= 1
			self.base_cooldown -= 1
			self.base2_cooldown -= 1
			beam = Beam(entity.position + Vector2(entity.width / 2, entity.height / 2) + direction*35, (target - entity.position).normalize(), entity,
					damage=1, colour=(20, 255, 100), width=5, range=200)
			entity.spawn.append(beam)
			self.cooldown += 2
			self.cooldown = self.max_cooldown
   
		# Sound stuff
		if self.sound_cooldown <= 0:
			if self.laser1 == True:
				self.sound1.play()
				self.laser1 = not self.laser1
				self.laser2 = not self.laser2
			elif self.laser2 == True:
				self.sound2.play()
				self.laser1 = not self.laser1
				self.laser2 = not self.laser2
			self.sound_cooldown = 40
		if self.base_cooldown <= 0:
			self.laserBase.play()
			self.base_cooldown = 15
		if self.base2_cooldown <=0:
			self.laserBase.play()
			self.base2_cooldown = 15
class Flamethrower(Weapon):

	def __init__(self, cooldown=3, max_deviation=4):
		self.max_cooldown = cooldown
		self.cooldown = 0

		self.sound = pygame.mixer.Sound(sound.flameFire)
		self.sound.set_volume(sound.flameFire_vol)
  
		self.sound1_cooldown = 5
		self.sound2_cooldown = 10
  
		self.spread = max_deviation
		self.name = 'Flamethrower'

	def control(self, entity, target, point, buttons):

		self.cooldown -= 1
		
  
		button1, button2, button3 = buttons
		direction = (target - entity.position).normalize()
		if button1 and self.cooldown <= 0:
			self.sound2_cooldown -=1
			self.sound1_cooldown -=1
			#target.rotate_ip(random.uniform(-self.spread, self.spread))
			fire = Flame(entity.position + Vector2(entity.width/2, entity.height/2) + direction*30, (target - entity.position).normalize(), entity,
				damage=0.6, size=3, speed=10)
			entity.spawn.append(fire)
			self.cooldown = self.max_cooldown
   
		#sound stuff
		if self.sound1_cooldown <= 0:
			self.sound.play()
			self.sound1_cooldown = 3
		if self.sound2_cooldown <=0:
			self.sound.play()
			self.sound2_cooldown = 3
class RocketLauncher(Weapon):

	def __init__(self, cooldown=80):
		self.max_cooldown = cooldown
		self.cooldown = 0
		self.name = 'Rocket Launcher'

		self.sound = pygame.mixer.Sound(sound.rocketLaunch)
		self.sound.set_volume(sound.rocketLaunch_vol)
  
	def control(self, entity, target, point, buttons):

		self.cooldown -= 1

		button1, button2, button3 = buttons
		direction = (target - entity.position).normalize()
		if button1 and self.cooldown <= 0:
			self.sound.play()
			rocket = Rocket(entity.position + Vector2(entity.width/2, entity.height/2) + direction*35, (target - entity.position).normalize(), entity)
			#print('NEW 2: ',(target - entity.position).normalize())
			entity.spawn.append(rocket)
			self.cooldown = self.max_cooldown

