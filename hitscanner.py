import pygame
from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import gfxdraw
import math
import config
from entity import Entity
from tank import Tank
import sound
from damage import DamageNum
from config import width, height
from projectile import Plane
class HitScanner(Entity):
	def __init__(self, position, direction, owner, damage, range=2000):
		super().__init__(position, collision_radius=1)
		self.direction = Vector2(direction)
		self.owner = owner
		self.damage = damage
		self.hitscan = True
		self.timer = 5
		self.range = range
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),1,1)
	def update(self):

		if self.timer == 4:
			self.damage = 0
		if self.timer <= 0:
			self.remove = True
		self.timer -= 1

	def collide(self, other):
		E = Vector2(self.position)
		L = Vector2(self.position + (self.direction * self.range))
		C = Vector2(other.position.x + (other.width / 2), other.position.y + (other.height / 2))

		d = L - E
		f = E - C

		a = d.dot(d)
		b = 2 * f.dot(d)
		c = f.dot(f) - (other.width * other.width)

		discriminant = (b * b) - (4 * a * c)

		if discriminant >= 0:

			disc = math.sqrt(discriminant)

			t1 = (-b - disc) / (2 * a)
			t2 = (-b + disc) / (2 * a)

			if 0 <= t1 <= 1:
				self.hit(other)
			elif 0 <= t2 <= 1:
				self.hit(other)

	def hit(self, other):
		other.health = max(other.health - self.damage, 0)
		if isinstance(self, Beam):
			other.on_fire = True
			other.get_dmg = True
			damge_number = DamageNum((other.position.x,other.position.y),font_size = 16,speed = 1,number = int((self.damage) * self.owner.damage_bonus),color=(255,255,255))
			other.spawn.append(damge_number)
		if isinstance(self, SniperShot) and isinstance(other, Tank)  == True and isinstance(other, Plane) == False:
			other.on_fire = True
			other.get_dmg = True
			if other.Tanktype == "BOSS":
				damge_number = DamageNum((other.position.x+150,other.position.y+150),font_size = 16,speed = 1,number = int((self.damage) * self.owner.damage_bonus),color=(255,255,255))
			else:
				damge_number = DamageNum((other.position.x,other.position.y),font_size = 16,speed = 1,number = int((self.damage) * self.owner.damage_bonus),color=(255,255,255))
			other.spawn.append(damge_number)
	
		if other.health <= 0:
			for die_controller in other.controllers:
				die_controller.die(other, self)

	def draw(self, screen):
		pass

