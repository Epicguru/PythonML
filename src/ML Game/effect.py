from sprite import Sprite
import pygame
from utils.math_utils import *


class Effect(Sprite):

    def __init__(self, image: pygame.Surface, position, duration):
        super().__init__(image, position=position)

        self.timer = 0
        self.duration = duration
        self.set_pivot(0.5, 0.5)
        self.velocity = Vector2(10, 25)

    def update(self, dt: float):

        self.position += self.velocity * dt

        self.timer += dt

        if self.timer > self.duration:
            self.remove()

        super().update(dt)
