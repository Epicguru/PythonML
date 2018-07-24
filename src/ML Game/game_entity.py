import pygame


class GameEntity(object):

    def upon_event(self, event):
        # Override and perform logical changes based on the event. Do not draw here, because it won't be rendered.
        pass

    def update(self, dt: float):
        # Called once per frame, before render. Rendering here is not possible, override the render method.
        pass

    def render(self, screen: pygame.Surface):
        # Render anything to the screen here. Called once every frame, after all update methods have run.
        pass
