import getpass
import json
from datetime import datetime
import os.path
import random
import pygame
import os
import requests
import signal_settings

pygame.init()

# Simulationsparameter
frequency = 100
frequency_as_level = 60
max_speed = 4
distance = 15
report_interval = 50
next_report = 0
server_ip = "217.160.10.113:1001"

time = 0
number_of_cars_left = 0
running = True
debug = False
file = None

# Farben
WHITE = (255, 255, 255)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
GREEN_YELLOW = (190, 255, 110)
GREY = (230, 230, 230)
FPS = 30

# Fenster
(width, height) = (1536, 864)
screen = pygame.display.set_mode((width, height))
pygame.display.flip()
pygame.display.set_caption("Verkehrssimulator")

# Bilder
CAR_DIMENSIONS = (20, 35)
SIGNAL_DIMENSIONS = (30, 60)

BACKGROUND = pygame.image.load(os.path.join("bilder", "background2.png"))
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
CAR_PICTURE_PURPLE = pygame.image.load(os.path.join("bilder", "auto_violett.png"))
CAR_PICTURE_PURPLE = pygame.transform.scale(CAR_PICTURE_PURPLE, CAR_DIMENSIONS)
CAR_PICTURE_ORANGE = pygame.image.load(os.path.join("bilder", "auto_orange.png"))
CAR_PICTURE_ORANGE = pygame.transform.scale(CAR_PICTURE_ORANGE, CAR_DIMENSIONS)
CAR_PICTURE_LEMON = pygame.image.load(os.path.join("bilder", "auto_limone.png"))
CAR_PICTURE_LEMON = pygame.transform.scale(CAR_PICTURE_LEMON, CAR_DIMENSIONS)

CAR_PICTURES = [CAR_PICTURE_RED, CAR_PICTURE_YELLOW, CAR_PICTURE_BLUE, CAR_PICTURE_GREEN, CAR_PICTURE_CYAN,
                CAR_PICTURE_PURPLE, CAR_PICTURE_ORANGE, CAR_PICTURE_LEMON]

SIGNAL_PICTURE_RED = pygame.image.load(os.path.join("bilder", "ampel_rot.png"))
SIGNAL_PICTURE_RED = pygame.transform.scale(SIGNAL_PICTURE_RED, SIGNAL_DIMENSIONS)

SIGNAL_PICTURE_GREEN = pygame.image.load(os.path.join("bilder", "ampel_gruen.png"))
SIGNAL_PICTURE_GREEN = pygame.transform.scale(SIGNAL_PICTURE_GREEN, SIGNAL_DIMENSIONS)

# Groups und Listen
CARS = pygame.sprite.Group()
SIGNALS = pygame.sprite.Group()
SIGNALS_POS_1 = []
SIGNALS_POS_2 = []
SIGNALS_POS_3 = []
STOP_AREAS = pygame.sprite.Group()
TURN_AREAS = pygame.sprite.Group()
TEXT_MESSAGES_TITLE = []
TEXT_MESSAGES_VALUES = []
TEXT_MESSAGES_HINTS = []
TIMETABLE = []
STARTPOINTS = [[width * 0.31, -50], [width * 0.475, -50], [width * 0.64, -50], [width, height * 0.47],
               [width * 0.68, height + 50], [width * 0.515, height + 50], [width * 0.345, height + 50],
               [-50, height * 0.53]]

# Textanzeigen
FONTSIZE = 20
font = pygame.font.SysFont('arial black', FONTSIZE)

titles = ["Fahrzeuge im Bild:", "Durchgefahrene Fahrzeuge:", "Maximalgeschwindigkeit:", "Level Fahrzeughäufigkeit:",
          "Simulationsdauer:", "Zeitpunkt in Timeline:"]
for i in range(6):
    text_message_title = font.render(titles[i], True, GREY)
    TEXT_MESSAGES_TITLE.append(text_message_title)
    text_message_value = font.render('---', True, GREY)
    TEXT_MESSAGES_VALUES.append(text_message_value)

