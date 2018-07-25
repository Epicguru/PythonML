import game_state as gs
from agents import *


def start_game():

    # Creates all enemies, positions the camera, creates friendlies...

    # Reset the stage
    gs.current_stage = 0

    # Create the friendlies...
    for i in range(settings.initial_friendlies):
        gs.friendlies.append(FAgent(i))

    for i in range(settings.total_stages):
        for j in range(settings.enemies_per_stage[i]):
            gs.enemies[i].append(EAgent(j))

    print("Started game with %d friendlies" % (len(gs.friendlies)))

timer = 0.0

def update(dt):

    gs.camera_controller.target_pos.set_x(gs.current_stage * settings.stage_distance)
    f = len(gs.friendlies)
    e = len(gs.enemies[gs.current_stage])
    m = f if f > e else e
    y_pos = (m * settings.agent_height_difference - 128.0) * 0.5
    gs.camera_controller.target_pos.set_y(y_pos)

    global timer
    timer += dt
    if timer > 3.0:
        timer = 0.0
        gs.current_stage += 1
