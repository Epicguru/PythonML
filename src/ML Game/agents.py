from game_entity import GameEntity
import utils.math_utils
import utils.asset_loader
from utils.math_utils import *
from sprite import Sprite
import game_state as gs
import settings


class Agent(GameEntity):

    def __init__(self, index: int):

        self.index = index
        self.is_friendly = True
        self.name = "Random Guy"
        self.health = 100.0
        self.weapon = None
        self.body_sprite = None
        self.position = Vector2(0, 0)

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

        if self.is_dead():
            super().remove()

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

    def update(self, dt: float):
        super().update(dt)

        if self.is_dead():
            return

        self.position.set(lerp(self.position,
                               Vector2(gs.current_stage * settings.stage_sep_distance +
                                       self.index * settings.agent_horizontal_difference,
                                       self.index * settings.agent_height_difference),
                               dt * 3.0))
