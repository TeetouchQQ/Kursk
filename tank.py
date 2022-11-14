import random

from pygame.locals import *
from pygame import draw
from pygame.math import Vector2
from pygame import transform
from pygame import image
from pygame import gfxdraw
from pygame import transform
import pygame
from config import width, height
from entity import Entity
from projectile import Projectile, Flame
from damage import DamageNum
from Plane import Plane
import config

class Tank(Entity):
	def __init__(self, position, controllers, size=20, max_health=20, high_colour=(255, 0, 0), low_colour=(100, 0, 100),
				collision_radius=10, weapons=[], is_player =False, sprite_coords=((0, 0, 40, 40), (40, 0, 40, 40),(0, 255, 0)),
    			Tanktype = None, bomb = [] , shield = [] , damage_bonus = 3 ,max_Shield = 0):
		super().__init__(position, sprite_coords=sprite_coords, collision_radius=collision_radius)
		self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
  
		#About Upgrade player stats
		self.level = 1
		self.health = max_health
		self.damage_bonus = damage_bonus
		self.exp = 0
		self.exp_perLevel = self.level * 60
		self.expBonus = 1
		self.planeLevel = 0
		self.max_Shield = 1
		#================================================

		self.is_player = is_player
		self.on_fire = False
		self.fire_resist = 85
		self.fire_time = self.fire_resist

		self.size = size
  
		self.width = size
		self.height = size
		self.max_health = max_health
		self.kills = 0
		self.high_colour = high_colour
		self.low_colour = low_colour
		self.controllers = controllers
		self.weapons = weapons
		self.bomb = bomb
		self.shield = shield
		self.current_weapon = 0
		self.angle = 0
		self.aim_angle = 90
  
		self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.width)
		self.old_rect = self.rect
		self.Tanktype = Tanktype
		self.gameOver = False
		self.get_dmg = False
		if is_player:
			
			self.turret_sprite = pygame.image.load(config.player_turrent).convert_alpha()
			self.sprite   = pygame.image.load(config.player_sprite).convert_alpha()
			self.sprite = transform.scale(self.sprite, (self.width, self.height))
			self.turret_sprite = transform.scale(self.turret_sprite, (12, 62))
		else:
			self.Tanktype = Tanktype
			if self.Tanktype == 'mothership':
				self.sprite = pygame.image.load(config.mothership_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.mothership_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'lightTank':
				self.sprite = pygame.image.load(config.lighttank_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.lighttank_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'shotgunner':
				self.sprite = pygame.image.load(config.shotgun_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.shotgun_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'beamer':
				self.sprite = pygame.image.load(config.beamer_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.beamer_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'basic':
				self.sprite = pygame.image.load(config.basic_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.basic_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'healer':
				self.sprite = pygame.image.load(config.healer_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.healer_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'scanner':
				self.sprite = pygame.image.load(config.scanner_sprite).convert_alpha()
				self.turret_sprite  = pygame.image.load(config.scanner_turrent).convert_alpha()
				self.turret_sprite = transform.scale(self.turret_sprite, (10, 30))
				self.sprite = transform.scale(self.sprite, (self.width, self.height))
			elif self.Tanktype == 'BOSS':
				self.image = []
				self.frame  = 0
				self.width = self.width*1.4
				self.sprite = pygame.image.load(config.BOSS_SPRITE).convert_alpha()
				for i in range(3):
					#self.image1 = self.sprite.subsurface(Rect(i*170,0,170,140))
					#self.image1 = pygame.transform.scale(self.image1, (200, 100))
					
					self.image1 = self.sprite.subsurface(Rect(0,i*146,272,146))
					self.image1 = pygame.transform.scale(self.image1, (400, 300))
					self.image.append(self.image1)
				self.ori = self.image
			# else:
			# 	self.turret_sprite = self.get_turret_sprite()
			# 	self.image_body = self.turret_sprite 
		if self.Tanktype != "BOSS":
			self.rotated_turret_sprite = self.turret_sprite
			self.image_turrent = self.rotated_turret_sprite
	def view_world(self, world):
		for controller in self.controllers:
			controller.view_world(self, world)

	def update(self):
		if self.Tanktype == "BOSS":
			self.frame += 0.25
		for controller in self.controllers:
			controller.control(self)
		
		if self.on_fire:
			self.handle_fire()

		self.old_rect = self.rect.copy()
		self.rect = pygame.Rect(self.position.x,self.position.y,self.width,self.width)
		
	def draw(self, screen):
		if self.Tanktype != "BOSS":
			old_rect = self.sprite.get_rect(center = (self.position.x + self.width/2, self.position.y + self.height/2))
	
			rotate_rect = self.turret_sprite.get_rect(center = (self.position.x + self.width/2, self.position.y + self.height/2))		
			self.rotated_turret_sprite, old_turret_rect = self.rotate_center(self.turret_sprite, rotate_rect, self.aim_angle)
	
			self.rotated_sprite, new_rect = self.rotate_center(self.sprite, old_rect, self.angle)

			screen.blit(self.rotated_sprite, new_rect)
			screen.blit(self.rotated_turret_sprite, old_turret_rect)

			self.draw_health_bar(screen)
		else:
			#pygame.draw.rect(screen,(255,0,0),self.rect)
			if self.get_dmg == False:
				screen.blit(self.image[round(self.frame) % 3], self.rect)
			else:
				cp = self.image[round(self.frame) % 3].copy()
				cp.fill((200, 200, 200, 90), special_flags=pygame.BLEND_ADD)
				screen.blit(cp, self.rect)
				self.get_dmg = False
   
	def rotate_by_angle(self, image, angle, rotations={}):
		r = rotations.get(image, 0) + round(angle)
		rotations[image] = r
		return transform.rotate(image, r)

	def rotate_center(self, image, rect, angle):
		rot_image = transform.rotate(image, round(angle-90))
		rot_rect = rot_image.get_rect(center=rect.center)
		return rot_image,rot_rect

	def draw_health_bar(self, screen):
		health_percent = self.health / self.max_health
		low_colour = self.low_colour
		high_colour = self.high_colour
		colour = list(low_colour)
		for i in range(3):
			colour[i] += health_percent * (high_colour[i] - colour[i])
			if colour[i] < 0:
				colour[i] = 0
			if colour[i] > 255:
				colour[i] = 255
		draw.rect(screen, colour, (self.position.x + self.width / 2 - 26, self.position.y - 13, health_percent * 50, 5))

	def get_turret_sprite(self):
		pass
		#return self.ss.image_at(self.ss.turret_sheet, (0, 0, 90, 18), (0, 255, 0))

	def should_collide(self, other):
		if (other.projectile or other.hitscan) and other.owner is not self:
			if not other.owner.is_player and not self.is_player:
				return False
			return True
		return False
	
	def handle_collision(self, other):
		if other.projectile or other.hitscan:
			if other.projectile and not other.penetrate and not other.explosive and not other.plane:
				other.remove = True
			flame_mod = 1
			if other.projectile and other.flame:
				self.on_fire = True
				self.fire_time = 150
			if other.explosive and not other.exploding and not other.plane:
				other.explode()	
			if not self.is_player and not other.minibomb and not other.flame:
					damge_number = DamageNum(other.position,font_size = 16,speed = 1,number = int((other.damage + other.blast_damage) * other.owner.damage_bonus),color=(255,255,255))


					
					self.get_dmg = True
					self.spawn.append(damge_number)
     
					#self.image[round(self.frame) % 3] = self.ori
			self.health = max(self.health - ((other.damage + other.blast_damage) * other.owner.damage_bonus), 0)
			#print(other.damage)
			if self.health <= 0:
				for die_controller in self.controllers:
					die_controller.die(self, other)
				
				other.owner.kills += 1
				other.owner.exp  += 1 * other.owner.expBonus
				
				if self.is_player:
					other.owner.gameOver = True

	def handle_fire(self):
		self.fire_time = max(self.fire_time - 1, 0)

		if self.fire_time <= 0:
			self.on_fire = False
			self.fire_time = self.fire_resist
		else:
			self.health = max(self.health - 0.1, 0)
			if self.fire_time % 5 == 0:
				try:
					flame = Flame(Vector2(random.uniform(self.position.x, self.position.x + self.width), random.uniform(self.position.y, self.position.y + self.height)),self.direction.reflect(self.direction), self, damage=0, size=1, speed=3, is_flame=False)
					self.spawn.append(flame)
					if self.health <= 0:
						for die_controller in self.controllers:
							if self.is_player:
								self.gameOver = True
							die_controller.die(self, flame)
						flame.owner.kills += 1
				except:
					pass
 
				
