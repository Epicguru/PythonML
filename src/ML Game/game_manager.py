import game_state as gs
from agents import *


def start_game():

    # Creates all enemies, positions the camera, creates friendlies...

    # Reset the stage
    gs.current_stage = 0

    # Create the friendlies...
    gs.friendlies = []
    for i in range(settings.initial_friendlies):
        gs.friendlies.append(FAgent(i))

    gs.enemies = []
    for i in range(settings.total_stages):
        gs.enemies.append([])
        for j in range(settings.enemies_per_stage[i]):
            gs.enemies[i].append(EAgent(j, i))

    print("Started game with %d friendlies" % (len(gs.friendlies)))


timer = 0.0


def update(dt):

    # Move the camera according to the current stage and number of agents on the screen
    gs.camera_controller.target_pos.set_x(gs.current_stage * settings.stage_distance + settings.agent_side_separation * 0.5)
    f = len(gs.friendlies)
    e = len(gs.enemies[gs.current_stage])
    m = f if f > e else e
    y_pos = (m * settings.agent_height_difference - 128.0) * 0.5
    gs.camera_controller.target_pos.set_y(y_pos)

    if gs.completed:
        return

    # Move the stage forwards if all the enemies are dead.
    enemies_gone = len(gs.enemies[gs.current_stage]) == 0
    enemies_dead = True

    for e in gs.enemies[gs.current_stage]:
        if e is not None:
            if not e.is_dead():
                enemies_dead = False
                break

    if enemies_gone or enemies_dead:
        next_stage()
    else:
        global timer
        timer += dt
        if timer >= 0.5:
            timer = 0
            gs.enemies[gs.current_stage][0].damage(25.0)


def next_stage():
    if gs.current_stage == settings.total_stages - 1:
        print("Whoo! You beat the game!")
        gs.completed = True
    else:
        gs.current_stage += 1
        print("Moving on to stage: index #%s" % str(gs.current_stage))
