from game_entity import GameEntity
import utils.math_utils
import utils.asset_loader
from utils.math_utils import *
from sprite import Sprite
import game_state as gs
import settings
import random


class Agent(GameEntity):

    def __init__(self, index: int):

        self.index = index
        self.is_friendly = True
        self.name = "Random Guy"
        self.health = 100.0
        self.weapon = None
        self.body_sprite = None
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

        if self.is_dead():
            super().remove()
            self.body_sprite.remove()

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

    def damage(self, hp: float):

        super().damage(hp)
        self.rumble_mag = 20.0

    def update(self, dt: float):

        if not self.is_dead():

            target = Vector2(self.stage * settings.stage_sep_distance -
                             self.index * settings.agent_horizontal_difference +
                             settings.agent_side_separation,
                             self.index * settings.agent_height_difference)
            self.position.set(target + self.offset)

        super().update(dt)
