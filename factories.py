from tank import Tank
import controllers
import config
import weapons
from health_pack import HealthPack
from projectile import GuidedMissile

def create_basic_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(), 
		controllers.BasicTargetingController(),
		controllers.EnemyDieController()
	],Tanktype='basic')

def create_mothership(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.4), 
		controllers.SpawnEnemyController(),
		controllers.EnemyDieController()
	], max_health=80, high_colour=(0, 255, 0), low_colour=(0, 100, 100), size=50, collision_radius=25,Tanktype='mothership')

def create_light_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=2),
		controllers.LightTargetingController(),
		controllers.EnemyDieController()
	], max_health=15, high_colour=(255, 255, 0), low_colour=(0, 100, 0), size=15, collision_radius=14,Tanktype='lightTank')

def create_shotgunner_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.PlayerHunterController(speed=2),
		controllers.ShotgunTargetingController(),
		controllers.EnemyDieController()
	], max_health=40, high_colour=(153, 204, 255), low_colour=(100, 100, 0), size=30, collision_radius=20,Tanktype='shotgunner')

def create_scanner_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.EnemyScannerController(),
		controllers.EnemyDieController()
	], max_health=60, high_colour=(0, 255, 200), low_colour=(0, 100, 0), size=50, collision_radius=25,Tanktype='scanner')

def create_beamer_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.PlayerHunterController(speed=2, sight_range=400, sprint=2.5),
		controllers.BeamTargetingController(),
		controllers.EnemyDieController()
	], max_health=45, high_colour=(121, 45, 216), low_colour=(102, 21, 86), size=30, collision_radius=20,Tanktype='beamer')


def create_player(position, loadout):
	all_weapons = [
		weapons.BasicGun(), #Main 0 
		weapons.BurstGun(),	#Second 1
		weapons.Shotgun(),	#Main 2
		weapons.MachineGun(),	#Second 3
		weapons.SniperRifle(),  #Main 4
		weapons.BeamGun(),		#Second 5 
		weapons.Flamethrower(),	#Second 6
		weapons.RocketLauncher(), #Main 7
		weapons.MissileBarrage(),	#Main 8
		weapons.GuidedMissileLauncher() #Main 9
	]
	count = 0
	chosen_weapons = []
	for i in range(10):
		if loadout[i] and count < 10:
			chosen_weapons.append(all_weapons[i])
			count += 1

	return Tank(position, [
		controllers.PlayerController(speed=4.2),
	], max_health=config.Player.health, high_colour=(0, 0, 255), low_colour=(0, 0, 255), weapons=chosen_weapons, is_player=True, size=40, collision_radius=15)

def create_healer_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=2),
		controllers.EnemyHealerController(),
		controllers.EnemyDieController()
	], max_health=20, high_colour=(211, 150, 20), low_colour=(135, 63, 41), size=30, collision_radius=15)

def create_health_pack(position):
	return HealthPack(position)