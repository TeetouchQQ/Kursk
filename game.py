from pyprobs import Probability as pr
import pygame, sys
import math
import random, pdb
from scipy.interpolate import interp1d
import pygame
from pygameZoom import PygameZoom
from pygame.locals import *
from pygame import draw
from pygame import gfxdraw
from pygame.math import Vector2
from pygame import mouse
from pygame import font
from pytmx.util_pygame import load_pygame
import pygame
from collections import OrderedDict
import re
import pyscroll.data
from pyscroll.group import PyscrollGroup
import weapons
import projectile
from tank import Tank
from projectile import Projectile
from tank import Tank
import factories
import button
from config import width, height
import config
import pygame_textinput
from world import World
from Player import Player
from scipy.interpolate import interp1d
import config
import time
import sound

class Game():
	def __init__(self):
		#self.bg_img = pygame.image.load('map1.png')
		self.background = (0, 0, 0)
		self.world = World()
		#STATE
		self.paused = True
		self.main_menu = True
		self.weapon_select = True
		self.levelUp = False
		self.input_name = False
		self.gameOver = False
		self.showBoard = False
		self.chosen_weapons = []
		self.gameStart = False

		self.pygameZoom = PygameZoom(width, height)
		self.pygameZoom.set_zoom_strength(2)
  
		self.boss_spawn = False
		self.tank_cnt = 0
		self.exp_bar = 0
		self.level = 1
		self.barMax = self.level * 100
		self.kill = 0
		self.P = 0
		self.name = ''
		
		
		self.pastMouseX = 0
		self.pastMouseY = 0	
		self.MouseX = 0
		self.MouseY = 0
  
		self.map_bg = pygame.image.load(config.map_bg)
		self.map_bg = pygame.transform.scale(self.map_bg, (width,height))
  
  
		self.basicgun_logo = pygame.image.load(config.basicgun_logo)
		self.burstgun_logo = pygame.image.load(config.burstgun_logo)
		self.machinegungun_logo = pygame.image.load(config.machinegun_logo)
		self.shotgun_logo = pygame.image.load(config.shotgun_logo)
		self.sniper_logo = pygame.image.load(config.sniper_logo)
		self.beamgun_logo = pygame.image.load(config.beamgun_logo)
		self.flamegun_logo = pygame.image.load(config.flamethrower_logo)
		self.rocketlauncher = pygame.image.load(config.rocketlauncher_logo)


		self.health_logo = pygame.image.load(config.health_logo)
		self.damage_logo = pygame.image.load(config.damage_logo)
		self.exp_logo = pygame.image.load(config.exp_logo)
		self.plane_logo = pygame.image.load(config.plane_logo)
		self.shield_logo = pygame.image.load(config.shield_logo)
  
		
  
		self.logo_size = 200

		self.basicgun_logo = pygame.transform.scale(self.basicgun_logo, (self.logo_size, self.logo_size))
		self.burstgun_logo = pygame.transform.scale(self.burstgun_logo, (self.logo_size, self.logo_size))
		self.shotgun_logo = pygame.transform.scale(self.shotgun_logo, (self.logo_size, self.logo_size))
		self.machinegungun_logo = pygame.transform.scale(self.machinegungun_logo, (self.logo_size, self.logo_size))
		self.sniper_logo = pygame.transform.scale(self.sniper_logo, (self.logo_size, self.logo_size))
		self.beamgun_logo = pygame.transform.scale(self.beamgun_logo, (self.logo_size, self.logo_size))
		self.flamegun_logo = pygame.transform.scale(self.flamegun_logo, (self.logo_size, self.logo_size))
		self.rocketlauncher = pygame.transform.scale(self.rocketlauncher, (self.logo_size, self.logo_size))

		self.levelUp_bg = pygame.image.load(config.levelup_bg)
		self.levelUp_bg = pygame.transform.scale(self.levelUp_bg, (300, 300))
  
		self.pause_logo =pygame.image.load(config.pause_logo)
		self.pause_logo = pygame.transform.scale(self.pause_logo, (300, 150))
		##TIME
		self.timeStop = False
		self.startTime = 0
		self.time  = time.time()
		self.toDelTime = 0
		self.stopStart = 0
		self.stopEnd = 0
		self.last_sec = 0
		self.ticks=0
		self.sec = 0
		self.minute  =0
		self.font1 = pygame.font.Font('8-BIT WONDER.TTF',20)
		self.font2 = pygame.font.SysFont(None, 35)
		self.font3 = pygame.font.SysFont(None, 80)
		self.textinput = pygame_textinput.TextInputVisualizer(font_object=self.font3)
  
		self.timeShow = ""
		for i in range(10):
			self.chosen_weapons.append(True)

		self.keybinds = {
			(KEYDOWN, K_ESCAPE): sys.exit,
			(QUIT, None): sys.exit,
			#(KEYDOWN, K_q): pdb.set_trace,
			(KEYDOWN, K_p): self.world.add_enemies,
			#(KEYDOWN, K_o): self.spawn_player,
			#(KEYDOWN, K_F11): self.fullscreen,
			(KEYDOWN, K_SPACE): self.toggle_pause
			#(KEYDOWN, K_t): self.start,
			#(KEYDOWN, K_BACKSPACE): self.menu,
		}




	def update(self):
		
  
		if self.input_name:
			self.textinput.update(pygame.event.get())
		for event in pygame.event.get():
			handler = self.keybinds.get((event.type, getattr(event, 'key', None)))
			if handler:
				handler()
		self.pastMouseX = self.MouseX
		self.pastMouseY = self.MouseY 
  
		self.MouseX = pygame.mouse.get_pos()[0]
		self.MouseY = pygame.mouse.get_pos()[1]
		if not self.paused and self.timeStop == False:
			
			for entity in self.world.entities:
				entity.view_world(self.world)

			for entity in self.world.entities:
				entity.update()

			self.do_collisions()

			for entity in self.world.entities:
				self.world.entities += entity.spawn
				entity.spawn = []
			i = 0
			while i < len(self.world.entities):
				if self.world.entities[i].remove:
					self.world.entities.pop(i)
					i -= 1
				i += 1
		else:
			self.timeStop = True
			
	def text_objects(self,text,font):
		textSurface = font.render(text,True,(255,255,255))
		return textSurface , textSurface.get_rect()
	def rainFall(self):
		self.rain = []
		for q in range(700):
			x = random.randrange(0,config.width)
			y = random.randrange(0,800)
			self.rain.append([x,y])
		
	def button(self,screen,msg,x,y,w,h,ic,ac,action=None):
		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		blink = pygame.mixer.Sound(sound.blink_menu)
		blink.set_volume(sound.blink_menu_vol)
		hover = True
		pastMouse = (self.pastMouseX,self.pastMouseY)

		# print("<------>")
		# print(self.pastMouseX)
		# print(self.pastMouseY)
		# print("=========")
		# print(mouse)
		# if pastMouse != mouse:
		# 	print(pastMouse)
		if x+w > mouse[0] > x and y+h > mouse[1] >y:
			pygame.draw.rect(screen,ac,(x,y,w,h))
			if (x+w-2 > round(pastMouse[0]) > x+2 and y+h-2 > round(pastMouse[1]) > y+2) == False:
				blink.play()

			if click[0] == 1 and action != None:
				action()
				

		else:
			pygame.draw.rect(screen,ic,(x,y,w,h))
			hover = False

		textSurf , textRect = self.text_objects(msg,self.font1)
		textRect.center  =((x+(w/2),(y+(h/2))))
		screen.blit(textSurf,textRect)
	def add_outline_to_image(self,image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pygame.Surface:
		mask = pygame.mask.from_surface(image)
		mask_surf = mask.to_surface(setcolor=color)
		mask_surf.set_colorkey((0, 0, 0))

		new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
		new_img.fill(color_key)
		new_img.set_colorkey(color_key)

		for i in -thickness, thickness:
			new_img.blit(mask_surf, (i + thickness, thickness))
			new_img.blit(mask_surf, (thickness, i + thickness))
		new_img.blit(image, (thickness, thickness))

		return new_img
	def draw_text(self,screen,text, color, size, x, y):
		text = self.font1.render(text, False, color)
		text_rect = text.get_rect(center=(x, y))
		screen.blit(text, text_rect)
	def draw_gui(self,screen,entity):
		
		pygame.draw.rect(self.zoom_surf,(255,255,255),(0,0,self.exp_bar,30))
		pygame.draw.rect(self.zoom_surf,(33,29,52,255),(0,22,width,30))
		
		pygame.draw.rect(self.zoom_surf,(129,255,8),(0,22,self.exp_bar,25))
		pygame.draw.rect(self.zoom_surf,(104,192,30),(0,30,self.exp_bar,20))
  
		font=pygame.freetype.SysFont(None, 25)
		font.origin=True


		#Show level
		fontlevel = pygame.font.Font('8-BIT WONDER.TTF',20)
		text_surface = fontlevel.render("LV "+str(entity.level), False, (255,255,255))
		text_with_ouline = self.add_outline_to_image(text_surface, 2, (1, 1, 1))
		screen.blit(text_with_ouline, (width/2,23))
  
		#font.render_to(self.zoom_surf, (50, 240),'Name : '+ str(self.name2),pygame.Color('dodgerblue'))
		#### Time ###
		fontTime=pygame.font.SysFont("arial", 35)

		out='{minutes:02d}:{seconds:02d}'.format(minutes=self.minute, seconds=self.sec)	
		self.timeShow = out
		#font.render_to(self.zoom_surf, (width/2, 100), out,pygame.Color('dodgerblue'))
		text_surf = fontTime.render(str(out), False, (255, 255, 255))
		text_with_ouline = self.add_outline_to_image(text_surf, 2, (5, 5, 5))
		self.zoom_surf.blit(text_with_ouline,(width/2, 60))
		###
		#print(entity.weapons[entity.current_weapon].name)
  

		if entity.weapons[entity.current_weapon].name == "Basic Gun":
			screen.blit(self.basicgun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Burst Gun":
			screen.blit(self.burstgun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Shotgun":
			screen.blit(self.shotgun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Machine Gun":
			screen.blit(self.machinegungun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Mega Beam":
			screen.blit(self.sniper_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Beam Gun":
			screen.blit(self.beamgun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Flamethrower":
			screen.blit(self.flamegun_logo,(100,50))
		elif entity.weapons[entity.current_weapon].name == "Rocket Launcher":
			screen.blit(self.rocketlauncher,(100,50))
		#DRAW GUN

		
	def draw(self, screen):
		
  
		if self.timeStop == False:
			self.time = time.time()
		if self.paused == False and self.main_menu == False and self.levelUp == False and self.gameOver == False:
			#print(self.timeStop)
			screen.blit(self.map_bg, (0, 0))
			player_x = 0
			player_y = 0
			self.tank_cnt = 0
			for entity in self.world.entities:
				entity.draw(screen)
			
				if entity is self.world.player:
					
					player_x = self.world.player.position.x
					player_y = self.world.player.position.y
					
					#Level Logic
					self.exp_bar = entity.exp*(width/entity.exp_perLevel)
					if self.exp_bar >= width:
         
						pygame.mixer.pause()
						self.stopStart = time.time()
						self.rainFall()
						self.levelUp = True
						entity.level +=1
						self.level = entity.level
						entity.exp = 0
				
						self.timeStop = True
						self.upAvalible = []
						if entity.controllers[0].main_weapon < 3:
							self.upAvalible.append('Main')
					
						if entity.controllers[0].second_weapon < 3:
							self.upAvalible.append('Second')

						self.upAvalible.append('Damage')
						self.upAvalible.append('Bonus')
						self.upAvalible.append('Health')
      
						self.upAvalible.append('Plane')
						self.upAvalible.append('Shield')
      
						random.shuffle(self.upAvalible)
						self.sample_list = self.upAvalible[:3]
				if (isinstance(entity,Tank)):
					self.tank_cnt += 1
					
			#900 + 700 /2
	
			wnd_w, wnd_h = screen.get_size()
			zoom_size = (round(wnd_w/config.zoom), round(wnd_h/config.zoom))
			zoom_area = pygame.Rect(0, 0, *zoom_size)
			zoom_area.center = (player_x, player_y)
			self.zoom_surf = pygame.Surface(zoom_area.size)
			self.zoom_surf.fill((0,0,0))
			self.zoom_surf.blit(screen, (0, 0), zoom_area)
   
			

			self.zoom_surf = pygame.transform.scale(self.zoom_surf, (wnd_w, wnd_h))

			font=pygame.freetype.SysFont(None, 20)
			font.origin=True
			font.render_to(self.zoom_surf,(1200,870),"65010478 Teetouch Jaknamon" ,pygame.Color('white'))
			#print((self.time - self.startTime) - abs(self.stopEnd - self.stopStart))
			second = (self.time - self.startTime) - self.toDelTime
 
			self.sec = math.floor(second % 60)
			self.minute = math.floor(second / 60)
			if self.minute== 10:
				self.spawn_boss(self.world.entities)
			if config.sps % 1 == 0 and self.last_sec != self.sec and self.boss_spawn == False:
				if pr.prob(config.mothership_probs + (self.level / 1000)):
					self.world.spawn_Mothership(round(1 + round(self.level / 200)),self.level)
					
				if pr.prob(config.lighttank_probs + (self.level / 900)):
					self.world.spawn_lightTank(round(1 + round(self.level / 80)),self.level)
					
				if pr.prob(config.shotgun_probs + (self.level / 900)): 
					self.world.spawn_Beamer(round(1 + round(self.level / 80)),self.level)
					
				if pr.prob(config.scanner_probs + (self.level / 900)):
					self.world.spawn_Scanner(round(1 + round(self.level / 80)),self.level)
					
				if pr.prob(config.shotgun_probs + (self.level / 900)):
					self.world.spawn_Shotgun(round(1 + round(self.level / 80)),self.level) 
     
				if pr.prob(config.basic_probs + (self.level / 900)):
					self.world.spawn_basic(round(1 + round(self.level / 80)),self.level)
				self.last_sec = self.sec
				

   
			for entity in self.world.entities:
				if (isinstance(entity,Tank)) == True:
					if entity.gameOver == True:
						self.gameOver = True
						print('Save GAME')

						#self.draw_GameOver(self.zoom_surf)
				if entity is self.world.player:
					#print(self.name2)
					self.draw_gui(self.zoom_surf,entity)
					

			screen.blit(self.zoom_surf, (0, 0))
			
		elif self.levelUp == True and self.paused == False and self.main_menu == False:
			for entity in self.world.entities:
				if entity is self.world.player:
					self.draw_levelUp(screen,self.sample_list)

		elif self.gameOver == True:
			self.draw_GameOver(screen)
		
			print('GameOver')
			
		
		elif self.main_menu == True:
			screen.fill(self.background)
			self.draw_mainMenu(screen)
		elif self.main_menu == False and self.paused == True and self.levelUp == False and self.gameStart == True:
			
			
			self.draw_pauseScreen(screen)
   
		if self.input_name == True:
			self.draw_CharacterInput(screen)
			if len(self.textinput.value) > 0:
				self.name2 = self.textinput.value
    
		if self.showBoard == True:
			self.draw_Board(screen)
			
			
	def spawn_boss(self,entities):
		if self.boss_spawn == False:
			for ent in entities:
				if(isinstance(ent,Tank) and ent.is_player == False):
					ent.remove = True
			self.boss_spawn = True
			self.world.spawn_BOSS(5)
    
	def spawn_player(self):
		if self.world.player.remove:
			self.world.player = factories.create_player(Vector2(1, 1), self.chosen_weapons)
			self.world.entities.append(self.world.player)

	def do_collisions(self):
		for entity in self.world.entities:
			for other in self.world.entities:
				if entity is not other and entity.should_collide(other) and entity.collide(other):
					entity.handle_collision(other)

	def draw_weapon_select(self, screen):
		for i in range(10):
			self.world.all_weapons[i].draw(screen, 100, (i + 1) * 50 + 20, self.chosen_weapons[i])
	def toggle_character(self):
		self.paused = True
		#self.time = 0
		self.input_name = True
  
		self.main_menu = False
		self.world.entities = []
		self.world.player = None
		self.weapon_select = True
		self.timeStop = True
	def save_name(self):
		self.input_name = False
		self.start()
	def record_score(self):
		with open('leaderboard.txt', 'a') as the_file:
				the_file.write(self.name2 + ',' + str(self.minute) + ':' + str(self.sec)+'\n')
		self.name2 = ''
		self.menu()
		
  
	#========================= LEVEL ============================================================================
	def levelUp_Maingun(self):
		print('levelUP Main')
		self.levelUp = False
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.controllers[0].main_weapon += 1
				entity.controllers[0].current_weapon = entity.controllers[0].main_idx[entity.controllers[0].main_weapon]

		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.levelUp = False
		self.timeStop = False
		pygame.mixer.unpause()
	def levelUp_Secondgun(self):
		#print('levelUP Sec')
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.controllers[0].second_weapon += 1
		

		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def levelUp_damage(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.damage_bonus *= 1.1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def levelUp_Exp(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.expBonus *= 1.1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def levelUp_health(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_health +=1
				entity.max_health *= 1.05
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def levelUp_Shield(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_Shield  +=1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def levelUp_Plane(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_Shield  +=1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
		pygame.mixer.unpause()
	def draw_levelUp(self,screen,sample_list):
		#print('level up draw')
		to_up = ['Main','Second','Damage','Bonus','Health']
		
		level_bg = pygame.image.load(config.level_bg)
		level_bg = pygame.transform.scale(level_bg, (1000,600))
  
		screen.blit(self.map_bg, (0, 0))
		for entity in self.world.entities:
				entity.draw(screen)
			
				if entity is self.world.player:
					
					player_x = self.world.player.position.x
					player_y = self.world.player.position.y
   
		wnd_w, wnd_h = screen.get_size()
		zoom_size = (round(wnd_w/config.zoom), round(wnd_h/config.zoom))
		zoom_area = pygame.Rect(0, 0, *zoom_size)
		zoom_area.center = (player_x, player_y)
		self.zoom_surf = pygame.Surface(zoom_area.size)
		self.zoom_surf.fill((0,0,0))
		self.zoom_surf.blit(screen, (0, 0), zoom_area)
		self.zoom_surf = pygame.transform.scale(self.zoom_surf, (wnd_w, wnd_h))
  
		for entity in self.world.entities:
			if entity is self.world.player:
				ent = entity
				#print(self.name2)
				self.draw_gui(self.zoom_surf,entity)

				#name = self.font1.render("John Hubbard", True, (0,0,255))
				
				#self.font2.render(self.zoom_surf, (50, 220),'Weapon : '+ str(entity.weapons[entity.current_weapon].name),pygame.Color('dodgerblue'))
		#pygame.draw.rect(self.zoom_surf,(255,255,255),(20,230,200,400))		
  
  
		nnamme = self.font2.render('Name : '+ str(self.name2),True,(0,0,0))
		Dmg_bonus = self.font2.render('Damage : '+ str(ent.damage_bonus*100) + "%",True,(0,0,0))
		Exp_bonus = self.font2.render('Exp bonus : '+ str(ent.expBonus*100) + "%",True,(0,0,0))
		maxHP = self.font2.render('maxHP : '+ str(ent.max_health),True,(0,0,0))
		Shield = self.font2.render('Shield : '+ str(ent.max_Shield),True,(0,0,0))
		pplane = self.font2.render('Plane CD : -'+ str(ent.planeLevel*10) + "%",True,(0,0,0))
		fire_res = self.font2.render('Fire resist : '+ str(ent.fire_resist) + "%",True,(0,0,0))
  
		screen.blit(self.zoom_surf, (0, 0))
		
		for i in self.rain:
			i[1] +=8
			pygame.draw.rect(screen, (255,255,255), (i, (2, 18)))
			#pygame.draw.circle(screen,(255,255,255),i,7)ds
			if i[1] > 850:
				i[1] = random.randrange(-50,-5)
				i[0] = random.randrange(config.width)
    
		
  
		screen.blit(level_bg, (300, 165))
		screen.blit(self.levelUp_bg,(670,30))
		
		# screen.blit(nnamme, (40,260))
		# screen.blit(Dmg_bonus, (40,290))
		# screen.blit(Exp_bonus, (40,320))
		# screen.blit(maxHP, (40,350))
		# screen.blit(Shield, (40,380))
		# screen.blit(pplane, (40,410))
		# screen.blit(fire_res, (40,440))
  
		font_Desc=pygame.freetype.SysFont(None, 20)
		font_Desc.origin=True
  
		for entity in self.world.entities:
			if entity is self.world.player:
				for i in range(len(sample_list)):
					if sample_list[i] == 'Main':
						
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
      
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
      
						font.render_to(screen, ((i*320)+385,350), "Main Slot",pygame.Color('white'))
						next = entity.controllers[0].main_idx[(entity.controllers[0].main_weapon)+1]
						new = entity.weapons[next].name
						new = re.sub("[\(\[].*?[\)\]]", "", new)

						font.render_to(screen, ((i*320)+385,400), new,pygame.Color('green'))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_Maingun)
						logo_x = (i*320)+385
						logo_y =  410
						show_size = 200
      
						if new == "Basic Gun":
							self.basicgun_logo = pygame.transform.scale(self.basicgun_logo, (show_size, show_size))
							screen.blit(self.basicgun_logo,(logo_x,logo_y))
						elif new == "Burst Gun":
							self.burstgun_logo = pygame.transform.scale(self.burstgun_logo, (show_size, show_size))
							screen.blit(self.burstgun_logo,(logo_x,logo_y))
						elif new == "Shotgun":
							self.shotgun_logo = pygame.transform.scale(self.shotgun_logo, (show_size, show_size))
							screen.blit(self.shotgun_logo,(logo_x,logo_y))
						elif new == "Machine Gun":
							self.machinegungun_logo = pygame.transform.scale(self.machinegungun_logo, (show_size, show_size))
							screen.blit(self.machinegungun_logo,(logo_x,logo_y))
						elif new == "Mega Beam":
							self.sniper_logo = pygame.transform.scale(self.sniper_logo, (show_size, show_size))
							screen.blit(self.sniper_logo,(logo_x,logo_y))
						elif new == "Beam Gun":
							self.beamgun_logo = pygame.transform.scale(self.beamgun_logo, (show_size, show_size))
							screen.blit(self.beamgun_logo,(logo_x,logo_y))
						elif new == "Flamethrower":
							self.flamegun_logo = pygame.transform.scale(self.flamegun_logo, (show_size, show_size))
							screen.blit(self.flamegun_logo,(logo_x,logo_y))
						elif new == "Rocket Launcher":
							self.rocketlauncher = pygame.transform.scale(self.rocketlauncher, (show_size, show_size))
							screen.blit(self.rocketlauncher,(logo_x,logo_y))
       
       
					if sample_list[i] == 'Second':

						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
      
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
						font.render_to(screen, ((i*320)+385,350), "Second Slot",pygame.Color('white'))
      
						next = entity.controllers[0].second_idx[(entity.controllers[0].second_weapon)+1]
						new = entity.weapons[next].name
						new = re.sub("[\(\[].*?[\)\]]", "", new)
     
						font.render_to(screen, ((i*320)+385,400), new,pygame.Color('green'))
						
      
	
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_Secondgun)
      
						logo_x = (i*320)+385
						logo_y =  410
						show_size = 200
      
			
						if new == "Basic Gun":
							self.basicgun_logo = pygame.transform.scale(self.basicgun_logo, (show_size, show_size))
							screen.blit(self.basicgun_logo,(logo_x,logo_y))
						elif new == "Burst Gun":
							self.burstgun_logo = pygame.transform.scale(self.burstgun_logo, (show_size, show_size))
							screen.blit(self.burstgun_logo,(logo_x,logo_y))
						elif new == "Shotgun":
							self.shotgun_logo = pygame.transform.scale(self.shotgun_logo, (show_size, show_size))
							screen.blit(self.shotgun_logo,(logo_x,logo_y))
						elif new == "Machine Gun":
							self.machinegungun_logo = pygame.transform.scale(self.machinegungun_logo, (show_size, show_size))
							screen.blit(self.machinegungun_logo,(logo_x,logo_y))
						elif new == "Mega Beam":
							self.sniper_logo = pygame.transform.scale(self.sniper_logo, (show_size, show_size))
							screen.blit(self.sniper_logo,(logo_x,logo_y))
						elif new == "Beam Gun":
							self.beamgun_logo = pygame.transform.scale(self.beamgun_logo, (show_size, show_size))
							screen.blit(self.beamgun_logo,(logo_x,logo_y))
						elif new == "Flamethrower":
							self.flamegun_logo = pygame.transform.scale(self.flamegun_logo, (show_size, show_size))
							screen.blit(self.flamegun_logo,(logo_x,logo_y))
						elif new == "Rocket Launcher":
							self.rocketlauncher = pygame.transform.scale(self.rocketlauncher, (show_size, show_size))
							screen.blit(self.rocketlauncher,(logo_x,logo_y))
       
					if sample_list[i] == 'Damage':
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
      
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
						font.render_to(screen, ((i*320)+385,350), "Damage",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_damage)

						##DESC
						font_Desc=pygame.freetype.SysFont(None, 20)
						font_Desc.origin=True
						font_Desc.render_to(screen, ((i*320)+385,390), "+10% Damage Bonus",pygame.Color('green'))
      
      
						logo_x = (i*320)+385
						logo_y = 410
						show_size = 200
      
						self.damage_logo = pygame.transform.scale(self.damage_logo, (show_size, show_size))
						screen.blit(self.damage_logo,(logo_x,logo_y))
      
					if sample_list[i] == 'Bonus':
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
						font.render_to(screen, ((i*320)+385,350), "Exp Bonus",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_Exp)
						font_Desc=pygame.freetype.SysFont(None, 20)
						font_Desc.origin=True
						font_Desc.render_to(screen, ((i*320)+385,390), "+10% xp Bonus",pygame.Color('green'))
      
						logo_x = (i*320)+385
						logo_y = 410
						show_size = 200
      
						self.exp_logo = pygame.transform.scale(self.exp_logo, (show_size, show_size))
						screen.blit(self.exp_logo,(logo_x,logo_y))
      
					if sample_list[i] == 'Health':
					
      
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
						font.render_to(screen, ((i*320)+385,350), "Health",pygame.Color('white'))
						
      
						font_Desc.render_to(screen, ((i*320)+385,390), "+10% Max HP",pygame.Color('green'))
      
						logo_x = (i*320)+385
						logo_y = 410
						show_size = 200

						self.health_logo = pygame.transform.scale(self.health_logo, (show_size, show_size))
						screen.blit(self.health_logo,(logo_x,logo_y))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_health)
					if sample_list[i] == 'Plane':
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
      
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
						font.render_to(screen, ((i*320)+375,350), "Bomber Plane",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_health)

						font_Desc.render_to(screen, ((i*320)+385,390), "-10% Plane CD",pygame.Color('green'))
    
						logo_x = (i*320)+385
						logo_y = 410
						show_size = 200
      
						self.plane_logo = pygame.transform.scale(self.plane_logo, (show_size, show_size))
						screen.blit(self.plane_logo,(logo_x,logo_y))
      

					if sample_list[i] == 'Shield':
         
				
						font=pygame.freetype.SysFont(None, 34)
						font.origin=True
      
						pygame.draw.rect(screen,(0,0,0),((i*320)+365,300,250,400))
						font.render_to(screen, ((i*320)+385,350), "Eletric Shield",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+390,600,200,80,(130,255,0),(255,0,0),self.levelUp_Shield)
      
						font_Desc.render_to(screen, ((i*320)+385,390), "+1 Max Shield",pygame.Color('green'))
      
						logo_x = (i*320)+385
						logo_y = 410
						show_size = 200
      
						self.shield_logo = pygame.transform.scale(self.shield_logo, (show_size, show_size))
						screen.blit(self.shield_logo,(logo_x,logo_y))
	#========================= LEVEL ============================================================================
	def draw_CharacterInput(self,screen):
     
     
		#bg = pygame.image.load(config.name_bg)
		#bg = pygame.transform.scale(bg, (width,height))

		#screen.blit(bg, (0, 0))
  
		screen.fill((0,0,0))
  
		pygame.draw.rect(screen,(255,255,255),(200,180,1150,570))
		pygame.draw.rect(screen,(0,0,0),(220,190,1100,550))
  
		font=pygame.freetype.SysFont(None, 50)
		font.origin=True
		font.render_to(screen, (260,420), "Enter your name : ",pygame.Color('white'))

		
  
		font=pygame.freetype.SysFont(None, 70)
		font.origin=True
		screen.blit(self.textinput.surface, (720, 380))
		self.textinput.font_color = (0, 2, 170)
		self.button(screen,"LETS GO",550,580,200,90,(20,200,20),(20,255,20),self.save_name)
		self.button(screen,"BACK",850,580,200,90,(200,15,15),(255,0,0),self.menu)
  
	def draw_Board(self,screen):
		screen.fill((0,0,0))
		show_dict = {}
		score_dict = {}
		f = open("leaderboard.txt", "r")
		for x in f:
			name = x.split(',')[0]
			sec = ((x.split(',')[1]).split(':')[1]).replace('/n','')
			minute = (x.split(',')[1]).split(':')[0]
			#print((name,minute,sec))
			show_dict[name] = str(minute) + ':' + str(sec)[:2]
			score = int(int(minute)*60) + int(sec)
			score_dict[name] = score
		#SORT
		z = dict(sorted(score_dict.items(), key=lambda item: item[1]))
		i = 0
		font=pygame.freetype.SysFont(None, 50)
		font.origin=True
		z = OrderedDict(reversed(list(z.items())))

		for name, value in z.items():
			i+=1
			if i > 5:
				break
			font.render_to(screen, (400, (i*90) + 120),name,pygame.Color('green'))
			font.render_to(screen, (800, (i*90) + 120),show_dict[name].replace(' ',''),pygame.Color('white'))
			self.button(screen,"MENU",600,650,150,90,(0,0,0),(255,0,0),self.menu)
			#print(name,show_dict[name])
			
  			

		font=pygame.freetype.SysFont(None, 34)
		font.origin=True
		font.render_to(screen, (550, 100), 'LeaderBoard',pygame.Color('Red'))

	def draw_pauseScreen(self,screen):
     
		#pygame.gfxdraw.box(screen, pygame.Rect(0,0,200,200), (100,0,0,1))
		
		pygame.draw.rect(screen,(252,186,119),(705,300,290,405))
		pygame.draw.rect(screen,(255,225,174),(710,300,280,400))
		
		pygame.draw.rect(screen,(0,0,0),(765,395,160,100))
		self.button(screen,"RESUME",770,400,150,90,(183,245,42),(255,0,0),self.toggle_pause)
		self.button(screen,"QUIT",770,550,150,90,(1,199,171),(255,0,0),self.menu)
		screen.blit(self.pause_logo,(700,250))
		#self.timeStop = True
	def draw_mainMenu(self, screen):
			bg = pygame.image.load(config.menu_bg)
			bg = pygame.transform.scale(bg, (width,height))

			screen.blit(bg, (0, 0))
			self.button(screen,"START A GAME",950,330,300,90,(0,0,0),(255,0,0),self.toggle_character)
			self.button(screen,"Leaderboard",950,440,300,90,(0,0,0),(255,0,0),self.toggle_board)
			self.button(screen,"OPTION",950,550,300,90,(0,0,0),(255,0,0))
			self.button(screen,"EXIT",950,660,300,90,(0,0,0),(255,0,0),sys.exit)
   
	def draw_GameOver(self,screen):

			pygame.mixer.stop()

			screen.fill((0,0,0))

			fontlevel = pygame.font.Font('8-BIT WONDER.TTF',140)
			text_surface = fontlevel.render(" GAME OVER ", False, (200,25,25))
			#text_with_ouline = self.add_outline_to_image(text_surface, 2, (1, 1, 1))
			screen.blit(text_surface, (100,220))
  
  
			
			font=pygame.freetype.SysFont(None, 50)
			font.origin=True
			font.render_to(screen,(750,500), str(self.timeShow) ,pygame.Color('white'))

  
			self.button(screen,"Continue",720,600,200,90,(100,200,30),(50,255,50),self.record_score)

	def draw_box(self, screen, x, y, active, string):
		draw.rect(screen, (80, 0, 0), (x, y, 110, 20))
		if active:
			draw.rect(screen, (255, 0, 0), (x, y, 110, 20))
		my_font = pygame.font.Font(None, 20)
		name = my_font.render(string, 1, (50, 255, 50))
		pygame.Surface.blit(screen, name, (x + 7, y + 5))


	def fullscreen(self):
		pygame.display.set_mode((width, height), pygame.FULLSCREEN)
	def toggle_board(self):
		self.showBoard = True
	def toggle_pause(self):
		#print(self.paused)


		if self.timeStop == False:
			self.stopStart = time.time()
			pygame.mixer.pause()
			
		else:
			self.stopEnd = time.time()
			pygame.mixer.unpause()
			self.toDelTime += abs(self.stopEnd - self.stopStart)
   
		self.paused = not self.paused
		self.timeStop = not self.timeStop
  
	def choose_weapon(self, num):
		def choose():
			if self.weapon_select:
				self.chosen_weapons[num] = not self.chosen_weapons[num]

		return choose

	def menu(self):
		self.name = ''
		self.input_name = False
		self.textinput.value = ''
		self.main_menu = True
		self.world.entities = []
		self.world.player = None
		self.weapon_select = True
		self.timeStop = True
		self.gameOver  = False
		self.showBoard = False
		self.toggle_pause()

		

	def start(self):
		self.boss_spawn = False
		self.startTime  = time.time()
		self.sec = 0
		self.minute  =0
		self.stopStart = time.time()
		self.main_menu = False
		self.timeStop == False
		self.gameStart = True
		#self.paused = True
		self.toDelTime = 0
		num_weapons = 0
		self.toggle_pause()
		self.world.add_enemies(1)
		for i in range(10):
			if self.chosen_weapons[i]:
				num_weapons += 1
		if num_weapons > 0:
			self.weapon_select = False
			#self.player = Player(self.input_name)
			self.world.player = factories.create_player(Vector2(450, 350), self.chosen_weapons)
			self.world.entities.append(self.world.player)
		


if __name__ == '__main__':
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption(config.title)
	g = Game()
	clock = pygame.time.Clock()
	while True:
		clock.tick()
		#print (clock.get_fps())
		
		g.update()		
		g.draw(screen)        
		pygame.display.flip()