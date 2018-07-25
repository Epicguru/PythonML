import game_state as gs
from agents import *
from utils.mouse_utils import *


def start_game():

    # Creates all enemies, positions the camera, creates friendlies...

    # Reset the stage
    gs.current_stage = 0
    gs.turn_index = 0
    gs.friendly_turn = True

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
    e = settings.enemies_per_stage[gs.current_stage]
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


def process_turn(turn_index: int, turn_agent: Agent, friendly: bool, friendlies: [], opponents: []) -> (int, int):
    """

    :param turn_index: The index of the friendly Agent. Note that in this processing section, friendlies may actually be enemies in the normal game, since this method is used to process both enemy and local player actions.
    :param turn_agent: The agent who's turn it is.
    :param friendly: The real in-game friendly state. So if true, this is one of the blue guys.
    :param friendlies: The friendly guys, from the perspective of the turn_agent. May be blue or red, see friendly param.
    :param opponents: The enemies, from the perspective of the turn_agent. May be blue or red, see friendly param.
    :return: A tuple consisting of:
    0: The target opponent index. Must be in the range 0 len(oponents - 1)
    1: The action index to perform on the target opponent. Not implemented yet, just set it to 0.
    """

    pass