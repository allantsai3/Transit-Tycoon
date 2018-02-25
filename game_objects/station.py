import pygame
from const import *
import controller
import random

class Station:
    
    def __init__(self, pos: (int, int), surface, name="New Station"):
        self.tracks = []  # "routeName": Track
        self.x = pos[0]
        self.y = pos[1]
        self.dimensions = (20, 10)
        self.sprite = pygame.Rect(self.x, self.y, *self.dimensions)
        self.surface = surface
        self.name = name
        self.color = BLUE

        # passenger info
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
        # text_surf = self.font.render("({},{})".format(self.x, self.y), True, (BLACK))
        # self.surface.blit(text_surf, (self.x, self.y + 10))

        # draws population of each station
        text_surf = self.font.render("Passenger: " + str(self.pop), True, BLACK)
        self.surface.blit(text_surf, (self.x, self.y + 15))

        # draw station names
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

        # color of passenger
        station_ratio = self.pop / TRAIN_CAPACITY
        if station_ratio <= 0.5:
            self.surface.blit(HAPPYIMG, [self.x - 30, self.y + 20])
        elif station_ratio > 0.5 and station_ratio <= 1:
            self.surface.blit(NEUTRALIMG, [self.x - 30, self.y + 20])
        elif station_ratio > 1:
            self.surface.blit(ANGRYIMG, [self.x - 30, self.y + 20])