class SniperShot(HitScanner):
	def __init__(self, position, direction, owner, damage):
		super().__init__(position, direction, owner, damage=damage)
		self.collision_radius = 100
		self.width = self.collision_radius
		
		self.owner= owner
		self.image = []
  
  
		self.ss = pygame.image.load(config.Shield_img).convert_alpha()
  
		
  
		self.image1 = self.ss.subsurface(Rect(20,1220,203,120))
		self.image2 = self.ss.subsurface(Rect(238,1220,203,120))
		self.image3 = self.ss.subsurface(Rect(453,1220,203,120))
		self.image4 = self.ss.subsurface(Rect(24,1349,203,120))
		self.image5 = self.ss.subsurface(Rect(264,1353,203,120))
		self.image6 = self.ss.subsurface(Rect(470,1353,203,120))
		self.image7 = self.ss.subsurface(Rect(40,1464,203,120))
  
		self.image1 = pygame.transform.scale(self.image1, (200, 120))
		self.image2 = pygame.transform.scale(self.image2, (200, 120))
		self.image3 = pygame.transform.scale(self.image3, (200, 120))
		self.image4 = pygame.transform.scale(self.image4, (200, 120))
		self.image5 = pygame.transform.scale(self.image5, (200, 120))
		self.image6 = pygame.transform.scale(self.image6, (200, 120))
		self.image7 = pygame.transform.scale(self.image7, (200, 120))
  
  
		self.dupIM = self.ss.subsurface(Rect(558,1353,118,118))
		self.dupIM= pygame.transform.scale(self.dupIM, (120, 120))
  
		self.image.append(self.image1)
		self.image.append(self.image2)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image4)
		self.image.append(self.image5)
		self.image.append(self.image6)
		self.image.append(self.image7)
		self.frame = 0
		self.timer = 20
	def update(self):
		self.frame += 0.15
  
		if self.timer == 2:
			self.damage = 0
		if self.timer <= 0:
			self.remove = True
		self.timer -= 1
  
	def draw(self, screen):
		P = Vector2(self.position)
		Q = Vector2(self.position + (self.direction * self.range))

		angle1 = pygame.math.Vector2(self.direction*100).angle_to((1, 0))
		to_render = pygame.transform.rotate(self.image[round(self.frame) % 10], angle1)
		new_rect = to_render.get_rect(center = to_render.get_rect(center = (self.position.x + (self.direction.x * 100), self.position.y+ (self.direction.y *100 ))).center)
		#draw.lines(screen, (0, 255, 0), False, [(P.x, P.y), (Q.x, Q.y)])
		screen.blit(to_render,new_rect)
		dup_render =pygame.transform.rotate(self.dupIM, angle1)
		if self.frame % 10 >0:
			new_rect1 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 250), self.position.y+ (self.direction.y *250 ))).center)
			new_rect2 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 350), self.position.y+ (self.direction.y *350 ))).center)
			new_rect3 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 450), self.position.y+ (self.direction.y *450 ))).center)
			new_rect4 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 550), self.position.y+ (self.direction.y *550 ))).center)
			screen.blit(dup_render,new_rect1)
			screen.blit(dup_render,new_rect2)
			screen.blit(dup_render,new_rect3)
			screen.blit(dup_render,new_rect4)
   
class Beam(HitScanner):

	def __init__(self, position, direction, owner, damage, width, colour, range):
		super().__init__(position, direction, owner, damage=damage, range=range)
		self.width = width
		self.colour = colour
		self.frame = 0
		self.timer = 1
	def update(self):
		self.frame += 0.25
  

		if self.timer <= 0:
			self.remove = True
		self.timer -= 1
  
	def draw(self, screen):
		P = Vector2(self.position)
		Q = Vector2(self.position + (self.direction * self.range))

		draw.lines(screen, self.colour, False, [(P.x, P.y), (Q.x, Q.y)], self.width)
  
class CageBeam(HitScanner):

	def __init__(self, position, direction, owner, damage, width, colour, range):
		super().__init__(position, direction, owner, damage=damage, range=range)
		self.width = width
		self.colour = colour
		self.frame = 0
		self.timer = 250
		self.angle = 0
		self.Q = Vector2(self.position + (self.direction * self.range))
  
		self.x = owner.position.x
		self.y = owner.position.y
		self.owner = owner
	def rotate2Darray(self,direction,angle):
		oldX = direction[0]
		oldY = direction[1]
		newX = oldX * math.cos(angle) - oldY * math.sin(angle)
		newY = oldX * math.sin(angle) + oldY * math.cos(angle)

		return (newX,newY)

	def update(self):
		self.frame += 0.25
  
		self.x = self.owner.position.x
		self.y = self.owner.position.y
		if self.timer <= 0:
			self.remove = True
		self.timer -= 1
		#self.angle  += 0.01
		self.angle = self.angle % 360
		self.direction = self.rotate2Darray(self.direction,0.005)
		self.direction = Vector2(self.direction)
	def draw(self, screen):
		
		Q = Vector2(self.position + (self.direction * self.range))
		P = Vector2(self.position)
		#print(P)
		draw.lines(screen, self.colour, False, [(self.x+200, self.y+150), (Q.x,Q.y)], self.width)