hints = ["Fahrzeughäufigkeit ändern: ↑/↓", "Maximalgeschwindigkeiten ändern: ←/→", "Hintergründe: 1/2/3", "Autos: d/f"]

for i in range(4):
    text_message_hint = font.render(hints[i], True, GREEN_YELLOW)
    TEXT_MESSAGES_HINTS.append(text_message_hint)


class Signal(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.position = position

        SIGNALS.add(self)
        signal_distance = 100

        STOP_AREA_DIMENSION_DIRECTION_1_3 = (30, 3)
        STOP_AREA_DIMENSION_DIRECTION_2_4 = (3, 30)

        TURN_AREA_DIMENSION = (5, 5)

        if position == 1:
            self.position_coordinates = [width * 0.318, height * 0.465]
        elif position == 2:
            self.position_coordinates = [width * 0.485, height * 0.465]
        elif position == 3:
            self.position_coordinates = [width * 0.65, height * 0.465]

        if direction == 1:
            self.position_coordinates = [self.position_coordinates[0] - signal_distance * 0.65,
                                         self.position_coordinates[1] - signal_distance * 0.8]
            self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
            self.stop_area = StopArea((self.position_coordinates[0] + 50, self.position_coordinates[1] + 20),
                                      STOP_AREA_DIMENSION_DIRECTION_1_3)
            self.turn_area1 = TurnArea((self.position_coordinates[0] + 60, self.position_coordinates[1] + 93),
                                       TURN_AREA_DIMENSION, self)
            self.turn_area2 = TurnArea((self.position_coordinates[0] + 60, self.position_coordinates[1] + 150),
                                       TURN_AREA_DIMENSION, self)
        elif direction == 2:
            self.position_coordinates = [self.position_coordinates[0] + signal_distance * 0.85,
                                         self.position_coordinates[1] - signal_distance * 0.5]
            self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)
            self.stop_area = StopArea((self.position_coordinates[0] + 20, self.position_coordinates[1] + 40),
                                      STOP_AREA_DIMENSION_DIRECTION_2_4)
            self.turn_area1 = TurnArea((self.position_coordinates[0] - 40, self.position_coordinates[1] + 60),
                                       TURN_AREA_DIMENSION, self)
            self.turn_area2 = TurnArea((self.position_coordinates[0] - 95, self.position_coordinates[1] + 60),
                                       TURN_AREA_DIMENSION, self)
        elif direction == 3:
            self.position_coordinates = [self.position_coordinates[0] + signal_distance * 0.85,
                                         self.position_coordinates[1] + signal_distance * 1]
            self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
            self.stop_area = StopArea((self.position_coordinates[0] - 50, self.position_coordinates[1] + 20),
                                      STOP_AREA_DIMENSION_DIRECTION_1_3)
            self.turn_area1 = TurnArea((self.position_coordinates[0] - 35, self.position_coordinates[1] - 40),
                                       TURN_AREA_DIMENSION, self)
            self.turn_area2 = TurnArea((self.position_coordinates[0] - 35, self.position_coordinates[1] - 80),
                                       TURN_AREA_DIMENSION, self)
        elif direction == 4:
            self.position_coordinates = [self.position_coordinates[0] - signal_distance * 0.95,
                                         self.position_coordinates[1] + signal_distance * 1]
            self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)
            self.stop_area = StopArea((self.position_coordinates[0] + 30, self.position_coordinates[1] - 40),
                                      STOP_AREA_DIMENSION_DIRECTION_2_4)
            self.turn_area1 = TurnArea((self.position_coordinates[0] + 90, self.position_coordinates[1] - 35),
                                       TURN_AREA_DIMENSION, self)
            self.turn_area2 = TurnArea((self.position_coordinates[0] + 145, self.position_coordinates[1] - 35),
                                       TURN_AREA_DIMENSION, self)

        self.rect = self.picture.get_rect()
        self.rect.x = self.position_coordinates[0]
        self.rect.y = self.position_coordinates[1]

    def change_color(self, color):
        self.picture = SIGNAL_PICTURE_GREEN

        if self.direction == 1:
            if color == "green":
                self.picture = SIGNAL_PICTURE_GREEN
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 180)
                STOP_AREAS.remove(self.stop_area)
                TURN_AREAS.add(self.turn_area1)
                TURN_AREAS.add(self.turn_area2)
            else:
                self.picture = SIGNAL_PICTURE_RED
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 180)
                STOP_AREAS.add(self.stop_area)
                TURN_AREAS.remove(self.turn_area1)
                TURN_AREAS.remove(self.turn_area2)
        elif self.direction == 2:
            if color == "green":
                self.picture = SIGNAL_PICTURE_GREEN
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 90)
                STOP_AREAS.remove(self.stop_area)
                TURN_AREAS.add(self.turn_area1)
                TURN_AREAS.add(self.turn_area2)
            else:
                self.picture = SIGNAL_PICTURE_RED
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 90)
                STOP_AREAS.add(self.stop_area)
                TURN_AREAS.remove(self.turn_area1)
                TURN_AREAS.remove(self.turn_area2)
        elif self.direction == 3:
            if color == "green":
                self.picture = SIGNAL_PICTURE_GREEN
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 0)
                STOP_AREAS.remove(self.stop_area)
                TURN_AREAS.add(self.turn_area1)
                TURN_AREAS.add(self.turn_area2)
            else:
                self.picture = SIGNAL_PICTURE_RED
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 0)
                STOP_AREAS.add(self.stop_area)
                TURN_AREAS.remove(self.turn_area1)
                TURN_AREAS.remove(self.turn_area2)
        elif self.direction == 4:
            if color == "green":
                self.picture = SIGNAL_PICTURE_GREEN
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_GREEN, 270)
                STOP_AREAS.remove(self.stop_area)
                TURN_AREAS.add(self.turn_area1)
                TURN_AREAS.add(self.turn_area2)
            else:
                self.picture = SIGNAL_PICTURE_RED
                self.picture = pygame.transform.rotate(SIGNAL_PICTURE_RED, 270)
                STOP_AREAS.add(self.stop_area)
                TURN_AREAS.remove(self.turn_area1)
                TURN_AREAS.remove(self.turn_area2)


