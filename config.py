	
class Enemies:
	health = 20


class Player:
	health = 150
	max_secondary_bullets = 8

menu_bg = 'bg\Menu_logo.png'
name_bg = 'bg\input.png'
level_bg = 'bg\level_bg.png'
map_bg = 'bg\map.png'
width, height = 1500, 800
zoom = 1.3

player_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_dark_outline.png'
player_turrent = 'resize_asset\\specialBarrel3_outline.png'
Shield_img = "resize_asset\\pngegg1.png"
sps = 1

health_folder = "C:\\Users\\Admin\\Desktop\\Kursk\\resize_asset\\Health\\"


Exp_desc = 'Increase exp gain 10%'
Dmg_desc = 'Damage increase 10%'
Health_desc = 'Max health increase 10%'

HIT_BULLET = "Asset_ALL\\PNG\\Retina\\explosion4.png"
Plane_im = "asset2\\PNG\\Retina\\towerDefense_tile271.png"
Plane_back = "asset2\\PNG\\Retina\\towerDefense_tile294.png"
bomb_explo = "Asset_ALL\\PNG\\Retina\\explosion4.png"


basic_probs = 0.1
basic_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_Red_outline.png'
basic_turrent = 'resize_asset\\TankRed_barrel.png'

mothership_probs = 0.05
mothership_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_bigRed_outline.png'
mothership_turrent = 'resize_asset\\TankRed_barrel.png'

lighttank_probs = 0.1
lighttank_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_blue_outline.png'
lighttank_turrent = 'resize_asset\\tankBlue_barrel2_outline.png'


shotgun_probs = 0.1
shotgun_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_sand_outline.png'
shotgun_turrent = 'resize_asset\\tankSand_barrel2_outline.png'


beamer_probs = 0.08
beamer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green_outline.png'
beamer_turrent= 'resize_asset\\tankGreen_barrel2_outline.png'


healer_probs = 0.08
healer_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green_outline.png'
healer_turrent= 'resize_asset\\tankGreen_barrel2_outline.png'

scanner_probs = 0.08
scanner_sprite = 'Asset_ALL\\PNG\\Retina\\tankBody_green_outline.png'
scanner_turrent= 'resize_asset\\tankGreen_barrel2_outline.png'

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

basicgun_logo = "logo\\rocketlauncher_Logo.png"
burstgun_logo = "logo\\burstgun_logo.png"
shotgun_logo = "logo\shotgun_Logo.png"
machinegun_logo ="logo\\Minigun_Logo.png"
sniper_logo = "logo\\rocketlauncher_Logo.png"
beamgun_logo = "logo\\rocketlauncher_Logo.png"
flamethrower_logo = "logo\\FlameThrower_Logo.png"
rocketlauncher_logo = "logo\\rocketlauncher_Logo.png"

plane_logo = "logo\\plane_Logo.png"
health_logo =  "logo\health_logo.png"
exp_logo = "logo\\exp_Logo.png"
damage_logo = "logo\\damage_Logo.png"
shield_logo = "logo\\shield_Logo.png"


#num_enemies = 0
#num_motherships = 0
#num_light_enemies = 0
#num_shotgunner_enemies = 0
#num_beamer_enemies = 0
#num_healer_enemies = 0
#num_scanner_enemies = 0

mothership_spawn_cooldown = 180 // 100

title = 'KURSK'