# import the pygame module, and the
# sys module for exiting the window we create
import pygame, sys
import random, pdb
from pyprobs import Probability as pr
# import some useful constants
from pygame.locals import *
from pygame import draw
from pygame import gfxdraw
from pygame.math import Vector2
from pygame import mouse
from pygame import font

import weapons
import projectile
from tank import Tank
from projectile import Projectile
from tank import Tank
import factories

from config import width, height
import config

class World:
	
	def __init__(self):
		self.player = None
		self.difficulty = config.EasyDifficulty
		self.entities = []

		self.all_weapons = [
			weapons.BasicGun(),
			weapons.BurstGun(),
			weapons.Shotgun(),
			weapons.MachineGun(),
			weapons.SniperRifle(),
			weapons.BeamGun(),
			weapons.Flamethrower(),
			weapons.RocketLauncher(),
			weapons.MissileBarrage(),
			weapons.GuidedMissileLauncher()
		]

	def spawn_enemies(self):
		enemies = [factories.create_basic_enemy(self.bounds()) for i in range(self.difficulty.num_enemies)]
		motherships = [factories.create_mothership(self.bounds()) for i in range(self.difficulty.num_motherships)]
		light_enemies = [factories.create_light_enemy(self.bounds()) for i in range(self.difficulty.num_light_enemies)]
		shotgunner_enemies = [factories.create_shotgunner_enemy(self.bounds()) for i in range(self.difficulty.num_shotgunner_enemies)]
		beamer_enemies = [factories.create_beamer_enemy(self.bounds()) for i in range(self.difficulty.num_beamer_enemies)]
		scanner_enemies = [factories.create_scanner_enemy(self.bounds()) for i in range(self.difficulty.num_scanner_enemies)]
		return enemies + motherships + light_enemies + shotgunner_enemies + beamer_enemies + scanner_enemies
	def spawn_Mothership(self,amount):
		self.entities +=  [factories.create_mothership(self.bounds()) for i in range(amount)]
		

	def spawn_lightTank(self,amount):
		self.entities += [factories.create_light_enemy(self.bounds()) for i in range(amount)]
		

	def spawn_Shotgun(self,amount):
		self.entities += [factories.create_shotgunner_enemy(self.bounds()) for i in range(amount)]
  
	def spawn_Beamer(self,amount):
		self.entities +=  [factories.create_beamer_enemy(self.bounds()) for i in range(amount)]
	def spawn_Scanner(self,amount):
		self.entities +=  [factories.create_scanner_enemy(self.bounds()) for i in range(amount)]
	def add_enemies(self):
		self.entities += self.spawn_enemies()

	def bounds(self):
		return Vector2(random.randint(100, width - 100), random.randint(100, height - 100))