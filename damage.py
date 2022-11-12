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
		text_with_ouline = self.add_outline_to_image(text_surface, 3, (1, 1, 1))
		screen.blit(text_with_ouline, (self.position.x,self.position.y))

	def view_world(self, world):
		pass


	def add_outline_to_image(self,image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (0, 0, 0)) -> pygame.Surface:
		mask = pygame.mask.from_surface(image)
		mask_surf = mask.to_surface(setcolor=color)
		mask_surf.set_colorkey((0, 0, 0))

		new_img = pygame.Surface((image.get_width() + 3, image.get_height() + 10))
		new_img.fill(color_key)
		new_img.set_colorkey(color_key)

		for i in -thickness, thickness:
			new_img.blit(mask_surf, (i + thickness, thickness))
			new_img.blit(mask_surf, (thickness, i + thickness))
		new_img.blit(image, (thickness, thickness))

		return new_img