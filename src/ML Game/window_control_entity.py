import pygame
from game_entity import GameEntity
import game_state as gs
from sprite import Sprite
import random

class WindowControlEntity(GameEntity):

    def update(self, dt: float):

        pass

    def upon_event(self, event: pygame.event):

        if event.type == pygame.QUIT:
            gs.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("s"):
                spr = Sprite(pygame.image.load("Test.png"), position=(random.randrange(0, 500), random.randrange(0, 300)))

