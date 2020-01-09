from base import *
import random
import enum
from standard_language import *
import training_loops
import pygame

class Adventure(World):
    def __init__(self, element_list, params):
        World.__init__(self, element_list, params)
        animate = self.params[0] # Typically not during training_loops
        if animate:
            pygame.init()
            self.size = width, height = 320, 240
            self.green = 0, 255, 0
            self.screen = pygame.display.set_mode(self.size)
            
