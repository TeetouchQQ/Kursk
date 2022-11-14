import random

from pygame.locals import *
from pygame import draw
import math
from pygame.math import Vector2
from pygame import gfxdraw
import pygame
from entity import Entity
import config
from config import width, height
import spritesheet

class Projectile(Entity):
	def __init__(self, position, direction, owner, damage, size, speed):
		super().__init__(position, collision_radius=5)
		self.direction = Vector2(direction)
		self.image = []
		self.owner = owner
		self.speed = speed
		self.damage = damage
		self.size = size
		self.width, self.height = size, size
		self.projectile = True
		self.penetrate = False
		self.flame = False
		self.minibomb = False
		self.explosive = False
		self.plane = False
		self.blast_damage = 0
		self.angle = 0
		self.ss
	def update(self):
		pass

	def draw(self, screen):
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (255, 50, 0))
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (255, 60, 0))

	def view_world(self, world):
		pass

class Bullet(Projectile):
	def __init__(self, position, direction, owner, damage=5, size=5, speed=10):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.owner = owner

		self.image = pygame.image.load(config.bullet_im).convert_alpha()
		self.image = pygame.transform.scale(self.image, (8*(self.size*0.25),52*(self.size*0.4)))
	def update(self):
		self.position += self.direction * self.speed

		if not (0 < self.position.x < width):
			self.remove = True
		if not (0 < self.position.y < height):
			self.remove = True
   
	def draw(self,screen):
		
  
		angle = (math.atan2(self.direction.x,self.direction.y))
		angle %= 2*math.pi
		angle = math.degrees(angle)

		rot_image = pygame.transform.rotate(self.image, round(angle-180))
		rotate_rect = self.image.get_rect(center = ((self.position.x), (self.position.y)))
		rot_rect = rot_image.get_rect(center=rotate_rect.center)
		#print(self.owner.Tanktype)
		if self.owner.Tanktype == "BOSS":
			cp = rot_image.copy()
			cp.fill((50, 255, 0, 100), special_flags=pygame.BLEND_RGB_SUB)
			screen.blit(cp,rot_rect)
		else:
			screen.blit(rot_image,rot_rect)
  
class Pellet(Projectile):
	def __init__(self, position, direction, owner, damage=2.5, size=1, speed=12 , font_size = 20):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
	def update(self):
		self.position += self.direction * self.speed
		self.damage = max(self.damage - 0.05, 0)
		self.speed -= 0.1

		if not (0 < self.position.x < width):
			self.remove = True
		if not (0 < self.position.y < height):
			self.remove = True
		if self.speed <= 1:
			self.remove = True
		if self.damage <= 0:
			self.remove = True

class Flame(Projectile):
	def __init__(self, position, direction, owner, damage=4, size=1, speed=12, is_flame=True):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.r = 255
		self.g = 231
		self.b = 160
		self.penetrate = True
		self.flame = is_flame
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
	def update(self):
		self.position += self.direction * self.speed
		self.speed -= 0.3
		self.size += 1
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		if not (0 < self.position.x < width):
			self.remove = True
		if not (0 < self.position.y < height):
			self.remove = True
		if self.speed <= 1:
			self.remove = True
		if self.size >= 80:
			self.remove = True
		if self.size >= 30 and not self.flame:
			self.remove = True

	def draw(self, screen):
		self.g = max(self.g - 10, 40)
		self.b = max(self.b - 10, 0)
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (self.r, self.g, self.b))
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (self.r, self.g, self.b))
	
