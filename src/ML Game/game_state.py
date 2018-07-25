from utils.math_utils import *

running = True
entities = []

time_scale = 1.0
target_frame_rate = 60
bg_colour = (230, 230, 230)
camera_pos = Vector2(0, 0)
resolution = (800, 600)
frames_per_second = target_frame_rate
camera_controller = None

completed = False

current_stage = 0
friendly_turn = True
turn_index = 0

friendlies = []
"""A 2D array, where the outer array are the stages and the inner arrays are the list of enemies themselves."""
enemies = []


def register_entity(entity: "GameEntity"):
    if entity is not None and entity not in entities:
        entities.append(entity)
        entity.create()
