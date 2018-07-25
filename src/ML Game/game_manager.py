import game_state as gs
from agents import *
from utils.mouse_utils import *
from battle_log import log_turn_action


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
        update_turns(dt)


def next_stage():
    if gs.current_stage == settings.total_stages - 1:
        print("Whoo! You beat the game!")
        gs.completed = True
    else:
        gs.turn_index = 0
        gs.friendly_turn = True
        gs.current_stage += 1
        print("Moving on to stage: index #%s" % str(gs.current_stage))


turn_timer = 0.0


def update_turns(dt: float):

    global turn_timer
    turn_timer += dt
    if turn_timer >= settings.turn_min_interval:

        # Wait until we are ready to actually execute the turn...
        if not ready_to_process_turn(dt):
            return

        # Process the next turn...
        turn_timer = 0

        # Get info about who's turn it is...
        is_f = gs.friendly_turn
        local_friendlies = gs.friendlies if is_f else gs.enemies[gs.current_stage]
        if gs.turn_index >= len(local_friendlies):
            # Error
            print("ERROR! Index is %d, local friendly count is %d" % (gs.turn_index, len(local_friendlies)))
        else:
            # Get the agent, and their in-game friendly status.
            agent = local_friendlies[gs.turn_index]
            is_in_game_friendly = agent.is_friendly
            turn_index = gs.turn_index
            friendlies = local_friendlies
            opponents = gs.friendlies if not is_in_game_friendly else gs.enemies[gs.current_stage]

            # Process, which returns a result.
            res_action_index, res_opponent_index = process_turn(turn_index, agent, is_in_game_friendly, friendlies, opponents)

            # Execute that result in the game...
            process_result(is_in_game_friendly, res_action_index, res_opponent_index, gs.turn_index, friendlies, opponents)

            # Move the turn system forwards...
            if gs.turn_index >= len(friendlies) - 1:
                # This side's turn is over, switch to the other.
                gs.turn_index = 0
                gs.friendly_turn = not gs.friendly_turn
            else:
                # Move over to the next member of our group.
                gs.turn_index += 1


def process_result(is_friendly, action_index: int, opponent_index: int, friendly_index: int, friendlies: [], opponents: []):

    log_turn_action(friendly_index, opponent_index, action_index, friendlies, opponents, is_friendly)

    if opponent_index >= len(opponents):
        print("ERROR! Opponent index greater than opponent count!")
    if opponent_index < 0:
        print("ERROR! Opponent index is less than zero! Why?")

    if action_index == 0:
        # They choose to skip! Ok then...
        return
    elif action_index == 1:
        # They want to attack somebody!
        # TODO implement.
        pass
    else:
        print("ERROR! Action index %d is invalid!")


def ready_to_process_turn(dt):
    return True

def process_turn(turn_index: int, turn_agent: Agent, friendly: bool, friendlies: [], opponents: []) -> (int, int):
    """
    :param turn_index: The index of the friendly Agent. Note that in this processing section, friendlies may actually be enemies in the normal game, since this method is used to process both enemy and local player actions.
    :param turn_agent: The agent who's turn it is.
    :param friendly: The real in-game friendly state. So if true, this is one of the blue guys.
    :param friendlies: The friendly guys, from the perspective of the turn_agent. May be blue or red, see friendly param.
    :param opponents: The enemies, from the perspective of the turn_agent. May be blue or red, see friendly param.
    :return: A tuple consisting of:
    0: The action index to perform on the target opponent. For now: 0 is skip, 1 is attack.
    1: The target opponent index. Must be in the range 0 len(opponents - 1)
    """

    if not friendly:
        # For now, in-game enemies just skip turns until they die. Yea.
        return 0, 0
    else:
        # Friendly, what do we do??
        return 1, 0

