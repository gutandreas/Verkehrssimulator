import os.path
import random
import pygame

import signal_settings

pygame.init()

#Simulationsparameter
frequency = 100
max_speed = 1
distance = 15

time = 0
number_of_cars_left = 0

#Farben
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
FPS = 30

#Fenster
(width, height) = (1536, 864)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Verkehrssimulator")


#Bilder
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

#Groups und Listen
CARS = pygame.sprite.Group()
SIGNALS = pygame.sprite.Group()
SIGNALS_POS_1 = []
SIGNALS_POS_2 = []
SIGNALS_POS_3 = []
STOP_AREAS = pygame.sprite.Group()
TEXT_MESSAGES = []
TIMETABLE = []


#Textanzeigen
FONTSIZE = 20
font = pygame.font.Font(pygame.font.get_default_font(), FONTSIZE)
text_number_of_cars_in_screen = font.render('---', True, WHITE)
TEXT_MESSAGES.append(text_number_of_cars_in_screen)
text_max_speed_cars = text_number_of_cars_in_screen = font.render('---', True, WHITE)
TEXT_MESSAGES.append(text_max_speed_cars)
text_frequncy = font.render('---', True, WHITE)
TEXT_MESSAGES.append(text_frequncy)
text_time = text_number_of_cars_in_screen = font.render('---', True, WHITE)
TEXT_MESSAGES.append(text_time)
text_number_of_cars_left_screen = font.render('---', True, WHITE)
TEXT_MESSAGES.append(text_number_of_cars_left_screen)



class Signal(pygame.sprite.Sprite):
  def __init__(self, position, direction):
    pygame.sprite.Sprite.__init__(self)
    self.direction = direction

    SIGNALS.add(self)
    signal_distance = 100

    STOP_AREA_DIMENSION_DIRECTION_1_3 = (30, 5)
    STOP_AREA_DIMENSION_DIRECTION_2_4 = (5, 30)

    if position == 1:
      self.position = [width*0.318, height*0.465]
    elif position == 2:
      self.position = [width * 0.485, height * 0.465]
    elif position == 3:
      self.position = [width * 0.65, height * 0.465]

    if direction == 1:
      self.position = [self.position[0] - signal_distance*0.65, self.position[1] - signal_distance*0.8]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
      self.stop_area = StopArea((self.position[0] + 50, self.position[1] + 20), STOP_AREA_DIMENSION_DIRECTION_1_3)
    elif direction == 2:
      self.position = [self.position[0] + signal_distance*0.85, self.position[1] - signal_distance*0.5]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)
      self.stop_area = StopArea((self.position[0], self.position[1] + 40), STOP_AREA_DIMENSION_DIRECTION_2_4)
    elif direction == 3:
      self.position = [self.position[0] + signal_distance*0.85, self.position[1] + signal_distance*1]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
      self.stop_area = StopArea((self.position[0] - 50, self.position[1]), STOP_AREA_DIMENSION_DIRECTION_1_3)
    elif direction == 4:
      self.position = [self.position[0] - signal_distance*0.95, self.position[1] + signal_distance*1]
      self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)
      self.stop_area = StopArea((self.position[0] + 30, self.position[1] - 40), STOP_AREA_DIMENSION_DIRECTION_2_4)

    self.rect = self.picture.get_rect()
    self.rect.x = self.position[0]
    self.rect.y = self.position[1]

  def change_color(self, color):
    self.picture = SIGNAL_PICTURE_GREEN

    if self.direction == 1:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 180)
        STOP_AREAS.remove(self.stop_area)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
        STOP_AREAS.add(self.stop_area)
    elif self.direction == 2:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 90)
        STOP_AREAS.remove(self.stop_area)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)
        STOP_AREAS.add(self.stop_area)
    elif self.direction == 3:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 0)
        STOP_AREAS.remove(self.stop_area)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
        STOP_AREAS.add(self.stop_area)
    elif self.direction == 4:
      if color == "green":
        self.picture = SIGNAL_PICTURE_GREEN
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 270)
        STOP_AREAS.remove(self.stop_area)
      else:
        self.picture = SIGNAL_PICTURE_RED
        self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)
        STOP_AREAS.add(self.stop_area)

class StopArea(pygame.sprite.Sprite):

  def __init__(self, position, dimensions):
    pygame.sprite.Sprite.__init__(self)
    self.rect = pygame.Rect(position, dimensions)
    STOP_AREAS.add(self)
    pygame.draw.rect(screen, (255, 0, 0), self.rect) #draw for debugging



