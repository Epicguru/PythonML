import game_entity
import pygame
import game_state as gs
import utils.math_utils
from utils.math_utils import *


class Sprite(game_entity.GameEntity):

    def __init__(self, image: pygame.Surface, position: Vector2 = Vector2(0.0, 0.0)):

        self.enabled = True
        self.image = None
        self.image_dim = (0, 0)
        self.pivot = (0, 0)
        self.bounds = pygame.Rect(0, 0, 0, 0)
        self.set_image(image)

        if position is not None:
            self.position = Vector2(position.get_x(), position.get_y())
        else:
            self.position = Vector2(0, 0)

        # Add to entities automatically.
        gs.register_entity(self)

        pass

    def get_pivot(self):
        return self.pivot

    def set_pivot(self, x: float, y: float):
        self.pivot = (clamp(x, 0, 1), clamp(y, 0, 1))

    def get_bounds(self) -> pygame.Rect:
        return self.bounds

    def set_image(self, image: pygame.Surface):
        self.image = image

        if image is None:
            self.image_dim = (0, 0)
            self.bounds.center = (0, 0)
            self.bounds.size = (0, 0)
        else:
            self.image_dim = (self.image.get_width(), self.image.get_height())
            self.bounds.center = (self.pivot[0], self.pivot[1])
            self.bounds.size = (self.image_dim[0], self.image_dim[1])

    def set_position(self, pos: Vector2):
        self.position.set(pos)

    def get_image_dimensions(self):
        return self.image_dim

    def update(self, dt: float):

        self.bounds.center = (self.position.get_x() + self.pivot[0], self.position.get_y() + self.pivot[1])

    def render(self, screen: pygame.Surface):

        if self.image is None:
            return
        if not self.enabled:
            return

        x = (self.position.get_x() -
             gs.camera_pos.get_x() + gs.resolution[0] * 0.5 -
             self.get_image_dimensions()[0] * self.get_pivot()[0])

        y = (-self.position.get_y() -
             self.get_image_dimensions()[1] + gs.camera_pos.get_y()
             + gs.resolution[1] * 0.5 +
             self.get_image_dimensions()[1] * self.get_pivot()[1])

        if x > gs.resolution[0]:
            return
        if y > gs.resolution[1]:
            return
        if x + self.get_image_dimensions()[0] < 0:
            return
        if y + self.get_image_dimensions()[1] < 0:
            return

        screen.blit(self.image, (x, y))

        pass
