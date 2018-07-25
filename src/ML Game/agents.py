from game_entity import GameEntity
import utils.math_utils
import utils.asset_loader
from utils.math_utils import *
from utils import asset_loader
from sprite import Sprite
import game_state as gs
import settings
import random


class Agent(GameEntity):

    def __init__(self, index: int):

        self.index = index
        self.highlighted = False
        self.is_friendly = True
        self.name = "Random Guy"
        self.max_health = 100.0
        self.health = 100.0
        self.weapon = None
        self.body_sprite = None
        self.highlight_sprite = Sprite(asset_loader.load_image("Agent Highlight.png"))
        self.position = Vector2(0, 0)
        self.offset = Vector2(0, 0)
        self.rumble = Vector2(0, 0)
        self.rumble_mag = 0.0
        self.rumble_decay = 5.0

        # Register
        gs.register_entity(self)

    def is_dead(self):
        return self.health <= 0

    def damage(self, hp: float):
        self.health = max(self.health - hp, 0.0)

    def update(self, dt: float):

        if self.body_sprite is not None:
            self.body_sprite.set_pivot(0.5, 0.5)
            self.body_sprite.set_position(self.position)

        self.rumble_mag = lerp(self.rumble_mag, 0.0, dt * self.rumble_decay)
        self.rumble.set_x(random.randrange(-1, 1))
        self.rumble.set_y(random.randrange(-1, 1))
        self.rumble.normalize()
        self.rumble *= self.rumble_mag
        self.offset.set(self.rumble)

        if self.highlighted:
            self.highlight_sprite.position.set(self.position + self.offset)
            self.highlight_sprite.to_bottom()
            self.highlight_sprite.set_pivot(0.5, 0.5)
        self.highlight_sprite.enabled = self.highlighted

        if self.is_dead():
            super().remove()
            self.body_sprite.remove()
            self.highlight_sprite.remove()
            self.died()

    def died(self):
        pass

    def to_top(self):
        super().to_top()

        if self.body_sprite is not None:
            self.body_sprite.to_top()

    def to_bottom(self):
        super().to_bottom()

        if self.body_sprite is not None:
            self.body_sprite.to_bottom()


class FAgent(Agent):

    def create(self):

        self.is_friendly = True
        self.body_sprite = Sprite(utils.asset_loader.load_image("Friendly.png"))
        self.name = "Good Guy #" + str(self.index + 1)

    def damage(self, hp: float):
        super().damage(hp)
        self.rumble_mag = 20.0

    def update(self, dt: float):

        if not self.is_dead():
            target = Vector2(
                gs.current_stage * settings.stage_sep_distance + self.index * settings.agent_horizontal_difference,
                self.index * settings.agent_height_difference)
            calculated_pos = lerp(self.position, target, dt * 3.0)
            self.position.set(calculated_pos + self.offset)

        super().update(dt)


class EAgent(Agent):

    def __init__(self, index: int, stage: int):
        Agent.__init__(self, index)

        self.stage = stage

    def create(self):

        self.is_friendly = False
        self.body_sprite = Sprite(utils.asset_loader.load_image("Enemy.png"))
        self.name = "Bad Guy #" + str(self.index + 1)

    def damage(self, hp: float):

        super().damage(hp)
        self.rumble_mag = 20.0

    def died(self):

        gs.enemies[self.stage].remove(self)

    def update(self, dt: float):

        if not self.is_dead():

            target = Vector2(self.stage * settings.stage_sep_distance -
                             self.index * settings.agent_horizontal_difference +
                             settings.agent_side_separation,
                             self.index * settings.agent_height_difference)
            self.position.set(target + self.offset)

        super().update(dt)
