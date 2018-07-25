from game_entity import GameEntity
from utils.math_utils import *


class Agent(GameEntity):

    is_friendly = True
    name = "Random Guy"
    health = 100.0
    weapon = None

    def is_dead(self):
        return self.health <= 0

    def damage(self, hp: float):
        health = clamp(self.health - hp, 0.)
