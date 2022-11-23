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

BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))
CAR_PICTURE_RED = pygame.image.load(os.path.join("bilder", "auto_rot.png"))
CAR_PICTURE_RED = pygame.transform.scale(CAR_PICTURE_RED, (20, 40))
CAR_PICTURE_YELLOW = pygame.image.load(os.path.join("bilder", "auto_gelb.png"))
CAR_PICTURE_YELLOW = pygame.transform.scale(CAR_PICTURE_YELLOW, (20, 40))
CAR_PICTURE_BLUE = pygame.image.load(os.path.join("bilder", "auto_blau.png"))
CAR_PICTURE_BLUE = pygame.transform.scale(CAR_PICTURE_BLUE, (20, 40))

CAR_PICTURES = [CAR_PICTURE_RED, CAR_PICTURE_YELLOW, CAR_PICTURE_BLUE]

start1 = [width * 0.3, -50]
start2 = [width * 0.47, -50]
start3 = [width * 0.635, -50]
start4 = [width, height * 0.45]
start5 = [width * 0.67, height+50]
start6 = [width * 0.5, height+50]
start7 = [width * 0.34, height+50]
start8 = [-50, height * 0.51]


#start4 = [width / 2.05, -50]

frequency = 50
speed = 1


class Car():

  def __init__(self, rectangle, direction):
    self.rectangle = rectangle
    self.direction = direction
    if self.direction == 1:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 180)
    elif self.direction == 2:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 90)
    elif self.direction == 3:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 0)
    else:
      self.picture = pygame.transform.rotate(CAR_PICTURES[random.randrange(len(CAR_PICTURES))].copy(), 270)

  def move(self, amount):
    if self.direction == 1:
      self.rectangle.y += amount
    elif self.direction == 2:
      self.rectangle.x -= amount
    elif self.direction == 3:
      self.rectangle.y -= amount
    else:
      self.rectangle.x += amount


def draw_screen(objects):
  screen.fill(WHITE)
  screen.blit(BACKGROUND, (0,0))
  for o in objects:
    screen.blit(o.picture, (o.rectangle.x, o.rectangle.y))
  pygame.display.update()










def main():
  global speed, frequency
  running = True
  clock = pygame.time.Clock()

  objects = []

  counter = 0

  while running:

    clock.tick(FPS)

    if counter == 0:
      objects.append(Car(pygame.Rect(start1[0], start1[1], 200, 200), 1))
      objects.append(Car(pygame.Rect(start2[0], start2[1], 200, 200), 1))
      objects.append(Car(pygame.Rect(start3[0], start3[1], 200, 200), 1))
      objects.append(Car(pygame.Rect(start4[0], start4[1], 200, 200), 2))
      objects.append(Car(pygame.Rect(start5[0], start5[1], 200, 200), 3))
      objects.append(Car(pygame.Rect(start6[0], start6[1], 200, 200), 3))
      objects.append(Car(pygame.Rect(start7[0], start7[1], 200, 200), 3))
      objects.append(Car(pygame.Rect(start8[0], start8[1], 200, 200), 4))

    counter += 1



    for o in objects:
      o.move(speed)

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


    draw_screen(objects)

    if counter >= frequency:
      counter = 0

if __name__ == "__main__":
  main()
