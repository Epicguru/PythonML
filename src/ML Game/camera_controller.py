from game_entity import GameEntity
from utils.math_utils import *
import game_state as gs


class CameraController(GameEntity):

    speed = 6.0
    target_pos = Vector2(0.0, 0.0)
    current_pos = Vector2(0.0, 0.0)

    def update(self, dt: float):

        self.current_pos = lerp(self.current_pos, self.target_pos, dt * self.speed)
        gs.camera_pos.set(self.current_pos)
