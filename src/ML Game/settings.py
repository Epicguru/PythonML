import os

path_to_exec_num = os.path.join("learning", "saves", "ExecNum.txt")

stage_sep_distance = 400.0
stage_distance = 400.0

agent_base_friendly_health = 200.0
agent_base_friendly_damage = 50.0

agent_base_enemy_health = 100.0
agent_base_enemy_damage = 25.0

agent_height_difference = 150.0
agent_horizontal_difference = 25.0
agent_side_separation = 300.0

boosted_time_scale = 5.0

friendly_is_ai = False

ability_does_not_require_target = [0, 2]

# How much health is healed.
ability_heal_amount = 30.0

player_turn_min_interval = 0.1
turn_min_interval = 0.6
time_before_stage_continue = 0.4

initial_friendlies = 4
total_stages = 20
enemies_per_stage =                 [1.0, 1.0, 2.0, 3.0, 3.0, 4.0, 4.0, 4.0, 4.0, 4.0, 3.0, 2.0, 1.0, 4.0, 4.0, 4.0, 4.0, 5.0, 5.0, 1.00]
enemies_health_multipliers =        [1.0, 1.0, 1.0, 1.0, 1.2, 1.0, 1.0, 1.0, 1.1, 1.0, 1.5, 2.0, 5.0, 1.3, 1.5, 1.5, 1.6, 1.3, 1.5, 10.0]
