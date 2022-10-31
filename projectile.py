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


class Projectile(Entity):
	def __init__(self, position, direction, owner, damage, size, speed):
		super().__init__(position, collision_radius=5)
		self.direction = Vector2(direction)
		self.owner = owner
		self.speed = speed
		self.damage = damage
		self.size = size
		self.width, self.height = size, size
		self.projectile = True
		self.penetrate = False
		self.flame = False
		self.explosive = False
		self.blast_damage = 0
		#self.image = pygame.image.load(config.bullet_im).convert_alpha()
	def update(self):
		pass

	def draw(self, screen):
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (0, 255, 0))
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (0, 255, 0))

	def view_world(self, world):
		pass

class Bullet(Projectile):
	def __init__(self, position, direction, owner, damage=5, size=5, speed=10):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
  
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
		screen.blit(rot_image,rot_rect)
  
class Pellet(Projectile):
	def __init__(self, position, direction, owner, damage=2.5, size=1, speed=12):
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
		

class MicroMissile(Projectile):

	def __init__(self, position, target, controller, direction, owner, damage=0, size=3, speed=35, explosive=True):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.penetrate = False
		self.direction = direction
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.explosive = explosive
		self.target = Vector2(target)
		self.blast_damage = 7
		self.exploding = False
		self.colour = (255, 0, 0)
		self.remove_timer = 6

		self.controller = controller

		self.mod = 1
		if random.uniform(1, -1) < 0:
			self.mod = -1

	def update(self):

		if self.exploding:
			self.remove_timer -= 1

			self.blast_damage = 0
			self.size += 3

		self.controller.control(self)

		if not (0 < self.position.x < width) and not self.exploding:
			self.explode()
		if not (0 < self.position.y < height) and not self.exploding:
			self.explode()
		if self.position.distance_to(self.controller.target_position) < 25 and not self.exploding:
			self.explode()
		if self.remove_timer <= 0:
			self.remove = True

	def draw(self, screen):
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)

	def explode(self):
		self.size = 10
		self.collision_radius = 30
		self.controller.speed = 0
		self.colour = (255, 120, 0)
		self.exploding = True

class GuidedMissile(Projectile):

	def __init__(self, position, controller, direction, owner, damage=0, size=7, speed=15, explosive=True):
		super().__init__(position, direction, owner, damage, size=size, speed=speed)
		self.collision_radius = size
		self.penetrate = False
		self.direction = direction
		self.explosive = explosive
		self.blast_damage = 50
		self.exploding = False
		self.colour = (255, 0, 0)
		self.remove_timer = 6
		self.rect = pygame.Rect(int(self.position.x),int(self.position.y),self.size,self.size)
		self.controller = controller

	def update(self):

		if self.exploding:
			self.remove_timer = max(0, self.remove_timer - 1)
			self.blast_damage = 0
			self.size += 5

		self.controller.control(self)
		
		if not (0 < self.position.x < width) and not self.exploding:
			self.explode()
		if not (0 < self.position.y < height) and not self.exploding:
			self.explode()
		if self.position.distance_to(self.controller.target_position) < 25 and not self.exploding:
			self.explode()

		if self.remove_timer == 0:
			self.remove = True

	def draw(self, screen):
		gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)
		gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, self.colour)

	def explode(self):
		self.size = 40
		self.collision_radius = 70
		self.controller.speed = 0
		self.colour = (255, 120, 0)
		self.exploding = True

	def view_world(self, world):
		self.controller.view_world(self, world)