import pygame
import game_state as gs


class GameEntity(object):

    def init(self):
        # Called at the beginning of the program, but not if added at runtime.
        # If added at runtime, just use the constructor to load assets or initialize.
        pass

    def upon_event(self, event: pygame.event):
        # Override and perform logical changes based on the event. Do not draw here, because it won't be rendered.
        pass

    def update(self, dt: float):
        # Called once per frame, before render. Rendering here is not possible, override the render method.
        pass

    def render(self, screen: pygame.Surface):
        # Render anything to the screen here. Called once every frame, after all update methods have run.
        pass

    def delete(self):

        gs.entities.remove(self)

        pass
