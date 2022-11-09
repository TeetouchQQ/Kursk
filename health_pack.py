from pygame.math import Vector2
from pygame import gfxdraw

from config import width, height
from config import Player
from entity import Entity
from projectile import Projectile
from tank import Tank
import pygame
import math
import config
    
class HealthPack(Entity):

	def __init__(self, position, health_power=5, collision_radius=9,exp_get = 10):
		super().__init__(position, collision_radius=collision_radius)
		self.collision_radius = collision_radius
		self.size = collision_radius
		self.width = self.size
		self.height = self.size
		self.health_power = health_power
		self.exp_get = exp_get
  
		self.image_list = ['frame-1.png','frame-2.png','frame-3.png','frame-4.png','frame-5.png','frame-6.png','frame-7.png','frame-8.png']
  
		self.image_load = [pygame.image.load(config.health_folder + self.image_list[0]).convert_alpha(),
                     		pygame.image.load(config.health_folder+ self.image_list[1]).convert_alpha(),
                       		pygame.image.load(config.health_folder+ self.image_list[2]).convert_alpha(),
                         	pygame.image.load(config.health_folder+ self.image_list[3]).convert_alpha(),
                          	pygame.image.load(config.health_folder+ self.image_list[4]).convert_alpha(),
                           	pygame.image.load(config.health_folder+ self.image_list[5]).convert_alpha(),
                            pygame.image.load(config.health_folder+ self.image_list[6]).convert_alpha(),
                            pygame.image.load(config.health_folder+ self.image_list[7]).convert_alpha()]
		self.shadow = pygame.image.load(config.health_folder + str("shadow.png"))
		self.shadow = pygame.transform.scale(self.shadow,(self.size+8,self.size+5))
		for i in range(len(self.image_load)):
			self.image_load[i] = pygame.transform.scale(self.image_load[i] , (self.size+4,self.size+4))
        
		self.time = 0
		self.angle = 0
	def draw(self, screen):
		#gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))
		#gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))
		pic_num = round(self.time) % 8
		screen.blit(self.shadow,(self.position.x-1,self.position.y+5))
		screen.blit(self.image_load[pic_num],(self.position.x,self.position.y))
		
	def update(self):
		self.time +=0.25
		self.position.x = int(math.cos(self.angle) * 1.0001) + (self.position.x)
		self.position.y = int(math.sin(self.angle) * 1.0001) + (self.position.y)
  
		self.angle += 0.05
	def should_collide(self, other):
		return isinstance(other, Tank) and other.is_player

	def handle_collision(self, other):
		if isinstance(other, Tank) and other.is_player:
			other.health = min(other.health + self.health_power, Player.health)
			other.exp += self.exp_get
			self.remove = True