class BossBeam(HitScanner):
	def __init__(self, position, direction, owner, damage):
		super().__init__(position, direction, owner, damage=damage)
		self.collision_radius = 100
		self.width = self.collision_radius
		
		self.owner= owner
		self.image = []
		self.ss = pygame.image.load(config.Shield_img).convert_alpha()
		
		self.image1 = self.ss.subsurface(Rect(20,1220,203,120))
		self.image2 = self.ss.subsurface(Rect(238,1220,203,120))
		self.image3 = self.ss.subsurface(Rect(453,1220,203,120))
		self.image4 = self.ss.subsurface(Rect(24,1349,203,120))
		self.image5 = self.ss.subsurface(Rect(264,1353,203,120))
		self.image6 = self.ss.subsurface(Rect(470,1353,203,120))
		self.image7 = self.ss.subsurface(Rect(40,1464,203,120))
  
		self.image1 = pygame.transform.scale(self.image1, (200, 120))
		self.image2 = pygame.transform.scale(self.image2, (200, 120))
		self.image3 = pygame.transform.scale(self.image3, (200, 120))
		self.image4 = pygame.transform.scale(self.image4, (200, 120))
		self.image5 = pygame.transform.scale(self.image5, (200, 120))
		self.image6 = pygame.transform.scale(self.image6, (200, 120))
		self.image7 = pygame.transform.scale(self.image7, (200, 120))
  
  
		self.dupIM = self.ss.subsurface(Rect(558,1353,118,118))
		self.dupIM= pygame.transform.scale(self.dupIM, (120, 120))
  
		self.image.append(self.image1)
		self.image.append(self.image2)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image3)
		self.image.append(self.image4)
		self.image.append(self.image5)
		self.image.append(self.image6)
		self.image.append(self.image7)
		self.frame = 0
		self.timer = 20
	def update(self):
		self.frame += 0.15
  
		if self.timer == 2:
			self.damage = 0
		if self.timer <= 0:
			self.remove = True
		self.timer -= 1
  
	def draw(self, screen):
		P = Vector2(self.position)
		Q = Vector2(self.position + (self.direction * self.range))

		#draw.lines(screen, (0, 255, 0), False, [(P.x, P.y), (Q.x, Q.y)])
  
		

		angle1 = pygame.math.Vector2(self.direction*100).angle_to((1, 0))
		to_render = pygame.transform.rotate(self.image[round(self.frame) % 10], angle1)
		new_rect = to_render.get_rect(center = to_render.get_rect(center = (self.position.x + (self.direction.x * 100), self.position.y+ (self.direction.y *100 ))).center)

		cp = to_render.copy()
		cp.fill((50, 255, 0, 100), special_flags=pygame.BLEND_RGB_SUB)
		screen.blit(cp,new_rect)
		dup_render =pygame.transform.rotate(self.dupIM, angle1)
		if self.frame % 10 >0:
      
			
			new_rect1 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 250), self.position.y+ (self.direction.y *250 ))).center)
			new_rect2 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 350), self.position.y+ (self.direction.y *350 ))).center)
			new_rect3 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 450), self.position.y+ (self.direction.y *450 ))).center)
			new_rect4 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 550), self.position.y+ (self.direction.y *550 ))).center)
			new_rect5 = dup_render.get_rect(center = dup_render.get_rect(center = (self.position.x + (self.direction.x * 650), self.position.y+ (self.direction.y *550 ))).center)
			dp = dup_render.copy()
			dp.fill((50, 255, 0, 100), special_flags=pygame.BLEND_RGB_SUB)
			screen.blit(dp,new_rect1)
			screen.blit(dp,new_rect2)
			screen.blit(dp,new_rect3)
			screen.blit(dp,new_rect4)
			screen.blit(dp,new_rect5)
			# screen.blit(dup_render,new_rect1)
			# screen.blit(dup_render,new_rect2)
			# screen.blit(dup_render,new_rect3)
			# screen.blit(dup_render,new_rect4)