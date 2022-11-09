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
  
		self.exp_bar = 0
		self.level = 1
		self.barMax = self.level * 100
		self.kill = 0
		self.P = 0
		self.name = ''
		self.textinput = pygame_textinput.TextInputVisualizer()
		

		self.map_bg = pygame.image.load(config.map_bg)
		self.map_bg = pygame.transform.scale(self.map_bg, (width,height))
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
			x = random.randrange(0,1280)
			y = random.randrange(0,800)
			self.rain.append([x,y])
		
	def button(self,screen,msg,x,y,w,h,ic,ac,action=None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		if x+w > mouse[0] > x and y+h > mouse[1] >y:
			pygame.draw.rect(screen,ac,(x,y,w,h))
   
			if click[0] == 1 and action != None:
				action()

		else:
			pygame.draw.rect(screen,ic,(x,y,w,h))
		
		textSurf , textRect = self.text_objects(msg,self.font1)
		textRect.center  =((x+(w/2),(y+(h/2))))
		screen.blit(textSurf,textRect)
	def draw_text(self,screen,text, color, size, x, y):
		text = self.font1.render(text, False, color)
		text_rect = text.get_rect(center=(x, y))
		screen.blit(text, text_rect)
	def draw_gui(self,screen,entity):
		pygame.draw.rect(self.zoom_surf,(90,90,90),(0,10,width,height/16))
		pygame.draw.rect(self.zoom_surf,(255,0,0),(0,10,self.exp_bar,height/16))
		font=pygame.freetype.SysFont(None, 25)
		font.origin=True
		font.render_to(self.zoom_surf, (width/2, 42),'Level '+ str(entity.level),pygame.Color('black'))
		font.render_to(self.zoom_surf, (50, 130),'Damage : '+ str(entity.damage_bonus),pygame.Color('dodgerblue'))
		font.render_to(self.zoom_surf, (50, 160),'exp : '+ str(entity.expBonus),pygame.Color('black'))
		font.render_to(self.zoom_surf, (50, 190),'maxHP : '+ str(entity.max_health),pygame.Color('dodgerblue'))
		font.render_to(self.zoom_surf, (50, 220),'Weapon : '+ str(entity.weapons[entity.current_weapon].name),pygame.Color('dodgerblue'))
		font.render_to(self.zoom_surf, (50, 240),'Name : '+ str(self.name2),pygame.Color('dodgerblue'))
		font=pygame.freetype.SysFont(None, 34)
		font.origin=True
		out='{minutes:02d}:{seconds:02d}'.format(minutes=self.minute, seconds=self.sec)
		font.render_to(self.zoom_surf, (width/2, 100), out,pygame.Color('dodgerblue'))
	def draw(self, screen):
		if self.timeStop == False:
			self.time = time.time()
		if self.paused == False and self.main_menu == False and self.levelUp == False and self.gameOver == False:
			#print(self.timeStop)
			screen.blit(self.map_bg, (0, 0))
			player_x = 0
			player_y = 0
			
			for entity in self.world.entities:
				entity.draw(screen)
			
				if entity is self.world.player:
					
					player_x = self.world.player.position.x
					player_y = self.world.player.position.y
					
					#Level Logic
					self.exp_bar = entity.exp*(width/entity.exp_perLevel)
					if self.exp_bar >= width:
						self.stopStart = time.time()
						self.rainFall()
						self.levelUp = True
						entity.level +=1
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

					
			#900 + 700 /2
			
			wnd_w, wnd_h = screen.get_size()
			zoom_size = (round(wnd_w/config.zoom), round(wnd_h/config.zoom))
			zoom_area = pygame.Rect(0, 0, *zoom_size)
			zoom_area.center = (player_x, player_y)
			self.zoom_surf = pygame.Surface(zoom_area.size)
			self.zoom_surf.fill((0,0,0))
			self.zoom_surf.blit(screen, (0, 0), zoom_area)
			#self.zoom_surf = pygame.transform.scale2x(self.zoom_surf)
			game_resolution = (800, 600)
			#display_resolution = (width, height) # Or use a function to get the real screen res
			#stretch_to_fit_resolution = ((width^2)/(800), (height[1]^2)/600)

			self.zoom_surf = pygame.transform.scale(self.zoom_surf, (wnd_w, wnd_h))

			
			#print((self.time - self.startTime) - abs(self.stopEnd - self.stopStart))
			second = (self.time - self.startTime) - self.toDelTime

			self.sec = math.floor(second % 60)
			self.minute = math.floor(second / 60)
   
			if config.sps % 1 == 0 and self.last_sec != self.sec:
				if pr.prob(config.mothership_probs):
					self.world.spawn_Mothership(2)
					
				if pr.prob(config.lighttank_probs):
					self.world.spawn_lightTank(2)
					
				if pr.prob(config.shotgun_probs):
					self.world.spawn_Beamer(2)
					
				if pr.prob(config.scanner_probs):
					self.world.spawn_Scanner(2)
					
				if pr.prob(config.shotgun_probs):
					self.world.spawn_Shotgun(2) 
     
				if pr.prob(config.basic_probs):
					self.world.spawn_basic(2) 
				self.last_sec = self.sec
				
    
			#print(minute)
			#print(abs(self.stopEnd - self.stopStart))
			#Debugging
			
			#print(ticks)
			
			#pygame.display.flip()

			
   
			for entity in self.world.entities:
				if (isinstance(entity,Tank)) == True:
					if entity.gameOver == True:
						self.gameOver = True
						print('Save GAME')
						print(self.sec)
						print(self.minute)
						#self.draw_GameOver(self.zoom_surf)
				if entity is self.world.player:
					#print(self.name2)
					self.draw_gui(self.zoom_surf,entity)
					
			#self.draw_text(self.zoom_surf,"EXP : " +str(self.world.player.), (255,0,0), 70, 50, height/16+10)
			#self.draw_text(self.zoom_surf,str(self.world.player.level), (0,0,0), 70, 50, height/16+30)
			#self.draw_text(self.zoom_surf,"KILLS : "+str(self.world.player.level), (255,0,0), 70, 50, height/16+50)
			#print(str(self.kill))
			######################################3333
			screen.blit(self.zoom_surf, (0, 0))
			
		elif self.levelUp == True and self.paused == False and self.main_menu == False:
			for entity in self.world.entities:
				if entity is self.world.player:
					self.draw_levelUp(screen,self.sample_list)
					print(self.sample_list)

					#self.timeStop = True

		
			#self.timeStop = True
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
			if len(self.textinput.value) > 1:
				print(len(self.textinput.value))
				self.name2 = self.textinput.value
				print(self.name2)
		if self.showBoard == True:
			self.draw_Board(screen)
			
			
		
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
  
	def levelUp_damage(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.damage_bonus *= 1.1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
  
	def levelUp_Exp(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.level +=1
				entity.expBonus *= 1.1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
  
	def levelUp_health(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_health +=1
				entity.max_health *= 1.1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
  
	def levelUp_Shield(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_Shield  +=1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
  
	def levelUp_Plane(self):
		for entity in self.world.entities:
			if entity is self.world.player:
				entity.max_Shield  +=1
		self.stopEnd = time.time()
		self.toDelTime += abs(self.stopEnd - self.stopStart)
		self.timeStop = False
		self.levelUp = False
  
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
				#print(self.name2)
				self.draw_gui(self.zoom_surf,entity)
	    	
		screen.blit(self.zoom_surf, (0, 0))
		
		for i in self.rain:
			i[1] +=8
			pygame.draw.rect(screen, (255,255,255), (i, (2, 18)))
			#pygame.draw.circle(screen,(255,255,255),i,7)
			if i[1] > 800:
				i[1] = random.randrange(-50,-5)
				i[0] = random.randrange(1280)
		screen.blit(level_bg, (150, 100))
		#pygame.draw.rect(screen,(0,0,0),(150,50,600,700))
		font=pygame.freetype.SysFont(None, 70)
		font.origin=True
			
		font.render_to(screen, (500, 170), 'Level Up',pygame.Color('green'))
		font=pygame.freetype.SysFont(None, 34)
		font.origin=True
		for entity in self.world.entities:
			if entity is self.world.player:
				for i in range(len(sample_list)):
					if sample_list[i] == 'Main':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Main Weapon",pygame.Color('white'))
						next = entity.controllers[0].main_idx[(entity.controllers[0].main_weapon)+1]
						new = entity.weapons[next].name
						new = re.sub("[\(\[].*?[\)\]]", "", new)
						font.render_to(screen, ((i*320)+220,300), new,pygame.Color('green'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_Maingun)
					if sample_list[i] == 'Second':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Second Weapon",pygame.Color('white'))
						next = entity.controllers[0].second_idx[(entity.controllers[0].second_weapon)+1]
						new = entity.weapons[next].name
						new = re.sub("[\(\[].*?[\)\]]", "", new)
						font.render_to(screen, ((i*320)+220,300), new,pygame.Color('green'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_Secondgun)
					if sample_list[i] == 'Damage':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Damage",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_damage)
					if sample_list[i] == 'Bonus':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Exp Bonus",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_Exp)
					if sample_list[i] == 'Health':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Health",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_health)
					if sample_list[i] == 'Plane':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Bomber Plane",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_Plane)
					if sample_list[i] == 'Shield':
						pygame.draw.rect(screen,(0,0,0),((i*320)+200,200,250,400))
						font.render_to(screen, ((i*320)+220,250), "Eletric Shield",pygame.Color('white'))
						self.button(screen,"Upgrade",(i*320)+225,500,200,80,(130,255,0),(255,0,0),self.levelUp_Shield)
	#========================= LEVEL ============================================================================
	def draw_CharacterInput(self,screen):
     
     
		#bg = pygame.image.load(config.name_bg)
		#bg = pygame.transform.scale(bg, (width,height))

		#screen.blit(bg, (0, 0))
  
		screen.fill((0,0,0))
		font=pygame.freetype.SysFont(None, 50)
		font.origin=True
		font.render_to(screen, (200,200), "Enter your name : ",pygame.Color('white'))

		
  
		font=pygame.freetype.SysFont(None, 70)
		font.origin=True
		screen.blit(self.textinput.surface, (670, 180))
		self.textinput.font_color = (0, 2, 170)
		self.button(screen,"LETS GO",700,580,200,90,(0,0,0),(255,0,0),self.save_name)
  
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
			print(name,show_dict[name])
			
  			

		font=pygame.freetype.SysFont(None, 34)
		font.origin=True
		font.render_to(screen, (550, 100), 'LeaderBoard',pygame.Color('Red'))

	def draw_pauseScreen(self,screen):
		self.button(screen,"RESUME",400,120,150,90,(255,255,0),(255,0,0),self.toggle_pause)
		self.button(screen,"QUIT",400,320,150,90,(255,255,0),(255,0,0),self.menu)
		#self.timeStop = True
	def draw_mainMenu(self, screen):
			bg = pygame.image.load(config.menu_bg)
			bg = pygame.transform.scale(bg, (width,height))

			screen.blit(bg, (0, 0))
			self.button(screen,"START A GAME",750,330,300,90,(0,0,0),(255,0,0),self.toggle_character)
			self.button(screen,"Leaderboard",750,440,300,90,(0,0,0),(255,0,0),self.toggle_board)
			self.button(screen,"OPTION",750,550,300,90,(0,0,0),(255,0,0))
			self.button(screen,"EXIT",750,660,300,90,(0,0,0),(255,0,0),sys.exit)
   
	def draw_GameOver(self,screen):
			screen.fill((0,0,0))
			self.button(screen,"Continue",400,400,200,90,(255,255,0),(255,0,0),self.record_score)

	def draw_boxก(self, screen, x, y, active, string):
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
		else:
			self.stopEnd = time.time()
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
		self.world.add_enemies()
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
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption(config.title)
	g = Game()
	clock = pygame.time.Clock()
	while True:
		clock.tick(144)
		g.update()		
		g.draw(screen)        
		pygame.display.flip()