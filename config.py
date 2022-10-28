	
class Enemies:
	health = 20


class Player:
	health = 999999
	max_secondary_bullets = 8

width, height = 900, 700


sps = 1
mothership_probs = 0.2
lighttank_probs = 0.2
shotgun_probs = 0.2
beamer_probs = 0.2
healer_probs = 0.2
scanner_probs = 0.2



class EasyDifficulty:
	index = 0
	num_enemies = 0
	num_motherships = 0
	num_light_enemies =3
	num_shotgunner_enemies = 0
	num_beamer_enemies = 3
	num_healer_enemies = 0
	num_scanner_enemies = 2
	speed_mod = 1



#num_enemies = 0
#num_motherships = 0
#num_light_enemies = 0
#num_shotgunner_enemies = 0
#num_beamer_enemies = 0
#num_healer_enemies = 0
#num_scanner_enemies = 0

mothership_spawn_cooldown = 180 // 100

title = 'KURSK'