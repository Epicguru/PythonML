import pygame
import game_state as gs


class GameEntity(object):

    def create(self):
        """Called once the entity has been registered to the system. Update and Render calls will start after this."""
        pass

    def upon_event(self, event: pygame.event):
        """Override and perform logical changes based on the event. Do not draw here, because it won't be rendered."""
        pass

    def update(self, dt: float):
        """Called once per frame, before render. Rendering here is not possible, override the render method."""
        pass

    def render(self, screen: pygame.Surface):
        """Render anything to the screen here. Called once every frame, after all update methods have run."""
        pass

    def late_render(self, screen: pygame.Surface):
        """Render after the normal render call, to ensure that anything drawn here will be on top of the normal objects.
        Normally exclusive for UI elements, but can be used for in-game objects."""
        pass

    def remove(self):
        """Removes from the system, stopping Update and Render calls."""
        gs.entities.remove(self)

        pass

    def to_top(self):
        """Puts the entity at the 'top' of the system, ensuring it will update and render after all other."""
        old_index = gs.entities.index(self)
        gs.entities.remove(self)
        gs.entities.append(self)
        new_index = gs.entities.index(self)

        print("Old index: %s, new index: %s" % (old_index, new_index))


    def to_bottom(self):
        """Puts the entity at the 'top' of the system, ensuring it will update and render after all other."""
        gs.entities.remove(self)
        gs.entities.insert(0, self)
