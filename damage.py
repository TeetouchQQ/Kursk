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

class DamageNum(Entity):
	def __init__(self, position, size, speed,number):
		super().__init__(position, collision_radius=5)
		self.speed = speed
		self.size = size
		self.width, self.height = size, size
		self.remove_timer = 15
		self.showing = True
		self.font_size = 20
		
		self.number = number
  
		self.position.x += random.uniform(-10, 10)
		self.position.y += random.uniform(-10, 10)
	def update(self):
		if self.showing:
			self.position.y -= 2 * self.speed
			if self.remove_timer < 6:
				self.font_size -= 1
   
			self.remove_timer -=1
   
		if self.remove_timer == 0:
			self.remove = True

	def draw(self, screen):
		self.font = pygame.font.Font('8-BIT WONDER.TTF',self.font_size)
		text_surface = self.font.render(str(self.number), False, (0, 0, 0))
		screen.blit(text_surface, (self.position.x,self.position.y))

	def view_world(self, world):
		pass
