import pygame
from math import sin, cos, pi, atan2, hypot
from const import *
import random
import controller

def dist(destination, origin):
    return hypot(destination[0] - origin[0], destination[1] - origin[1])

class Track:
    
    def __init__(self, start_station, end_station, breakpoints: (int, int), surface):
        self.breakpoints = breakpoints
        self.start_station = start_station
        self.end_station = end_station
        self.color = BLACK
        self.surface = surface
    
    def tick(self):
        pass
    
    def draw(self):
        # connect as following
        # start_station - breakpoint1 - breakpoint2 ...-beakpointN - end_station
        point_list = list(self.breakpoints)
        point_list.insert(0, (self.start_station.x, self.start_station.y))
        point_list.append((self.end_station.x, self.end_station.y))
        pygame.draw.lines(self.surface, self.color, False, point_list)

class Station:
    
    def __init__(self, pos: (int, int), surface, name="New Station"):
        self.tracks = [] # "routeName": Track
        self.x = pos[0]
        self.y = pos[1]
        self.dimensions = (20,10)
        self.sprite = pygame.Rect(self.x, self.y, *self.dimensions)
        self.surface = surface
        self.name = name
        self.color = BLUE

        #passenger info
        self.populate_rate = POP_RATE
        self.pop_countdown = 100
        self.pop = 0
        
        self.color = BLUE
        self.font = pygame.font.SysFont(None, 20)
        self.moneyMessage = ["dummy", -1]
        
    def addTrack(self, track):
        self.tracks.append(track)
    
    def send(self, train, track):
        train.travel_track(track)
    
    def receive(self, train):
        money_delta = train.train_pop * INCOME_RATE
        train.train_pop = 0
        self.pop = train.pickup(self.pop)
        controller.Controller.addMoney(money_delta)
        train.wait_time = FPS
        random_track = random.choice(self.tracks)
        self.send(train, random_track)
        if money_delta > 0:
            self.moneyMessage = [str(money_delta), 25]

    def draw(self):
        self.sprite.center = (self.x, self.y)
        
        pygame.draw.circle(self.surface, GRAY, (self.x, self.y), 28)
        pygame.draw.circle(self.surface, WHITE, (self.x, self.y), 13)
        pygame.draw.rect(self.surface, self.color, self.sprite)
        #text_surf = self.font.render("({},{})".format(self.x, self.y), True, (BLACK))
        #self.surface.blit(text_surf, (self.x, self.y + 10))

        #draws population of each station
        text_surf = self.font.render("Passenger: " + str(self.pop), True, BLACK)
        self.surface.blit(text_surf, (self.x, self.y + 15))

        #draw station names
        stationfont = pygame.font.SysFont(None, 30)
        text_surf = stationfont.render(self.name, True, BLACK)
        self.surface.blit(text_surf, (self.x - 60, self.y - 40))

        if self.moneyMessage[1] > 0:
            receive_font = pygame.font.Font(None, 25)
            receive_surf = receive_font.render("+" + self.moneyMessage[0], True, GREEN)
            self.surface.blit(receive_surf, (self.x + 10, self.y - 10))
            self.moneyMessage[1] -= 1

    
    def tick(self):
        self.pop_countdown -= self.populate_rate
        if self.pop_countdown <= 0:
            self.pop += 1
            self.pop_countdown = 100

        #color of passenger
        station_ratio = self.pop / TRAIN_CAPACITY
        if station_ratio <= 0.5:
            self.surface.blit(HAPPYIMG, [self.x-30, self.y+20])
        elif station_ratio >0.5 and station_ratio <= 1:
            self.surface.blit(NEUTRALIMG, [self.x-30, self.y+20])
        elif station_ratio > 1:
            self.surface.blit(ANGRYIMG, [self.x-30, self.y+20])

