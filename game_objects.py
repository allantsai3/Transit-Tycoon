import pygame
from math import sin, cos, pi, atan2, hypot
from const import *


class GameObject:
    pass


class Track(GameObject):
    
    def __init__(self, start_station, end_station, breakpoints: [(int, int)], surface):
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


class Station(GameObject):
    
    def __init__(self, pos: (int, int), surface):
        self.tracks = {} # "routeName": Track
        self.x = pos[0]
        self.y = pos[1]
        self.stationSize = 20
        self.surface = surface
    
    def addTrack(self, track, route):
        self.tracks[route] = track
    
    def send(self, train, track):
        train.travel_track(track)
    
    def receive(self, train):
        target_track = self.tracks[train.route]
        self.send(train, target_track)
    
    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 255), [self.x - (self.stationSize/2), self.y-(self.stationSize/2), self.stationSize, self.stationSize])

    
    def tick(self):
        pass
    

class Train(GameObject):
    
    def __init__(self, parked_station, route, surface):
        self.destination = (0,0)
        
        self.route = route
        self.speed = 5
        self.route = route
        self.x, self.y = parked_station.x, parked_station.y
        self.dimensions = (30, 10)
        self.angle = 0
        self.sprite = pygame.Rect(self.x, self.y, *self.dimensions)
        self.surface = surface
        self.color = GREEN

    def travel_track(self, track):
        self.i = 0
        self.destination = (track.end_station.x, track.end_station.y) if len(track.breakpoints) == 0 else track.breakpoints[0]
        self.track = track
        
    
    def get_angle(self,destination):
        x_dist = destination[0] - self.x
        y_dist = destination[1] - self.y
        return atan2(-y_dist, x_dist) % (2 * pi)

    def project(self):
        if (hypot(self.destination[0] - self.x, self.destination[1] - self.y) <= 3):
            return self.x, self.y
        return (round(self.x + (cos(self.angle) * self.speed)),
                round(self.y - (sin(self.angle) * self.speed)))
    
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.sprite)
        
    def tick(self):
        self.angle = self.get_angle(self.destination)
        self.x, self.y = self.project()
        self.sprite.center = (self.x, self.y)
        if hypot(self.destination[0] - self.x, self.destination[1] - self.y) <= 3:
            self.i += 1
            if (self.x, self.y) != (self.track.end_station.x, self.track.end_station.y):

                if self.i > len(self.track.breakpoints)-1: # if out of bps, head to end station
                    self.destination = (self.track.end_station.x, self.track.end_station.y)
                else:
                    # else head to next bp
                    self.destination = self.track.breakpoints[self.i]
            else:
                self.i = 0
                self.track.end_station.receive(self)