class Car(pygame.sprite.Sprite):

  def __init__(self, start):
    pygame.sprite.Sprite.__init__(self)
    self.distance = 0
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
    self.speed = max_speed

  def move(self):
    road_free = True
    signal_green = True

    collision_with = pygame.sprite.spritecollide(self, CARS, False)
    collision_with.remove(self)

    touches_stop_area = pygame.sprite.spritecollide(self, STOP_AREAS, False)
    if len(touches_stop_area) > 0:
      signal_green = False


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

    if self.speed < max_speed:
      self.speed += 0.2
    else:
      self.speed = max_speed

    if road_free and signal_green:
      if self.direction == 1:
        self.rect.y += self.speed
      elif self.direction == 2:
        self.rect.x -= self.speed
      elif self.direction == 3:
        self.rect.y -= self.speed
      else:
        self.rect.x += self.speed
      self.distance += self.speed
    else:
      self.speed = 0

    if check_if_left_screen(self):
      CARS.remove(self)
      global number_of_cars_left
      number_of_cars_left += 1

class Event_Green():
  def __init__(self, signal_group, direction, time):
    self.signal_group = signal_group
    self.direction = direction
    self.time = time


def check_if_left_screen(car):
    started = car.distance > 100
    top = car.rect.y < 0
    right = car.rect.x > width
    bottom = car.rect.y > height
    left = car.rect.x < 0
    return started and (top or right or bottom or left)

def draw_screen():
  screen.fill(WHITE)
  screen.blit(BACKGROUND, (0,0))
  for c in CARS:
    screen.blit(c.picture, (c.rect.x, c.rect.y))
  for s in SIGNALS:
    screen.blit(s.picture, (s.rect.x, s.rect.y))
  counter = 10
  for t in TEXT_MESSAGES:
    screen.blit(t, pygame.Rect(10, counter, 200, 30))
    counter += FONTSIZE + 10
  pygame.display.update()




def change_signal_to_green(signal_group, direction):

  signal = None

  if signal_group == 1:
    for i in range(1,5,1):
      if direction == i:
        for s in SIGNALS_POS_1:
          s.change_color("red")
        signal = SIGNALS_POS_1[i-1]
  elif signal_group == 2:
    for i in range(1,5,1):
      if direction == i:
        for s in SIGNALS_POS_2:
          s.change_color("red")
        signal = SIGNALS_POS_2[i-1]
  else:
    for i in range(1,5,1):
      if direction == i:
        for s in SIGNALS_POS_3:
          s.change_color("red")
        signal = SIGNALS_POS_3[i-1]

  signal.change_color("green")












def main():
  global max_speed, frequency, time
  running = True
  clock = pygame.time.Clock()
  events = signal_settings.Settings.events

  for e in events:
    TIMETABLE.append(e)

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
    global SPRITES, text_number_of_cars_in_screen, text_max_speed_cars
    TEXT_MESSAGES[0] = font.render('Anzahl Fahrzeuge im Bild: ' + str(len(CARS)), True, WHITE)
    TEXT_MESSAGES[1] = font.render('Maximalgeschwindigkeit Fahrzeuge: ' + str(max_speed), True, WHITE)
    TEXT_MESSAGES[2] = font.render('Dauer zwischen Autos: ' + str((int(frequency/0.06))) + " ms", True, WHITE)
    TEXT_MESSAGES[3] = font.render('Simulationsdauer: ' + str(int(time/60)) + ":" + str(time%60), True, WHITE)
    TEXT_MESSAGES[4] = font.render('Anzahl Fahrzeuge ausser Bild: ' + str(number_of_cars_left), True, WHITE)

    if counter % frequency == 0:
      for i in range(1,9,1):
        Car(i)


    for e in TIMETABLE:
      if counter == e.time:
        change_signal_to_green(e.signal_group, e.direction)


    if counter%FPS == 0 and counter != 0:
      time += 1

    counter += 1


    for c in CARS:
      c.move()

    for event in pygame.event.get():

      keys_pressed = pygame.key.get_pressed()

      if keys_pressed[pygame.K_DOWN] and frequency <= 200:
        frequency += 3
        print("frequency", frequency)

      if keys_pressed[pygame.K_UP] and frequency >= 60:
        frequency -= 3
        print("frequency", frequency)

      if keys_pressed[pygame.K_RIGHT] and max_speed <= 3:
        max_speed += 1
        print("speed", max_speed)

      if keys_pressed[pygame.K_LEFT] and max_speed >= 2:
        max_speed -= 1
        print("speed", max_speed)

      if event.type == pygame.QUIT:
        running = False


    draw_screen()

    if counter >= 500:
      counter = 0

if __name__ == "__main__":
  main()
