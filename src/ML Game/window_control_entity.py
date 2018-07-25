import pygame
from game_entity import GameEntity
from sprite import Sprite
import random
from utils.asset_loader import load_image
import game_state as gs
from utils.math_utils import *
from agents import *


class WindowControlEntity(GameEntity):

    def create(self):

        for i in range(100):
            x = random.randrange(0, 19) * 64
            y = random.randrange(0, 19) * 64

            spr = Sprite(load_image("Test.png"), position=Vector2(x, y))
            spr.set_pivot(0.5, 0.5)

    def upon_event(self, event: pygame.event):

        if event.type == pygame.QUIT:
            gs.running = False

