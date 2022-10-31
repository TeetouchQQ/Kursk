	
class Enemies:
	health = 20


class Player:
	health = 10000
	max_secondary_bullets = 8

menu_bg = 'bg\Menu_logo.png'
name_bg = 'bg\input.png'
level_bg = 'bg\level_bg.png'
map_bg = 'bg\map.png'
width, height = 1280, 800
zoom = 1.5
player_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_dark.png'
player_turrent = 'resize_asset\\TankRed_barrel.png'

sps = 1

basic_probs = 0.0
basic_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_Red.png'
basic_turrent = 'resize_asset\\TankRed_barrel.png'

mothership_probs = 0.0
mothership_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_bigRed.png'
mothership_turrent = 'resize_asset\\TankRed_barrel.png'

lighttank_probs = 0.0
lighttank_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_blue.png'
lighttank_turrent = 'resize_asset\\tankBlue_barrel1.png'


shotgun_probs = 0.0
shotgun_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_sand.png'
shotgun_turrent = 'resize_asset\\tankSand_barrel1.png'


beamer_probs = 0.0
beamer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
beamer_turrent= 'resize_asset\\tankGreen_barrel1.png'


healer_probs = 0.0
healer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
healer_turrent= 'resize_asset\\tankGreen_barrel1.png'

scanner_probs = 0.0
scanner_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green.png'
scanner_turrent= 'resize_asset\\tankGreen_barrel1.png'

bullet_im = 'resize_asset\shotThin.png'
shotgun_im = 'resize_asset\shotThin.png'
rocket_bullet = 'resize_asset\shotRed.png'
rocket_explosive = 'Asset_ALL\\PNG\Retina\\explosion3.png'
class EasyDifficulty:
	index = 0
	num_enemies = 1
	num_motherships = 1
	num_light_enemies =1
	num_shotgunner_enemies = 1
	num_beamer_enemies = 1
	num_healer_enemies = 1
	num_scanner_enemies = 1
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