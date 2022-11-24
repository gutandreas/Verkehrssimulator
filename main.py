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

SIGNAL_PICTURE_RED = pygame.image.load(os.path.join("bilder", "ampel_rot.png"))
SIGNAL_PICTURE_RED = pygame.transform.scale(SIGNAL_PICTURE_RED, SIGNAL_DIMENSIONS)

SIGNAL_PICTURE_GREEN = pygame.image.load(os.path.join("bilder", "ampel_gruen.png"))
SIGNAL_PICTURE_GREEN = pygame.transform.scale(SIGNAL_PICTURE_GREEN, SIGNAL_DIMENSIONS)

CARS = pygame.sprite.Group()
SIGNALS = pygame.sprite.Group()
SIGNALS_POS_1 = []
SIGNALS_POS_2 = []
SIGNALS_POS_3 = []

#start4 = [width / 2.05, -50]

frequency = 100
speed = 1
distance = 15

class Signal(pygame.sprite.Sprite):
  def __init__(self, position, direction):
    pygame.sprite.Sprite.__init__(self)
    self.direction = direction

    SIGNALS.add(self)

    signal_distance = 100

    if position == 1:
      self.position = [width*0.318, height*0.465]
    elif position == 2:
      self.position = [width * 0.485, height * 0.465]
    elif position == 3:
      self.position = [width * 0.65, height * 0.465]

    if direction == 1:
      self.position = [self.position[0] - signal_distance*0.65, self.position[1] - signal_distance*0.8]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
    elif direction == 2:
      self.position = [self.position[0] + signal_distance*0.85, self.position[1] - signal_distance*0.5]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)
    elif direction == 3:
      self.position = [self.position[0] + signal_distance*0.85, self.position[1] + signal_distance*1]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
    elif direction == 4:
      self.position = [self.position[0] - signal_distance*0.95, self.position[1] + signal_distance*1]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)

    self.rect = self.picture.get_rect()
    self.rect.x = self.position[0]
    self.rect.y = self.position[1]

  def change_color(self, color):
    self.picture = SIGNAL_PICTURE_GREEN
    print("green")

    if self.direction == 1:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 180)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
    elif self.direction == 2:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 270)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)
    elif self.direction == 3:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 0)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
    elif self.direction == 4:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 90)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)


class Car(pygame.sprite.Sprite):

  def __init__(self, start):
    pygame.sprite.Sprite.__init__(self)
    if start == 1:
      start = [width * 0.31, -50]
      self.direction = 1
    elif start == 2:
      start = [width * 0.475, -50]
      self.direction = 1
    elif start == 3:
      start = [width * 0.64, -50]
      self.direction = 1
    elif start == 4:
      start = [width, height * 0.47]
      self.direction = 2
    elif start == 5:
      start = [width * 0.68, height + 50]
      self.direction = 3
    elif start == 6:
      start = [width * 0.515, height + 50]
      self.direction = 3
    elif start == 7:
      start = [width * 0.345, height + 50]
      self.direction = 3
    else:
      start = [-50, height * 0.53]
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


  for j in range(1,5,1):
    s = Signal(1, j)
    SIGNALS_POS_1.append(s)

  for j in range(1,5,1):
    s = Signal(2, j)
    SIGNALS_POS_2.append(s)

  for j in range(1,5,1):
    s = Signal(3, j)
    SIGNALS_POS_3.append(s)

  counter = 0


  while running:

    clock.tick(FPS)

    if counter == 0:
      global SPRITES
      print(len(CARS))
      for i in range(1,9,1):
        Car(i)

    if counter == 20:
      pos_1 = random.randrange(0,4)
      SIGNALS_POS_1[pos_1].change_color("green")
      pos_2 = random.randrange(0,4)
      SIGNALS_POS_2[pos_2].change_color("green")
      pos_3 = random.randrange(0, 4)
      SIGNALS_POS_3[pos_3].change_color("green")


    if counter == 30:
      SIGNALS_POS_1[pos_1].change_color("red")
      SIGNALS_POS_2[pos_2].change_color("red")
      SIGNALS_POS_3[pos_3].change_color("red")

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
