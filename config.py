	
class Enemies:
	health = 20


class Player:
	health = 999999
	max_secondary_bullets = 8

width, height = 1080, 920
zoom = 1.5
player_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_dark.png'
player_turrent = 'Asset_ALL\\PNG\\Retina\\tankRed_barrel1.png'

sps = 1

basic_probs = 0.1
basic_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_Red.png'
basic_turrent = 'Asset_ALL\\PNG\\Retina\\tankRed_barrel2.png'

mothership_probs = 0.1
mothership_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_bigRed.png'
mothership_turrent = 'Asset_ALL\\PNG\\Retina\\tankRed_barrel1_outline.png'

lighttank_probs = 0.1
lighttank_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_blue.png'
lighttank_turrent = 'Asset_ALL\\PNG\\Retina\\tankBlue_barrel1.png'


shotgun_probs = 0.1
shotgun_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_sand.png'
shotgun_turrent = 'Asset_ALL\\PNG\\Retina\\tankSand_barrel1.png'


beamer_probs = 0.1
beamer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
beamer_turrent= 'Asset_ALL\\PNG\\Retina\\tankGreen_barrel1.png'


healer_probs = 0.1
healer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
healer_turrent= 'Asset_ALL\\PNG\\Retina\\tankGreen_barrel1.png'

scanner_probs = 0.1
scanner_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
scanner_turrent= 'Asset_ALL\\PNG\\Retina\\tankGreen_barrel1.png'


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