class Rocket(Projectile):

	def __init__(self, position, direction, owner, damage=0, size=7, speed=15, explosive=True):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.penetrate = False
		self.direction = direction
		
		self.explosive = explosive
		self.blast_damage = 25
		self.exploding = False
		self.colour = (255, 0, 0)
		self.remove_timer = 6
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.rocket = pygame.image.load(config.rocket_bullet).convert_alpha()
		self.rocket = pygame.transform.scale(self.rocket, (8*(self.size*0.25),52*(self.size*0.4)))
	def update(self):

		if self.exploding:
			self.remove_timer = max(0, self.remove_timer - 1)
			self.blast_damage = 0
			self.size += 5
   
		self.position += self.direction * self.speed

		if not (0 < self.position.x < width) and not self.exploding:
			self.explode()
		if not (0 < self.position.y < height) and not self.exploding:
			self.explode()
		if self.remove_timer == 0:
			self.remove = True

	def draw(self, screen):
		# gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)
		# gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)
		angle = (math.atan2(self.direction.x,self.direction.y))
		angle %= 2*math.pi
		angle = math.degrees(angle)

		rot_image = pygame.transform.rotate(self.rocket, round(angle-180))
		rotate_rect = self.rocket.get_rect(center = ((self.position.x), (self.position.y)))
		rot_rect = rot_image.get_rect(center=rotate_rect.center)
		screen.blit(rot_image,rot_rect)
		
	def explode(self):
		self.rocket = pygame.image.load(config.rocket_explosive).convert_alpha()
		self.rocket = pygame.transform.scale(self.rocket, (40*self.size,40*self.size))
		self.size = 40
		self.collision_radius = 50
		self.speed = 0
		self.colour = (255, 120, 0)
		self.exploding = True
  
class Shield(Projectile):
	def __init__(self, position, direction, owner, damage=0, size=13, speed=15, explosive=False):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
  
		self.collision_radius = size
		self.direction = Vector2(direction)
  
		self.damage= 100
		self.explosive = explosive
		self.blast_damage = 100
		self.exploding = False
		self.colour = (255, 0, 0)
		#self.rect.center = (self.position.x,self.position.y)
		

		#self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.angle =  0
		self.owner = owner
   
		self.ss = pygame.image.load(config.Shield_img).convert_alpha()
		
		self.image1 = self.ss.subsurface(Rect(32,1010,100,120))
		self.image2 = self.ss.subsurface(Rect(166,1010,100,120))
		# self.image3 = self.ss.subsurface(Rect(287,1010,100,120))
		# self.image4 = self.ss.subsurface(Rect(420,1010,100,120))
  
		self.image1 = pygame.transform.scale(self.image1, (35,35))
		self.image2 = pygame.transform.scale(self.image2, (35,35))
		# self.image3= pygame.transform.scale(self.image3, (35,35))
		
		# self.image4 = pygame.transform.scale(self.image4, (35,35))

		self.image = []
		self.image.append(self.image1)
		self.image.append(self.image2)
		# self.image.append(self.image3)
		# self.image.append(self.image4)
	
  

		self.frame = 0
		#self.image = image
	def update(self):
		self.frame += 0.2
		
  
		self.position.x = int(math.cos(self.angle) * 100) + (self.owner.position.x)
		self.position.y = int(math.sin(self.angle) * 100) + (self.owner.position.y)
  
		self.angle += min(max(0.05,(self.speed * 1)),0.5)
	def draw(self,screen):
		
		#print(self.image)
		
		screen.blit(self.image[round(self.frame) % 2],(self.position.x-14, self.position.y-14))
		pygame.draw.circle(screen, (255,255,255), (self.position.x, self.position.y), self.size)
	
  
class bombDrop(Projectile):
	def __init__(self, position, direction, owner, damage=0, size=100, speed=15, explosive=True,angle = 0):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.direction = Vector2(direction)
		
		self.damage= 1000
		self.explosive = explosive
		self.blast_damage = 1000
		self.exploding = True
		self.colour = (255, 0, 0)
		self.remove_timer = 25
		self.angle = angle
		self.minibomb = True
		if angle == 0:
			self.position.y -= 200
			self.position.x -= 20
			self.position.x += random.uniform(-100, 100)
		elif angle == 1:
			self.position.y += 100
			self.position.x += 20
			self.position.x += random.uniform(-100, 100)
		elif angle == 2:
			self.position.y  -= 50
			self.position.x -= 100
			self.position.y += random.uniform(-50, 50)
		elif angle == 3:
			self.position.y -= 50
			self.position.x += 100
			self.position.y += random.uniform(-50, 50)
   
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.rect.center = (self.position.x,self.position.y)
		


		self.imageOri = pygame.image.load(config.bomb_explo).convert_alpha()
		self.image = self.imageOri
		self.image = pygame.transform.scale(self.image, (size,size))
		

	def update(self):
		
		self.image = pygame.transform.scale(self.imageOri, (self.size,self.size))
		self.rect = self.image.get_rect(center = (self.position.x,self.position.y))
		
		if self.exploding:
			self.remove_timer = max(0, self.remove_timer - 1)
			self.blast_damage = 1000
			self.size += 2
			
		if self.remove_timer == 0:
			self.remove = True
   
	def draw(self, screen):
		screen.blit(self.image,self.rect)


  
