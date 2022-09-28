import xdrlib
import pygame
from pygame.locals import QUIT
import math

# Initalizing everything
pygame.init()
pygame.display.set_caption('Top Down Tank Wars || Cloud Multiplayer')
screen = pygame.display.set_mode((600, 600))
from math import sin, cos

# Loading, converting and coloring the space around the tank_body and
# tank_turret images white.
tank_body = pygame.image.load(
    'Asset\imges\Tank\Tank.png'
).convert()
tank_body.set_colorkey((0, 0, 0))

tank_turret = pygame.image.load(
    'Asset\imges\Tank\Turret.png'
).convert()
tank_turret.set_colorkey((0, 0, 0))


class Tank(pygame.sprite.Sprite):
    def __init__(self, startingX, startingY, starting_angle, speed):
        super(Tank, self).__init__()
        self.x = startingX
        self.y = startingX
        self.angle = starting_angle
        self.speed = speed

    def up(self):
        
        self.x -= sin(math.radians(self.angle)) * self.speed
        self.y -= cos(math.radians(self.angle)) * self.speed
        return self.x , self.y

    def down(self):
        self.x += sin(math.radians(self.angle)) * self.speed
        self.y += cos(math.radians(self.angle)) * self.speed
        return  self.x , self.y 

    def left(self):
        self.angle = self.angle + self.speed
        return self.angle

    def right(self):
        self.angle = self.angle - self.speed
        return self.angle


running = True
x = 300
y = 300
angle = 0
speed = 0.05
tank = Tank(x, y, angle, speed)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Set 'key_pressed' to the key that is being currently pressed
    keys_pressed = pygame.key.get_pressed()

    # Forward and backward manuevers
    if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]):
        x,y = tank.up()

    if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]):
        x,y = tank.down()

    # Turning tank body
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]):
        angle = tank.left()

    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]):
        angle = tank.right()

    angle = round(angle)
    angle = angle % 360

    #print(angle)
    #print(x,y)
    screen.fill((255, 255, 255))

    # Rotating tank and rendering it
    tank_body_copy = pygame.transform.rotate(tank_body, angle)
    screen.blit(
        tank_body_copy,
        (x - int(tank_body_copy.get_width() / 2),
         y - int(tank_body_copy.get_height() / 2))
    )

    # Rotating turret and rendering it
    tank_turret_copy = pygame.transform.rotate(tank_turret, angle)
    screen.blit(
        tank_turret_copy,
        (x - (int(tank_turret_copy.get_width() / 2)),
         y - (int(tank_turret_copy.get_height() / 2)))
    )

    pygame.display.update()

# Quit pygame when main loop has finished
pygame.quit()