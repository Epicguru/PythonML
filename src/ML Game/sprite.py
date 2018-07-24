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

    def render(self, screen: pygame.Surface):

        if self.image is None:
            return

        screen.blit(self.image, (self.position[0] - gs.camera_pos[0], self.position[1] + gs.camera_pos[1]))

        pass
