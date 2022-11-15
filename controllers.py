import pygame, sys

from pygame.math import Vector2
import math
from pygame import mouse
from pygame.locals import *
from pygame import transform
from math import atan2, degrees, pi
import random
from scipy.interpolate import interp1d
from hitscanner import Beam,CageBeam,BossBeam
from tank import Tank
from projectile import Bullet, Pellet,Shield
from config import width, height
from config import Player
import factories
import sound
from weapons import SniperRifle

from world import World

class Controller:

	def view_world(self, entity, world):
		pass

	def control(self, entity):
		pass

	def die(self, entity, killer):
		pass


class EnemyDieController(Controller):

	def __init__(self):
		pass

	def die(self, entity, killer):
		if not entity.is_player and killer.owner.is_player:
			chance = random.randint(1,100)
			if chance <= 10:
				health_pack = factories.create_health_pack(entity.position,health_power=(8)*2,exp_get = (10)*2,color = (255,255,0))
			elif chance > 10 and chance <= 40:
				health_pack = factories.create_health_pack(entity.position,health_power=(8)*1.5,exp_get = (10)*1.5,color = (50,50,200))
			elif chance > 40:
				health_pack = factories.create_health_pack(entity.position,health_power=8,exp_get = 10,color = (255,255,255))
			entity.spawn.append(health_pack)
			entity.remove = True
		entity.remove = True


