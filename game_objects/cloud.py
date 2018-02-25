
from const import *
import random

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