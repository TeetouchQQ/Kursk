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
#from tank import Tank

from projectile import * 
class Plane(Entity):
	def __init__(self, position, direction, damage = 100, size =20, speed = 5):
		super().__init__(position, collision_radius=5)
		self.direction = Vector2(direction)


		self.speed = speed
		self.damage = damage
		self.size = size
		self.width, self.height = size, size

		self.explosive = False
		self.blast_damage = 0
  
		self.image = pygame.image.load(config.Plane_im).convert_alpha()
		self.image = pygame.transform.scale(self.image, (300,300))
		self.image = pygame.transform.rotate(self.image , -90)
  
	def update(self):
		self.position +=  self.direction * self.speed
  
		if not (0 < self.position.x < width):
			self.remove = True
		if not (0 < self.position.y < height):
			self.remove = True

		bomb = Bomb(self.position, 100 ,size=100, speed=0, explosive=True)
		#self.word.spawn.append(bomb)
	def draw(self, screen):
		screen.blit(self.image,(self.position.x,self.position.y))

	def view_world(self, world):
		self.entities = world.entities
		print(self.entities)
