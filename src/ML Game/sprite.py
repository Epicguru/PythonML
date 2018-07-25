import game_entity
import pygame
import game_state as gs
import utils.math_utils
from utils.math_utils import *


class Sprite(game_entity.GameEntity):

    image = None
    image_dim = (0, 0)
    pivot = (0, 0)

    def __init__(self, image: pygame.Surface, position: Vector2 = utils.math_utils.VECTOR_ZERO):

        self.set_image(image)

        if position is not None:
            self.position = Vector2(position.get_x(), position.get_y())
        else:
            self.position = utils.math_utils.VECTOR_ZERO

        # Add to entities automatically.
        gs.entities.append(self)

        pass

    def get_pivot(self):
        return self.pivot

    def set_pivot(self, x: float, y: float):
        self.pivot = (clamp(x, 0, 1), clamp(y, 0, 1))

    def set_image(self, image: pygame.Surface):
        self.image = image

        if image is None:
            self.image_dim = (0, 0)
        else:
            self.image_dim = (self.image.get_width(), self.image.get_height())

    def set_position(self, pos: Vector2):
        self.position.set(pos)

    def get_image_dimensions(self):
        return self.image_dim

    def render(self, screen: pygame.Surface):

        if self.image is None:
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
