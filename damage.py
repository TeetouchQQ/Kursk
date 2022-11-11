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
	def __init__(self, position, font_size, speed,number,color):
		super().__init__(position, collision_radius=5)
		self.speed = speed

		self.remove_timer = 15
		self.showing = True
		self.font_size = font_size
		
		self.number = number
  
		self.color = color
		self.position.x += random.uniform(-30, 30)
		self.position.y += random.uniform(-30, 30)
  
		self.font = pygame.font.Font('8-BIT WONDER.TTF',self.font_size)
	def update(self):
		if self.showing:
			self.position.y -= 2 * self.speed
			if self.remove_timer < 6:
				self.font_size -= 1
   
			self.remove_timer -=1
   
		if self.remove_timer == 0:
			self.remove = True

	def draw(self, screen):
		
		text_surface = self.font.render(str(self.number), False, self.color)
		screen.blit(text_surface, (self.position.x,self.position.y))

	def view_world(self, world):
		pass