class StopArea(pygame.sprite.Sprite):

    def __init__(self, position, dimensions):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(position, dimensions)
        STOP_AREAS.add(self)


class TurnArea(pygame.sprite.Sprite):

    def __init__(self, coordinates, dimensions, signal):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(coordinates, dimensions)
        TURN_AREAS.add(self)
        self.signal = signal


class Car(pygame.sprite.Sprite):

    def __init__(self, start):
        pygame.sprite.Sprite.__init__(self)
        self.distance = 0

        if start == 1:
            self.start = STARTPOINTS[0]
            self.direction = 1
        elif start == 2:
            self.start = STARTPOINTS[1]
            self.direction = 1
        elif start == 3:
            self.start = STARTPOINTS[2]
            self.direction = 1
        elif start == 4:
            self.start = STARTPOINTS[3]
            self.direction = 2
        elif start == 5:
            self.start = STARTPOINTS[4]
            self.direction = 3
        elif start == 6:
            self.start = STARTPOINTS[5]
            self.direction = 3
        elif start == 7:
            self.start = STARTPOINTS[6]
            self.direction = 3
        else:
            self.start = STARTPOINTS[7]
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
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
        CARS.add(self)
        self.speed = max_speed
        self.next_direction_random_number = random.randrange(3)

    def move(self):
        road_free = True
        signal_green = True

        collision_with = pygame.sprite.spritecollide(self, CARS, False)
        collision_with.remove(self)

        touches_stop_area = pygame.sprite.spritecollide(self, STOP_AREAS, False)
        if len(touches_stop_area) > 0:
            signal_green = False

        if len(collision_with) > 0:
            road_free = True
            if self.direction == 1:
                point_to_check = self.rect.midbottom
            elif self.direction == 2:
                point_to_check = self.rect.midleft
            elif self.direction == 3:
                point_to_check = self.rect.midtop
            else:
                point_to_check = self.rect.midright

            for c in collision_with:
                if c.rect.collidepoint(point_to_check):
                    road_free = False
                    break

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

        self.turn()

        if check_if_left_screen(self):
            self.kill()
            global number_of_cars_left
            number_of_cars_left += 1

    def turn(self):
        touches_turn_area = pygame.sprite.spritecollide(self, TURN_AREAS, False)

        start_coordinates = [[]]

        for a in touches_turn_area:
            if a.signal.direction == self.direction:
                if a == a.signal.turn_area1 and self.next_direction_random_number == 0:
                    # Ampel 1
                    if a.signal.position == 1:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[6][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[0][0]

                    # Ampel 2
                    if a.signal.position == 2:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[5][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[1][0]

                    # Ampel 3
                    if a.signal.position == 3:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[4][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[2][0]

                    self.direction = self.direction % 4 + 1
                    self.picture = pygame.transform.rotate(self.picture, 270)
                    self.rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.height, self.rect.width)
                    self.next_direction_random_number = random.randrange(3)

                if a == a.signal.turn_area2 and self.next_direction_random_number == 1:
                    # Ampel 1
                    if a.signal.position == 1:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[0][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[6][0]

                    # Ampel 2
                    if a.signal.position == 2:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[1][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[5][0]

                    # Ampel 3
                    if a.signal.position == 3:
                        if self.direction == 1:
                            self.rect.y = STARTPOINTS[7][1]
                        if self.direction == 2:
                            self.rect.x = STARTPOINTS[2][0]
                        if self.direction == 3:
                            self.rect.y = STARTPOINTS[3][1]
                        if self.direction == 4:
                            self.rect.x = STARTPOINTS[4][0]

                    self.direction = (self.direction - 1) % 4
                    self.picture = pygame.transform.rotate(self.picture, 90)
                    self.rect = self.picture.get_rect(topleft=self.rect.topleft)
                    self.next_direction_random_number = random.randrange(3)


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
    screen.blit(BACKGROUND, (0, 0))
    for c in CARS:
        screen.blit(c.picture, (c.rect.x, c.rect.y))
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), c.rect)
    for s in SIGNALS:
        screen.blit(s.picture, (s.rect.x, s.rect.y))
    counter = 0
    for t in TEXT_MESSAGES_TITLE:
        screen.blit(t, pygame.Rect(10, counter, 200, 30))
        counter += FONTSIZE + 10
    counter = 0
    for t in TEXT_MESSAGES_VALUES:
        screen.blit(t, pygame.Rect(350, counter, 200, 30))
        counter += FONTSIZE + 10
    counter = 0
    for t in TEXT_MESSAGES_HINTS:
        screen.blit(t, pygame.Rect(1090, counter, 200, 30))
        counter += FONTSIZE + 10

    if debug:
        for t in TURN_AREAS:
            pygame.draw.rect(screen, (255, 0, 0), t)
        for s in STOP_AREAS:
            pygame.draw.rect(screen, (255, 255, 255), s)
    pygame.display.update()


def change_signal_to_green(signal_group, direction):
    signal = None

    if signal_group == 1:
        for i in range(1, 5, 1):
            if direction == i:
                for s in SIGNALS_POS_1:
                    s.change_color("red")
                signal = SIGNALS_POS_1[i - 1]
    elif signal_group == 2:
        for i in range(1, 5, 1):
            if direction == i:
                for s in SIGNALS_POS_2:
                    s.change_color("red")
                signal = SIGNALS_POS_2[i - 1]
    else:
        for i in range(1, 5, 1):
            if direction == i:
                for s in SIGNALS_POS_3:
                    s.change_color("red")
                signal = SIGNALS_POS_3[i - 1]

    signal.change_color("green")


def check_key_events():
    global frequency, frequency_as_level, max_speed, running, debug, BACKGROUND

    for event in pygame.event.get():

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_DOWN] and frequency <= 200:
            frequency += 3
            frequency_as_level -= 1
            print("frequency", frequency)

        if keys_pressed[pygame.K_UP] and frequency >= 60:
            frequency -= 3
            frequency_as_level += 1
            print("frequency", frequency)

        if keys_pressed[pygame.K_RIGHT] and max_speed <= 3:
            max_speed += 1
            print("speed", max_speed)

        if keys_pressed[pygame.K_LEFT] and max_speed >= 2:
            max_speed -= 1
            print("speed", max_speed)

        if keys_pressed[pygame.K_d]:
            debug = True

        if keys_pressed[pygame.K_f]:
            debug = False

        if keys_pressed[pygame.K_1]:
            BACKGROUND = pygame.image.load(os.path.join("bilder", "background3.png"))
            BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))

        if keys_pressed[pygame.K_2]:
            BACKGROUND = pygame.image.load(os.path.join("bilder", "background.png"))
            BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))

        if keys_pressed[pygame.K_3]:
            BACKGROUND = pygame.image.load(os.path.join("bilder", "background2.png"))
            BACKGROUND = pygame.transform.scale(BACKGROUND, (width, height))

        if event.type == pygame.QUIT:
            running = False


