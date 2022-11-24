import math
import os.path
import random

import pygame
import kivy
from kivy.uix.slider import Slider


WHITE = (255, 255, 255)
FPS = 30

(width, height) = (1536, 864)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Verkehrssimulator")

CAR_DIMENSIONS = (20, 35)
SIGNAL_DIMENSIONS = (30, 60)

BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))
CAR_PICTURE_RED = pygame.image.load(os.path.join("bilder", "auto_rot.png"))
CAR_PICTURE_RED = pygame.transform.scale(CAR_PICTURE_RED, CAR_DIMENSIONS)
CAR_PICTURE_YELLOW = pygame.image.load(os.path.join("bilder", "auto_gelb.png"))
CAR_PICTURE_YELLOW = pygame.transform.scale(CAR_PICTURE_YELLOW, CAR_DIMENSIONS)
CAR_PICTURE_BLUE = pygame.image.load(os.path.join("bilder", "auto_blau.png"))
CAR_PICTURE_BLUE = pygame.transform.scale(CAR_PICTURE_BLUE, CAR_DIMENSIONS)
CAR_PICTURE_CYAN = pygame.image.load(os.path.join("bilder", "auto_tuerkis.png"))
CAR_PICTURE_CYAN = pygame.transform.scale(CAR_PICTURE_CYAN, CAR_DIMENSIONS)
CAR_PICTURE_GREEN = pygame.image.load(os.path.join("bilder", "auto_gruen.png"))
CAR_PICTURE_GREEN = pygame.transform.scale(CAR_PICTURE_GREEN, CAR_DIMENSIONS)

CAR_PICTURES = [CAR_PICTURE_RED, CAR_PICTURE_YELLOW, CAR_PICTURE_BLUE, CAR_PICTURE_GREEN, CAR_PICTURE_CYAN]

SIGNAL = pygame.image.load(os.path.join("bilder", "ampel_rot.png"))
SIGNAL = pygame.transform.scale(SIGNAL, SIGNAL_DIMENSIONS)

CARS = pygame.sprite.Group()
SIGNALS = pygame.sprite.Group()

#start4 = [width / 2.05, -50]

frequency = 100
speed = 1
distance = 15

class Signal(pygame.sprite.Sprite):
  def __init__(self, position, direction):
    pygame.sprite.Sprite.__init__(self)

    SIGNALS.add(self)

    signal_distance = 100

    if position == 1:
      self.position = [width*0.317, height*0.465]
    elif position == 2:
      self.position = [width * 0.48, height * 0.465]
    elif position == 3:
      self.position = [width * 0.65, height * 0.465]

    if direction == 1:
      self.position = [self.position[0] - signal_distance*0.75, self.position[1] - signal_distance*0.9]
      self.picture = pygame.transform.rotate(SIGNAL, 180)
    elif direction == 2:
      self.position = [self.position[0] + signal_distance*0.8, self.position[1] - signal_distance*0.6]
      self.picture = pygame.transform.rotate(SIGNAL, 90)
    elif direction == 3:
      self.position = [self.position[0] + signal_distance*0.8, self.position[1] + signal_distance*0.95]
      self.picture = pygame.transform.rotate(SIGNAL, 0)
    elif direction == 4:
      self.position = [self.position[0] - signal_distance*1, self.position[1] + signal_distance*0.95]
      self.picture = pygame.transform.rotate(SIGNAL, 270)

    self.rect = self.picture.get_rect()
    self.rect.x = self.position[0]
    self.rect.y = self.position[1]



class Car(pygame.sprite.Sprite):

  def __init__(self, start):
    pygame.sprite.Sprite.__init__(self)
    if start == 1:
      start = [width * 0.3, -50]
      self.direction = 1
    elif start == 2:
      start = [width * 0.47, -50]
      self.direction = 1
    elif start == 3:
      start = [width * 0.635, -50]
      self.direction = 1
    elif start == 4:
      start = [width, height * 0.45]
      self.direction = 2
    elif start == 5:
      start = [width * 0.67, height + 50]
      self.direction = 3
    elif start == 6:
      start = [width * 0.5, height + 50]
      self.direction = 3
    elif start == 7:
      start = [width * 0.34, height + 50]
      self.direction = 3
    else:
      start = [-50, height * 0.51]
      self.direction = 4

    if self.direction == 1:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 180)
    elif self.direction == 2:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 90)
    elif self.direction == 3:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 0)
    else:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 270)

    self.rect = self.picture.get_rect()
    self.rect.x = start[0]
    self.rect.y = start[1]
    CARS.add(self)



  def move(self, amount):
    road_free = True

    collision_with = pygame.sprite.spritecollide(self, CARS, False)
    collision_with.remove(self)

    if len(collision_with) > 0:
      road_free = False
      if self.direction == 1:
        point_to_check = self.rect.midbottom
      elif self.direction == 2:
        point_to_check = self.rect.midleft
      elif self.direction == 3:
        point_to_check = self.rect.midtop
      else:
        point_to_check = self.rect.midright

      if not collision_with[0].rect.collidepoint(point_to_check):
        road_free = True

    if road_free:
      if self.direction == 1:
        self.rect.y += amount
      elif self.direction == 2:
        self.rect.x -= amount
      elif self.direction == 3:
        self.rect.y -= amount
      else:
        self.rect.x += amount


def draw_screen():
  screen.fill(WHITE)
  screen.blit(BACKGROUND, (0,0))
  for c in CARS:
    screen.blit(c.picture, (c.rect.x, c.rect.y))
  for s in SIGNALS:
    screen.blit(s.picture, (s.rect.x, s.rect.y))
  pygame.display.update()










def main():
  global speed, frequency
  running = True
  clock = pygame.time.Clock()

  for i in range(1,4,1):
    for j in range(1,5,1):
      Signal(i, j)

  counter = 0


  while running:

    clock.tick(FPS)

    if counter == 0:
      for i in range(1,9,1):
        Car(i)

    counter += 1

    for c in CARS:
      c.move(speed)

    for event in pygame.event.get():

      keys_pressed = pygame.key.get_pressed()

      if keys_pressed[pygame.K_UP]:
        frequency += 10
        print("frequency", frequency)

      if keys_pressed[pygame.K_DOWN]:
        frequency -= 10
        print("frequency", frequency)

      if keys_pressed[pygame.K_RIGHT]:
        speed += 1
        print("speed", speed)

      if event.type == pygame.QUIT:
        running = False


    draw_screen()

    if counter >= frequency:
      counter = 0

if __name__ == "__main__":
  main()
