from game_entity import GameEntity
from utils.math_utils import *
import game_state as gs
import pygame


class CameraController(GameEntity):

    def __init__(self):

        self.speed = 6.0
        self.target_pos = Vector2(0.0, 0.0)
        self.current_pos = Vector2(0.0, 0.0)
        self.clicked_this_frame = False

    def update(self, dt: float):

        self.current_pos = lerp(self.current_pos, self.target_pos, dt * self.speed)
        gs.camera_pos.set(self.current_pos)

    def late_render(self, screen: pygame.Surface):
        self.clicked_this_frame = False

    def upon_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked_this_frame = True