class BossSkillController(Controller):
	def __init__(self, bulletCooldown=50,laserCooldown = 100 , beamCooldown = 5,cageCooldown = 1000):
		self.max_bulletCooldown = bulletCooldown
		self.bulletCooldown= 0
		self.name = 'BOSS SKILL'
  
		self.max_laserCooldown = laserCooldown
		self.laserCooldown= 200
  
		self.max_beamCooldown = beamCooldown
		self.beamCooldown = 500
		self.spawn_Shield = True


		self.max_cageCooldown = cageCooldown
		self.cageCooldown = 500
  
		self.point = [(0,-1),(-1,0),(0,1),(1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

		self.laser_angle = 0
		self.test_vec = (-1,0)
	def control(self, entity):
		# if self.spawn_Shield:
		# 	for i in range(5):
		# 		shield = Shield((0,0), (0,0), entity, damage=10, size=5,speed = ((entity.max_Shield/10)*0.1))
		# 		entity.spawn.append(shield)
		
		self.bulletCooldown -= 1
  
		if self.bulletCooldown <= 0:
			for i in range(8):
				#direction = (target - entity.position).normalize()
				bullet = Bullet(entity.position + Vector2(entity.width / 2, entity.height / 2) +Vector2(self.point[i])*35, Vector2(self.point[i]).normalize(), entity, damage=10, size=5)
				entity.spawn.append(bullet)
			self.bulletCooldown = self.max_bulletCooldown
		#==================================================================
		self.laserCooldown -= 1
		if self.laserCooldown <= 0:
			#self.laser_angle += 0.01
		
			oldX = self.test_vec[0]
			oldY = self.test_vec[1]
			self.laser_angle = random.randrange(0, 360)
			newX = oldX * math.cos(self.laser_angle) - oldY * math.sin(self.laser_angle)
			newY = oldX * math.sin(self.laser_angle) + oldY * math.cos(self.laser_angle)
			self.test_vec = (newX,newY)
   
			beam = BossBeam(entity.position + Vector2(entity.width / 2, entity.height / 2) + Vector2(self.test_vec)*35,Vector2(self.test_vec).normalize(), entity,
					damage=1)
			entity.spawn.append(beam)
			self.laser_angle = random.randrange(0, 360)
			newX = oldX * math.cos(self.laser_angle) - oldY * math.sin(self.laser_angle)
			newY = oldX * math.sin(self.laser_angle) + oldY * math.cos(self.laser_angle)
			self.test_vec = (newX,newY)
			beam2 = BossBeam(entity.position + Vector2(entity.width / 2, entity.height / 2) + Vector2(self.test_vec)*35,Vector2(self.test_vec).normalize(), entity,
					damage=1)
			entity.spawn.append(beam2)
			self.laserCooldown = self.max_laserCooldown
   
		
		#========================================================================
  
		self.beamCooldown -= 1
		if self.beamCooldown <= 0:
			main_vec = (-1,-1)
			oldX  = -1
			oldY = -1
			rand_angle = random.randrange(0, 360)
			newX = oldX * math.cos(rand_angle) - oldY * math.sin(rand_angle)
			newY = oldX * math.sin(rand_angle) + oldY * math.cos(rand_angle)
			shoow_vec = (newX,newY)
			bulletMini = Bullet(entity.position + Vector2(entity.width/2, entity.height/2) + Vector2(shoow_vec)*35,Vector2(shoow_vec).normalize(), entity,
				damage=1.5, size=1, speed=12)
			entity.spawn.append(bulletMini)
			#self.beamCooldown = self.max_beamCooldown
		#================================================================
		self.cageCooldown -= 1
		cageVec = self.point
		if self.cageCooldown <= 0:
			for vec in cageVec:
				cagebeam1 = CageBeam(entity.position + Vector2(entity.width / 2, entity.height / 2) + Vector2(vec)*15,Vector2(vec).normalize(), entity,
						damage=1, colour=(255, 40, 40), width=5, range=700)
				entity.spawn.append(cagebeam1)


			self.cageCooldown = self.max_cageCooldown
		#==========================

			
class BounceMoveController(Controller):

	def __init__(self, speed=3):
		self.speed = speed
		self.speed_original = speed
		
	def view_world(self, entity, world):
		self.rect = entity.rect
		self.old_rect = entity.old_rect
		self.speed = self.speed_original * world.difficulty.speed_mod
		self.player_position = world.player.position
		
		self.word_entities = world.entities
	def control(self, entity):
		collision_tor = 5
		#print(entity.get_sprite())
		for enemy in self.word_entities:
				if (isinstance(enemy,Tank)) == True and enemy != entity and not enemy.is_player:
					collision_tor = 1
					if  pygame.Rect.colliderect(enemy.rect, entity.rect) == True:
						if enemy.rect.right >= entity.rect.left and enemy.old_rect.right <= entity.old_rect.left:
							enemy.rect.right = entity.rect.left
							enemy.position.x = enemy.rect.x
						if enemy.rect.left <= entity.rect.right and enemy.old_rect.left >= entity.old_rect.right:
							enemy.rect.left = entity.rect.right
							enemy.position.x = enemy.rect.x
						if enemy.rect.bottom >= entity.rect.top and enemy.old_rect.bottom <= entity.old_rect.top:
							enemy.rect.bottom = entity.rect.top
							enemy.position.y = enemy.rect.y
						if enemy.rect.top <= entity.rect.bottom and enemy.old_rect.top >= entity.old_rect.bottom:
							enemy.rect.top = entity.rect.bottom
							enemy.position.y = enemy.rect.y

		if (entity.position - self.player_position).length() < 40:
				entity.direction.x = 0
				entity.direction.y = 0
    
		entity.position.x += entity.direction.x * self.speed
		entity.position.y += entity.direction.y * self.speed			

      
		if not (0 < entity.position.x < width - entity.width):
			entity.position.x -= entity.direction.x * self.speed
			entity.direction.x *= -1
		if not (0 < entity.position.y < height - entity.height):
			entity.position.y -= entity.direction.y * self.speed
			entity.direction.y *= -1
		
		
		dx , dy = self.player_position[0] - entity.position.x , self.player_position[1] - entity.position.y
		angle = math.degrees(math.atan2(-dy, dx)) - 360
		entity.angle = angle
		entity.rotated_sprite = entity.rotate_center(entity.sprite, entity.sprite.get_rect(), -entity.angle)
		entity.rotated_turret_sprite = entity.rotate_center(entity.sprite, entity.sprite.get_rect(), -entity.angle)
		entity.aim_angle = angle

class PlayerHunterController(Controller):

	def __init__(self, speed=2, sight_range=300, sprint=2):
		self.speed = speed
		self.speed_original = speed
		self.sprint = sprint
		self.sight = sight_range

	def view_world(self, entity, world):
		self.speed = self.speed_original * world.difficulty.speed_mod
		if (entity.position - world.player.position).length() < self.sight:
			self.player_position = Vector2(world.player.position)
			self.speed = self.sprint * world.difficulty.speed_mod
		else:
			self.player_position = None

	def control(self, entity):
		
  
		entity.position += entity.direction * self.speed

		if self.player_position:
			entity.direction = (self.player_position - entity.position).normalize()

		if not (0 < entity.position.x < width - entity.width):
			entity.position.x -= entity.direction.x * self.speed
			entity.direction.x *= -1
		if not (0 < entity.position.y < height - entity.height):
			entity.position.y -= entity.direction.y * self.speed
			entity.direction.y *= -1


class EnemyHunterController(Controller):

	def __init__(self, target, speed=8):
		self.speed = speed
		self.target = target
		self.target_position = target
		self.locked_target = None

	def view_world(self, entity, world):
		for e in world.entities:
			if (isinstance(e,Tank)) == True and not e.is_player:
				actual_position = Vector2(e.position.x + e.width/2, e.position.y + e.height/2)
				if (actual_position - self.target).length() < e.collision_radius + 10 and not self.locked_target:
					self.locked_target = e
					self.target_position = self.locked_target.position


	def control(self, entity):
		entity.position += entity.direction * self.speed

		if self.target_position:
			entity.direction = (self.target_position - entity.position).normalize()


class TargeterController(Controller):

	def __init__(self, target, start_direction, deviation=0, speed=2):
		self.speed = speed
		self.target = target + Vector2(random.uniform(-deviation, deviation), random.uniform(-deviation, deviation))
		self.target_position = self.target
		self.speed_original = speed
		self.total_distance = None
		self.distance = self.total_distance
		self.proportion = 0.01

		self.start_direction = start_direction

	def view_world(self, entity, world):
		self.speed = self.speed_original * world.difficulty.speed_mod
		if not self.total_distance:
			self.total_distance = (self.target_position - entity.position).length()
			self.distance = self.total_distance

	def control(self, entity):
		self.proportion *= 1.5
		self.speed = min(35, self.speed + 1)

		self.distance = (self.target_position - entity.position).length()

		entity.direction = (((self.target_position - entity.position).normalize()*self.proportion + self.start_direction) / 2).normalize()

		entity.position += entity.direction * self.speed


class BasicTargetingController(Controller):

	def __init__(self, min_fire_time=60, max_fire_time=140, fire_range=200):
		self.min_fire_time = min_fire_time
		self.max_fire_time = max_fire_time
		self.range = fire_range

		self.player_position = None
		self.fire_cooldown = random.randint(self.min_fire_time, self.max_fire_time)

	def view_world(self, entity, world):
		
		if (entity.position - world.player.position).length() < self.range:
			self.player_position = Vector2(world.player.position)
		else:
			self.player_position = None
		self.world_entities = world.entities
  
	def control(self, entity):
		self.fire_cooldown -= 1
		if self.fire_cooldown < 0 and self.player_position:
			bullet_direction = (self.player_position - entity.position).normalize()
			bullet = Bullet(entity.position, bullet_direction, entity)
			entity.spawn.append(bullet)
			self.fire_cooldown = random.randint(self.min_fire_time, self.max_fire_time)

				

class LightTargetingController(Controller):

	def __init__(self, fire_cooldown=5, fire_range=250):
		self.max_fire_cooldown = fire_cooldown
		self.fire_cooldown = fire_cooldown
		self.range = fire_range

	def view_world(self, entity, world):
		if (entity.position - world.player.position).length() < self.range:
			self.player_position = Vector2(world.player.position)
		else:
			self.player_position = None

	def control(self, entity):
		self.fire_cooldown -= 1
		if self.fire_cooldown < 0 and self.player_position:
			bullet_direction = (self.player_position - entity.position).normalize()
			bullet = Bullet(entity.position, bullet_direction, entity, damage=1, size=1, speed=12)
			entity.spawn.append(bullet)
			self.fire_cooldown = self.max_fire_cooldown


class ShotgunTargetingController(Controller):

	def __init__(self, fire_cooldown=60, fire_range=200):
		self.max_fire_cooldown = fire_cooldown
		self.fire_cooldown = fire_cooldown
		self.range = fire_range

	def view_world(self, entity, world):
		if (entity.position - world.player.position).length() < self.range:
			self.player_position = Vector2(world.player.position)
		else:
			self.player_position = None

	def control(self, entity):
		self.fire_cooldown -= 1

		if self.fire_cooldown < 0 and self.player_position:
			bullet_direction = (self.player_position - entity.position).normalize()
			for i in range(15):
				new_direction = Vector2(bullet_direction)
				new_direction.rotate_ip(random.uniform(-4, 4))
				pellet = Pellet(entity.position + Vector2(entity.width / 2, entity.height / 2), new_direction, entity, damage=3,
				                speed=random.uniform(10, 14))
				entity.spawn.append(pellet)
			self.fire_cooldown = self.max_fire_cooldown


class EnemyHealerController(Controller):

	def __init__(self, heal_radius=300):
		self.range = heal_radius
		self.patients = []

	def view_world(self, entity, world):
		for other in world.entities:
			for i in range(len(self.patients)):
				if other is not self.patients[i]:
					if other is not entity and type(other) is Tank and not other.is_player:
						if (entity.position - other.position).length() < self.range:
							self.patients.append(other)

	def control(self, entity):
		for patient in self.patients:
			patient.health += 0.02


class EnemyScannerController(Controller):

	def __init__(self, sight_range=1000, range=1000):
		self.sight = sight_range
		self.range = range
		self.world_entities = []

	def view_world(self, entity, world):
		if (entity.position - world.player.position).length() < self.sight:
			self.player_position = Vector2(world.player.position)
		else:
			self.player_position = None
		self.world_entities = world.entities

	def control(self, entity):

		if self.player_position:
			entity.direction = (self.player_position - entity.position).normalize()
			for enemy in self.world_entities:
				if type(enemy) is Tank and not enemy.is_player and (entity.position - enemy.position).length() < self.range:
					enemy.direction = (self.player_position - enemy.position).normalize()
				if type(entity) != Tank:
					if (entity.position - enemy.position).length() < 10:
						enemy.direction.x = 0
						enemy.direction.y = 0


					


class BeamTargetingController(Controller):

	def __init__(self, fire_cooldown=40, fire_range=200):
		self.max_fire_cooldown = fire_cooldown
		self.fire_cooldown = fire_cooldown
		self.range = fire_range
		self.damage = 3
		self.max_damage = 15

	def view_world(self, entity, world):
		if (entity.position - world.player.position).length() < self.range:
			self.player_position = Vector2(world.player.position)
		else:
			self.player_position = None

	def control(self, entity):
		self.fire_cooldown -= 1
		if not self.player_position:
			self.damage = max(self.damage - 1, 0)

		if self.fire_cooldown < 0 and self.player_position:
			colour = (255, 0, 150)
			if self.damage < 5:
				colour = (0, 255, 240)
			beam_direction = (self.player_position - entity.position).normalize()
			beam = Beam(entity.position + Vector2(entity.width / 2, entity.height / 2), beam_direction, entity,
			            damage=self.damage, colour=colour, width=5, range=200)
			entity.spawn.append(beam)
			self.damage = min(self.damage + 4, self.max_damage)
			self.fire_cooldown = self.max_fire_cooldown

class HealthController(Controller):
	def __int__(self,speed_mod = 1.2,speed = 0.1,range = 1000):
		self.speed_mod = speed_mod
		self.speed = speed
		self.range = range
	def view_world(self,entity,world):
		self.entities = world.entities
		for ent in self.entities:
				if (isinstance(ent,Tank)) == True  and ent.is_player and (entity.position - ent.position).length() < 100:
						entity.direction = (entity.position - ent.position).normalize()
						

	
class SpawnEnemyController(Controller):
	def __init__(self, spawn_time=1000):
		self.spawn_time = spawn_time
		self.plevel  = 1
		self.spawn_cooldown = spawn_time

	def control(self, entity):
		self.spawn_cooldown -= 1
		if self.spawn_cooldown <= 0:
			for ent in self.entities:
				if (isinstance(ent,Tank)) == True  and ent.is_player:
					self.plevel  = ent.level
			enemy = factories.create_basic_enemy(entity.position,self.plevel)
			entity.spawn.append(enemy)
			self.spawn_cooldown = self.spawn_time
	def view_world(self, entity, world):
		self.entities = world.entities
		
class ShieldController(Controller):
	def __init__(self,cooldown = 100 , shield = 1):
		self.cooldown = cooldown
		self.max_cooldown = cooldown
	
	def view_world(self, entity, world):
		self.entitites = world.entities
	def control(self,entity):
		entity.shield.control(entity,self.entitites)
class PlaneController(Controller):
	def __init__(self, cooldown=1000):	
		self.max_cooldown = cooldown
		self.cooldown = cooldown
	def control(self, entity):
		entity.bomb.control(entity)
			
class PlayerController(Controller):

	def __init__(self, speed=2):
		self.speed = speed

		self.max_speed = speed
		self.max_weapon_switch_cooldown = 10
		self.weapon_switch_cooldown = 0
		
		self.main_select = True
		self.main_idx = [0,2,4,7,8,9]
		self.second_idx = [1,3,5,6]
		self.main_weapon = 2
		self.second_weapon = 3
		self.mouse_x = mouse.get_pos()[0]
		self.mouse_y = mouse.get_pos()[1]

		self.mock_x = 5
		self.mock_y = 5
  
		self.sound = pygame.mixer.Sound(sound.changeGun)
		self.sound.set_volume(sound.changeGun_vol)
	def control(self, entity):
		keys = pygame.key.get_pressed()
		move = Vector2()
		self.mouse_x = mouse.get_pos()[0]
		self.mouse_y = mouse.get_pos()[1]
		angle = 0
		if keys[K_a]:
			move += Vector2(-1, 0)
			
		if keys[K_d]:
			move += Vector2(1, 0)
			
		if keys[K_w]:
			move += Vector2(0, -1)
			
	
		if keys[K_s]:
			move += Vector2(0, 1)

		self.player_x = entity.get_centre()[0]
		self.player_y = entity.get_centre()[1]

		self.player_y = height/2
		self.player_x = width/2
		#pygame.mouse.set_pos(self.player_x,self.player_y)
		#print("Mouse pos : ", pygame.mouse.get_pos())
		self.player_x,self.player_y = round(self.player_x) , round(self.player_y)
		#pygame.mouse.set_pos(self.player_x,self.player_y)

		mouse_x = pygame.mouse.get_pos()[0]
		mouse_y = pygame.mouse.get_pos()[1]
		dx = self.player_x - mouse_x
		dy = self.player_y - mouse_y
		rads = atan2(-dy,dx)
		rads %= 2*pi
		self.degs = degrees(rads)
		
		
		if move.length_squared():
			new_position = entity.position + move.normalize() * self.speed

			if move.normalize().x == 0 and move.normalize().y == -1:
				angle = 90
			if move.normalize().x > 0 and move.normalize().x < 1 and move.normalize().y > -1 and move.normalize().y < 0:
				angle = 45
				
			if move.normalize().x == 1 and move.normalize().y == 0:
				angle = 0
			if move.normalize().x > 0 and move.normalize().x < 1 and move.normalize().y > 0 and move.normalize().y < 1:
				angle = 315
			if move.normalize().x == 0 and move.normalize().y == 1:
				angle = 270
			if move.normalize().x < 0 and move.normalize().x > -1 and move.normalize().y > 0 and move.normalize().y < 1:
				angle = 225
			if move.normalize().x == -1 and move.normalize().y == 0:
				angle = 180
			if move.normalize().x < 0 and move.normalize().x > -1 and move.normalize().y < 0 and move.normalize().y > -1:
				angle = 135
			#print(self.mouse)
			entity.rotated_sprite = entity.rotate_center(entity.sprite, entity.sprite.get_rect(), -entity.angle)
			entity.angle = angle

			if 0 < new_position.x < width - entity.width and 0 < new_position.y < height - entity.height:
				entity.position = new_position

		self.weapon_switch_cooldown -= 1
		button1, button2, button3 = mouse.get_pressed()
		#print(self.mock_x,self.mock_y)
		#print(self.main_idx[self.main_weapon])
		
		if button3 and self.weapon_switch_cooldown <= 0:
			
			self.sound.play()
			if self.main_select:
				entity.current_weapon = self.main_idx[self.main_weapon]
				self.main_select = False
				#entity.current_weapon = (entity.current_weapon + 1) % len(entity.weapons) # 0 - 9		
			else:	
				entity.current_weapon = self.second_idx[self.second_weapon]
				self.main_select = True
			self.weapon_switch_cooldown = self.max_weapon_switch_cooldown
		if self.main_select:
			entity.current_weapon = self.main_idx[self.main_weapon]
		else:
			entity.current_weapon = self.second_idx[self.second_weapon]
   
		
		
		#print(entity.weapons[8])
		entity.weapons[entity.current_weapon].control(entity, self.get_aim_direction(entity, pygame.mouse.get_pos()),  pygame.mouse.get_pos(), mouse.get_pressed())
		if type(entity.weapons[entity.current_weapon]) is SniperRifle:
			self.speed = 1
		else:
			self.speed = self.max_speed
		for weapon in entity.weapons:
			weapon.control(entity, self.get_aim_direction(entity, pygame.mouse.get_pos()), None, (False, False, False))
		
	def get_aim_direction(self, entity, position):
		#target_dir = (position - entity.get_centre()).normalize()
		test = Vector2(self.player_x,self.player_y)
		target_dir = (position - test ).normalize()
		entity.rotated_turret_sprite = entity.rotate_center(entity.turret_sprite, entity.turret_sprite.get_rect(), -entity.aim_angle)
		entity.aim_angle = -(((math.atan2(target_dir.y, target_dir.x) * (180/math.pi))) % 360)
		return entity.position + (target_dir).normalize() #* 1000
		
	def die(self, entity, killer):
		print(killer)
		entity.gameOver = True
		entity.position = Vector2(-1000, -1000)
		#entity.remove = True
		