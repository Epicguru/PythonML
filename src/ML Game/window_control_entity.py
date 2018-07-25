import pygame
from game_entity import GameEntity
from sprite import Sprite
import random
from utils.asset_loader import load_image
import game_state as gs
from utils.math_utils import *


class WindowControlEntity(GameEntity):

    i = 0

    def update(self, dt: float):

        x = gs.camera_pos.get_x()
        y = gs.camera_pos.get_y()

        mp = pygame.mouse.get_pos()
        mx = mp[0]
        my = mp[1]

        center = (gs.resolution[0] / 2.0, gs.resolution[1] / 2.0)
        off_x = mx - center[0]
        off_x /= gs.resolution[0]

        off_y = my - center[1]
        off_y /= gs.resolution[1]

        gs.camera_pos.inc_x(dt * off_x * 1000.0)
        gs.camera_pos.dec_y(dt * off_y * 1000.0)

    def upon_event(self, event: pygame.event):

        if event.type == pygame.QUIT:
            gs.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("s"):
                spr = Sprite(load_image("Test.png"), position=Vector2(self.i * 64, self.i * 32))
                spr.set_pivot(0.5, 0.5)
                spr.set_position()
                self.i += 1

