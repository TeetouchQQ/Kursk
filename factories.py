from tank import Tank
import controllers
import config
import weapons
from health_pack import HealthPack


def create_basic_enemy(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(), 
		controllers.BasicTargetingController(),
		controllers.EnemyDieController()
	],Tanktype='basic',max_health=(plevel/10)*20,damage_bonus = (plevel/20) + 1)

def create_mothership(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.4), 
		controllers.SpawnEnemyController(),
		controllers.EnemyDieController()
	], max_health=80, high_colour=(0, 255, 0), low_colour=(0, 100, 100), size=50, collision_radius=25,Tanktype='mothership'
            ,damage_bonus = (plevel/20) + 1)

def create_light_enemy(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(speed=2),
		controllers.LightTargetingController(),
		controllers.EnemyDieController()
	], max_health=15, high_colour=(255, 255, 0), low_colour=(0, 100, 0), size=15, collision_radius=14,Tanktype='lightTank'
             ,damage_bonus = (plevel/10) + 1)

def create_shotgunner_enemy(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.PlayerHunterController(speed=2),
		controllers.ShotgunTargetingController(),
		controllers.EnemyDieController()
	], max_health=40, high_colour=(153, 204, 255), low_colour=(100, 100, 0), size=30, collision_radius=20,Tanktype='shotgunner'
             ,damage_bonus = (plevel/10) + 1)

def create_scanner_enemy(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.EnemyScannerController(),
		controllers.EnemyDieController()
	], max_health=60, high_colour=(0, 255, 200), low_colour=(0, 100, 0), size=50, collision_radius=25,Tanktype='scanner'
             ,damage_bonus = (plevel/10) + 1)

def create_beamer_enemy(position,plevel):
	return Tank(position, [
		controllers.BounceMoveController(speed=0.5),
		controllers.PlayerHunterController(speed=2, sight_range=400, sprint=2.5),
		controllers.BeamTargetingController(),
		controllers.EnemyDieController()
	], max_health=45, high_colour=(121, 45, 216), low_colour=(102, 21, 86), size=30, collision_radius=20,Tanktype='beamer'
             ,damage_bonus = (plevel/10) + 1)


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
		
	]
	count = 0
	chosen_weapons = []
	for i in range(8):
		if loadout[i] and count < 8:
			chosen_weapons.append(all_weapons[i])
			count += 1

	return Tank(position, [
		controllers.PlayerController(speed=4.2),
		controllers.PlaneController(),
		controllers.ShieldController()
	], max_health=config.Player.health, high_colour=(0, 0, 255), low_colour=(0, 0, 255), weapons=chosen_weapons, is_player=True, size=40, collision_radius=15,
             bomb = weapons.PlaneBomber(),shield = weapons.ShieldCreater())

def create_healer_enemy(position):
	return Tank(position, [
		controllers.BounceMoveController(speed=2),
		controllers.EnemyHealerController(),
		controllers.EnemyDieController()
	], max_health=20, high_colour=(211, 150, 20), low_colour=(135, 63, 41), size=30, collision_radius=15)

def create_health_pack(position,health_power,exp_get,color):
	return HealthPack(position,controllers= [controllers.HealthController()],health_power=health_power,exp_get = exp_get,color = color)

def create_BOSS(position,plevel):
	return Tank(position, [
		#controllers.BounceMoveController(speed=2),
		
		controllers.EnemyScannerController(),
		controllers.PlayerHunterController(speed=1.5, sight_range=5000, sprint=1),
		controllers.BossSkillController(),
		controllers.EnemyDieController()
	], max_health=9000000,high_colour=(0, 255, 200), low_colour=(0, 100, 0), size=300, collision_radius=165,Tanktype='BOSS'
             ,damage_bonus = 10)