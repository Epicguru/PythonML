import game_state as gs
from agents import *
from utils.mouse_utils import *
from battle_log import *
from effect import Effect


def start_game():

    # Creates all enemies, positions the camera, creates friendlies...

    # Reset the stage
    gs.current_stage = 0
    gs.turn_index = 0
    gs.friendly_turn = True
    gs.game_over = False

    # Create the friendlies...
    gs.friendlies = []
    for i in range(settings.initial_friendlies):
        gs.friendlies.append(FAgent(i))

    gs.enemies = []
    for i in range(settings.total_stages):
        gs.enemies.append([])
        for j in range(int(settings.enemies_per_stage[i])):
            gs.enemies[i].append(EAgent(j, i, settings.agent_base_enemy_health * settings.enemies_health_multipliers[i]))

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

    if len(gs.friendlies) == 0 and not gs.game_over:
        gs.game_over = True
        print("All friendlies died! Game over!")

    if gs.completed or gs.game_over:
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
        global stage_timer
        stage_timer += dt
        if stage_timer >= settings.time_before_stage_continue:
            next_stage()
            stage_timer = 0.0
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
stage_timer = 0.0


def update_turns(dt: float):

    global turn_timer
    turn_timer += dt

    is_currently_ai = (gs.friendly_turn and settings.friendly_is_ai) or not gs.friendly_turn

    if turn_timer >= (settings.player_turn_min_interval if not is_currently_ai else settings.turn_min_interval):

        if not is_currently_ai:
            handle_user_input(dt)

        # Wait until we are ready to actually execute the turn...
        if not ready_to_process_turn(dt, is_currently_ai):
            return

        # Process the next turn...
        turn_timer = 0

        # Get info about who's turn it is...
        is_f = gs.friendly_turn
        local_friendlies = gs.friendlies if is_f else gs.enemies[gs.current_stage]
        if gs.turn_index >= len(local_friendlies):
            # Error
            print("ERROR! Index is %d, local friendly count is %d" % (gs.turn_index, len(local_friendlies)))
            print("Is Friendly Team? " + str(is_f))
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

            # Reset the input variables, even if they were not used (in AI vs AI for example)
            global in_target_index
            global in_action_index
            global in_confirmed

            in_target_index = -1
            in_action_index = 0
            in_confirmed = False

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

    performer = friendlies[friendly_index]
    target = opponents[opponent_index]

    log_state(is_friendly, performer, opponent_index, action_index, opponents)

    if action_index == 0:
        # They choose to skip! Ok then...
        spawn_effect(performer, "Clock Icon")

    elif action_index == 1:
        # They want to attack somebody!
        target.damage(performer.get_damage(action_index))
        anim_size = 150
        performer.attack_anim(anim_size if is_friendly else -anim_size)

    elif action_index == 2:
        # Wants to heal self.
        amount = settings.ability_heal_amount
        performer.health = min(performer.health + amount, performer.max_health)
        spawn_effect(performer, "Heal Icon")

    else:
        print("ERROR! Action index %d is invalid!" % action_index)


def spawn_effect(user: Agent, icon_name):

    pos = user.position + Vector2(55 if user.is_friendly else -55, 15)

    Effect(asset_loader.load_image(icon_name + ".png"), pos, 1.0)


def ready_to_process_turn(dt, is_AI):
    return is_AI or ((in_action_index in settings.ability_does_not_require_target or in_target_index != -1) and in_confirmed)


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
        # For now, the enemies just whack a random opponent
        # TODO implement real AI
        return 1, 0
    else:
        # Friendly, what do we do??
        if settings.friendly_is_ai:
            # Here AI code would come in. What action should be taken?
            # TODO start implementing real AI
            return 1, 0
        else:
            return in_action_index, in_target_index


in_action_index = 0
in_target_index = -1
in_confirmed = False


def handle_user_input(dt):
    # TODO return true when done, and action and target index.

    global in_action_index
    global in_confirmed
    global in_target_index

    if gs.selected_agent is not None:
        if not gs.selected_agent.is_friendly:
            if not gs.selected_agent.is_dead():
                if gs.selected_agent in gs.enemies[gs.current_stage]:
                    in_target_index = gs.enemies[gs.current_stage].index(gs.selected_agent)
    else:
        in_target_index = -1

    in_action_index = gs.action_display.s_a

    if (in_action_index in settings.ability_does_not_require_target) or in_target_index != -1:
        if gs.camera_controller.clicked_this_frame:
            in_confirmed = True

            if in_action_index in settings.ability_does_not_require_target:
                in_target_index = 0

    pass