class Plane(Projectile):

	def __init__(self, position, direction, owner, damage=0, size=7, speed=10,angle=0):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size

		self.width =250
		self.height = 250
		self.direction = Vector2(direction)
		self.plane = True
		self.blast_damage = 25

		self.colour = (255, 0, 0)
		self.remove_timer = 150
  
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.bomb = True
		self.plane = pygame.image.load(config.Plane_im).convert_alpha()
		self.plane = pygame.transform.scale(self.plane , (self.width,self.height))
		self.plane_back =  pygame.image.load(config.Plane_back).convert_alpha()
		self.plane_back = pygame.transform.scale(self.plane_back , (self.width,self.height))
  
		self.minibomb_cooldown = 5
		self.minibomb_Maxcooldown = self.minibomb_cooldown

		self.angle =  random.randrange(0, 4)
		if self.angle == 0:
			self.direction = Vector2(0,1)
			self.position.x = self.position.x + random.uniform(-100,100)
			self.position.y = 0
			self.plane = pygame.transform.rotate(self.plane , -90)
			self.plane_back = pygame.transform.rotate(self.plane_back , -90)
		elif self.angle == 1:
			self.direction = Vector2(0,-1)
			self.position.x = self.position.x + random.uniform(-100,100)
			self.position.y = height
			self.plane = pygame.transform.rotate(self.plane , 90)
			self.plane_back = pygame.transform.rotate(self.plane_back , 90)
		elif self.angle == 2:
			self.direction = Vector2(1,0)
			self.position.x = 0
			self.position.y = self.position.y
			self.plane = pygame.transform.rotate(self.plane , 0)
			self.plane_back = pygame.transform.rotate(self.plane_back , 0)
		elif self.angle == 3:
			self.direction = Vector2(-1,0)
			self.position.x = width
			self.position.y = self.position.y + random.uniform(-100,100)
			self.plane = pygame.transform.rotate(self.plane , 180)
			self.plane_back = pygame.transform.rotate(self.plane_back , 180)
	def update(self):
		self.remove_timer -= 1
  
		self.minibomb_cooldown -= 1
		if self.minibomb_cooldown <= 0:
			minibomb = bombDrop(self.position, (0,0), self.owner, damage=0, size=20, speed=15, explosive=True,angle = self.angle)
			minibomb1 = bombDrop(self.position, (0,0), self.owner, damage=0, size=20, speed=15, explosive=True,angle = self.angle)
			self.owner.spawn.append(minibomb)
			self.owner.spawn.append(minibomb1)
			self.minibomb_cooldown  = self.minibomb_Maxcooldown
		
		self.position += self.direction * self.speed


		if self.remove_timer == 0:
			self.remove = True

	def draw(self, screen):
		screen.blit(self.plane_back,((self.position.x-(self.width/2)-70),(self.position.y-((self.height/2*1.5)))-40))
		screen.blit(self.plane,(self.position.x-(self.width/2),self.position.y-((self.height/2*1.5))))
		
		
	# def explode(self):
	# 	self.rocket = pygame.image.load(config.rocket_explosive).convert_alpha()
	# 	self.rocket = pygame.transform.scale(self.rocket, (40*self.size,40*self.size))
	# 	self.size = 40
	# 	self.collision_radius = 50
	# 	self.speed = 0
	# 	self.colour = (255, 120, 0)
	# 	self.exploding = True