def save_report():
    try:
        file = open("report.txt", "a")
        file.write(str(next_report) + " Autos zum Zeitpunkt "
                   + str(int(time / 60)) + ":" + str("{:02d}".format(time % 60))
                   + " mit Maximalgeschwindigkeit " + str(max_speed * 20)
                   + " und Häufigkeit " + str(frequency_as_level) + "\n")
        file.close()
        print("Report wurde gespeichert.")
    except Exception as e:
        print("Report konnte nicht gespeichert werden.")


def send_http_request():
    global file

    try:
        url = "http://" + server_ip + "/ranking"
        user = str(getpass.getuser())
        data = {'name': user, 'cars': str(next_report), 'time': str(time)}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post(url, data=json.dumps(data), headers=headers)
        print("Report wurde an Server geschickt.")
    except Exception as e:
        print("Report konnte nicht an Server geschickt werden.")


def main():
    global time, file, next_report
    clock = pygame.time.Clock()
    events = signal_settings.Settings.events

    for e in events:
        TIMETABLE.append(e)

    for j in range(1, 5, 1):
        s = Signal(1, j)
        SIGNALS_POS_1.append(s)

    for j in range(1, 5, 1):
        s = Signal(2, j)
        SIGNALS_POS_2.append(s)

    for j in range(1, 5, 1):
        s = Signal(3, j)
        SIGNALS_POS_3.append(s)

    counter = 0
    next_report = report_interval
    duration = signal_settings.Settings.duration
    file = open("report.txt", "w")
    file.write("Report zur Simulation von " + str(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
               + " des Users " + str(os.environ.get('USER')) + "\n")
    file.close()

    while running:

        clock.tick(FPS)
        global SPRITES, text_number_of_cars_in_screen, text_max_speed_cars
        TEXT_MESSAGES_VALUES[0] = font.render(str(len(CARS)), True, GREY)
        TEXT_MESSAGES_VALUES[1] = font.render(str(number_of_cars_left), True, GREY)
        TEXT_MESSAGES_VALUES[2] = font.render(str(max_speed * 20), True, GREY)
        TEXT_MESSAGES_VALUES[3] = font.render(str(frequency_as_level), True, GREY)
        TEXT_MESSAGES_VALUES[4] = font.render(str(int(time / 60)) + ":" + str("{:02d}".format(time % 60)), True, GREY)
        TEXT_MESSAGES_VALUES[5] = font.render(str(counter), True, GREY)

        if counter % frequency == 0:
            for i in range(1, 9, 1):
                Car(i)

        for e in TIMETABLE:
            if counter == e.time:
                change_signal_to_green(e.signal_group, e.direction)

        if counter % FPS == 0 and counter != 0:
            time += 1

        counter += 1

        for c in CARS:
            c.move()

        if number_of_cars_left >= next_report:
            save_report()
            send_http_request()
            next_report += report_interval

        check_key_events()
        draw_screen()

        if counter >= duration:
            counter = 0


if __name__ == "__main__":
    main()
