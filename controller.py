import pygame
import game_objects
from const import *
from random import randint
from pygame.locals import *
from const import *

from game_objects.train import Train
from game_objects.station import Station
from game_objects.cloud import Cloud


class Controller():
    instance = None

    surface = None
    entities = []
    
    fpsClock = pygame.time.Clock()

    # on start
    currentMoney = INITIAL_AMOUNT
    deductRate = 1000
    timeUntilDeduct = 1000
    deductPeriod = 1800
    positive = None

    @staticmethod
    def initialize(surface):
        if Controller.instance:
            raise Exception("controller already initialized")
        Controller.surface = surface
        Controller.instance = Controller()

    @staticmethod
    def tick():
        Controller.handleExpense()
        for entity in Controller.entities:
            entity.tick()
            entity.draw()

        money_font = pygame.font.SysFont(None, 80)
        pos_surf = money_font.render("$"+str(Controller.currentMoney), True, (GREEN))
        neg_surf = money_font.render("$"+str(Controller.currentMoney), True, (RED))
        if Controller.currentMoney >= 0:
            Controller.surface.blit(pos_surf, (10, DISPLAY_HEIGHT - 60))
        else:
            Controller.surface.blit(neg_surf, (10, DISPLAY_HEIGHT - 60))
        
        rounded_fps = round(Controller.fpsClock.get_fps())
        text_surf = money_font.render("Wind: " + str(rounded_fps)+"km/hr", True, (BLACK))
        Controller.surface.blit(text_surf, (10, 10))

        #Legend ui
        legend_font = pygame.font.SysFont(None, 25)
        all_routes = set()
        for entity in Controller.entities:
            if type(entity) == Station:
                for route in entity.tracks:
                    all_routes.add(route)

        #randomized cloud generation
        if randint(0, 200) == 0:
            cloud1 = Cloud(Controller.surface)
            Controller.entities.append(cloud1)


        pygame.display.update()
        Controller.fpsClock.tick(FPS)

    @staticmethod
    def addMoney(delta):
        Controller.instance.currentMoney += delta

    @staticmethod
    def handleExpense():
        controller = Controller.instance
        if controller.timeUntilDeduct is 0:
            controller.currentMoney -= controller.deductRate
            controller.timeUntilDeduct = controller.deductPeriod
        else:
            controller.timeUntilDeduct -= 1

