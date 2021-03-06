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
        self.use_late_render = False

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

    def get_position(self):
        return self.position

    def set_position(self, pos: Vector2):
        self.position.set(pos)

    def get_image_dimensions(self):
        return self.image_dim

    def update(self, dt: float):

        self.bounds.center = (self.position.get_x() + self.pivot[0], self.position.get_y() + self.pivot[1])

    def render(self, screen: pygame.Surface):

        if not self.use_late_render:
            self.draw(screen)

    def late_render(self, screen: pygame.Surface):

        if self.use_late_render:
            self.draw(screen)

    def draw(self, screen):
        if self.image is None:
            return
        if not self.enabled:
            return

        x, y = translate((self.get_position().get_x(), self.get_position().get_y()), self.get_image_dimensions(), self.get_pivot())

        if x > gs.resolution[0]:
            return
        if y > gs.resolution[1]:
            return
        if x + self.get_image_dimensions()[0] < 0:
            return
        if y + self.get_image_dimensions()[1] < 0:
            return

        screen.blit(self.image, (x, y))


def translate(pos: (float, float), size: (float, float), pivot: (float, float)) -> (float, float):
    x = (pos[0] -
         gs.camera_pos.get_x() + gs.resolution[0] * 0.5 -
         size[0] * pivot[0])

    y = (-pos[1] -
         size[1] + gs.camera_pos.get_y()
         + gs.resolution[1] * 0.5 +
         size[1] * pivot[1])

    return x, y