class Train(pygame.sprite.Sprite):
    
    def __init__(self, parked_station, surface):
        super().__init__()
        
        self.image = pygame.Surface((30, 10))
        self.image.fill(GREEN)
        
        self.destination = (0,0)
        self.wait_time = 0
        
        self.max_speed = 3
        self.min_speed = .5
        self.speed = 0
        self.accel = .1
        
        self.x, self.y = parked_station.x, parked_station.y
        self.dimensions = (30, 10)
        self.angle = 0
        self.sprite = pygame.Rect(self.x, self.y, *self.dimensions)
        self.surface = surface
        self.color = GREEN

        self.font = pygame.font.SysFont(None, 20)

        #passenger info
        self.max_capacity = TRAIN_CAPACITY
        self.train_pop = 0

    #sets the passenger count on each train object and returns leftover passengers if any
    def pickup(self, passenger):
        if passenger > self.max_capacity:
            self.train_pop = self.max_capacity
        else:
            self.train_pop = passenger
        return passenger-self.train_pop


    def travel_track(self, track):
        self.break_point_index = 0
        self.destination = (track.end_station.x, track.end_station.y) if len(track.breakpoints) == 0 else track.breakpoints[0]
        self.track = track
        
    
    def get_angle(self,destination):
        x_dist = destination[0] - self.x
        y_dist = destination[1] - self.y
        return atan2(-y_dist, x_dist) % (2 * pi)

    def project(self):
        # if (hypot(self.destination[0] - self.x, self.destination[1] - self.y) <= 3):
        #     return self.x, self.y
        return (round(self.x + (cos(self.angle) * self.speed), 2),
                round(self.y - (sin(self.angle) * self.speed), 2))
    
    def at(self, destination, within=3):
        return dist(destination, (self.x, self.y)) <= within
    
    def get_head_pos(self):
        x = self.x + self.dimensions[0]*sin(self.angle+pi/2)
        y = self.y + self.dimensions[0]*cos(self.angle+pi/2)
        return (x, y)

    def draw(self):
        pygame.draw.line(self.surface, self.color,
                         (self.x, self.y), self.get_head_pos(), self.dimensions[1])
        text_surf = self.font.render("speed: {}".format(self.speed), True, (BLACK))
        self.surface.blit(text_surf, (self.x, self.y + 25))
        text_surf = self.font.render("Passenger: {}/{}".format(self.train_pop, self.max_capacity), True, (BLACK))
        self.surface.blit(text_surf, (self.x, self.y + 40))
        
    def tick(self):
        ctrlr = controller.Controller.instance
        if self.wait_time >= 0:
            self.wait_time -= 1
            self.speed = 0
        # if approaching station, slow down
        elif self.at((self.track.end_station.x, self.track.end_station.y), 75):
            self.speed = self.speed - self.accel if self.speed > self.min_speed else self.min_speed
        # if leaving station, speed up
        else:
            self.speed = self.speed + self.accel if self.speed < self.max_speed else self.max_speed
        

        capacity_ratio = self.train_pop/self.max_capacity
        if capacity_ratio >= 0.9:
            self.color  = RED
        elif capacity_ratio >= 0.4 and capacity_ratio < 0.9:
            self.color = YELLOW
        elif capacity_ratio < 0.4:
            self.color = GREEN

        
        self.speed = round(self.speed, 2)
        
        self.angle = self.get_angle(self.destination)
        
        self.x, self.y = self.project()
        self.sprite.center = (self.x, self.y)
        # if reaches the destination
        if self.at(self.destination):
            self.break_point_index += 1
            # if is not at end station
            if not self.at((self.track.end_station.x, self.track.end_station.y)):
                # if out of bps, head to end station
                if self.break_point_index > len(self.track.breakpoints)-1:
                    self.destination = (self.track.end_station.x, self.track.end_station.y)
                else:
                    # else head to next bp
                    self.destination = self.track.breakpoints[self.break_point_index]
            else: # if at end station
                self.break_point_index = 0
                self.track.end_station.receive(self)

class Cloud():
    def __init__(self, surface):
        self.surface = surface
        self.y = random.randint(0, DISPLAY_HEIGHT)
        self.x = -600
        self.velocity = random.randint(1, 5)
        self.img = pygame.transform.scale(CLOUD, (random.randint(150,200), random.randint(50,100)))
        self.rect = self.img.get_rect()


    def draw(self):
        if(self.x >= DISPLAY_WIDTH):
            pass
        else:
            self.surface.blit(self.img, self.rect)

    def tick(self):
        self.rect.center = (self.x, self.y)
        self.x += self.velocity

