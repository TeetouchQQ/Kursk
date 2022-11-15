from pygame.math import Vector2
from pygame import gfxdraw

from config import width, height
from config import Player
from entity import Entity
from projectile import Projectile
from tank import Tank
import sound
import pygame
import math
import config
from damage import DamageNum
class HealthPack(Entity):

	def __init__(self,position,controllers, health_power=8, collision_radius=15,exp_get = 10,color = (255,255,255)):
		super().__init__(position, collision_radius=collision_radius)
		self.collision_radius = collision_radius
		self.size = 9
		self.width = self.size
		self.height = self.size
		self.health_power = health_power
		self.exp_get = exp_get
		self.controllers = controllers
		self.direction = Vector2(0,0)
		self.speed = 5
		self.color = color
		self.sound = pygame.mixer.Sound(sound.pickUP)
		self.sound.set_volume(sound.pickupVol)
  
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
  
		self.entities = []
	def draw(self, screen):
		#gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))
		#gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.size, (200, 0, 100))
		pic_num = round(self.time) % 8
		screen.blit(self.shadow,(self.position.x-1,self.position.y+5))
		cp = self.image_load[pic_num].copy()
		cp.fill(self.color, special_flags=pygame.BLEND_RGBA_MULT) 

		screen.blit(cp,(self.position.x,self.position.y))
	def view_world(self, world):
		for controller in self.controllers:
			controller.view_world(self, world)
		self.entities = world.entities
	def update(self):
		to_remove = []
		for pack in self.entities:
			if (isinstance(pack,HealthPack)) == True:
				if pack.position == self.position:
					to_remove.append(pack)
		if len(to_remove) > 0:
			for x in to_remove[1:]:
				x.remove = True
		self.time +=0.25
		# self.position.x = int(math.cos(self.angle) * 1.0001) + (self.position.x)
		# self.position.y = int(math.sin(self.angle) * 1.0001) + (self.position.y)
		self.position -= self.direction * self.speed
		# for controller in self.controllers:
		# 	controller.control(self)
		#self.angle += 0.05
	def should_collide(self, other):
		return isinstance(other, Tank) and other.is_player

	def handle_collision(self, other):
		if isinstance(other, Tank) and other.is_player:
			other.health = min(other.health + (other.max_health * (self.health_power/100)), other.max_health)
			healnum = DamageNum(self.position,font_size = 14,speed = 1,number = int(other.max_health * (self.health_power/100)),color=(0,255,0))
			self.spawn.append(healnum)
			self.sound.play()
			other.exp += self.exp_get
			self.remove = True