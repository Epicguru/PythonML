import game_entity
import pygame
import game_state as gs


class Sprite(game_entity.GameEntity):

    def __init__(self, image: pygame.Surface, position=(0, 0)):

        self.image = image
        self.position = position

        # Add to entities automatically.
        gs.entities.append(self)

        pass

    def update(self, dt: float):

        x = self.position[0]
        x += 64.0 * dt
        self.position = (x, self.position[1])

    def render(self, screen: pygame.Surface):

        screen.blit(self.image, self.position + gs.camera_pos)

        pass
