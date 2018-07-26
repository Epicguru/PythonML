from dataset import DataSet
import settings
import os
import datetime

verbose_log = []
f_dataset = DataSet()
e_dataset = DataSet()

def log_turn_action(friendly_index, opponent_index, action, friendlies, opponents, is_friendly):

    text = "%s '%s' (local index %d) used action %d on opponent '%s' (local index %d)" % ("Friendly" if is_friendly else "Enemy",
                                                                                          friendlies[friendly_index].name,
                                                                                          friendly_index,
                                                                                          action,
                                                                                          opponents[opponent_index].name,
                                                                                          opponent_index)
    verbose_log.append(text)
    print(text)

def log_state(is_friendly: bool, performer: "Agent", target_index: int, action_performed: int, opponents: []):

    db = f_dataset if is_friendly else e_dataset

    # 0: The action performed
    # 1: The target index of the action
    #          SPLIT
    # 2: Self health, 0-1
    # 3: Itteration of enemy data:
    # A. Enemy health, size.
    # B. Enemy heath, percentage.

    # TODO add the other parameters

    db.write_column(0, action_performed)
    db.write_column(1, target_index)
    db.write_column(2, performer.health / performer.max_health)

    largest_enemy_count = int(max(settings.enemies_per_stage))

    j = 3
    for i in range(largest_enemy_count):
        if i < len(opponents):
            db.write_column(j, opponents[i].health)
            j += 1
            db.write_column(j, opponents[i].health / opponents[i].max_health)
            j += 1
        else:
            db.write_column(j, 0)
            j += 1
            db.write_column(j, 0)
            j += 1

    db.next()


def save_datasets():

    global f_dataset
    global e_dataset

    exec_num = 0
    try:
        fh = open(settings.path_to_exec_num, "r")
        exec_num = int(fh.readline())
        fh.close()
    except:
        exec_num = 0
        print("Failed to read execution number from file, assuming it is zero and rewriting file.")

    dt = datetime.datetime.now()

    f_path = os.path.join("learning", "saves", "datasets", "{}_Friendly[{:%d %b %H-%M-%S}].ds".format(exec_num, dt))
    f_dataset.save_to_file(f_path, condense=True)

    e_path = os.path.join("learning", "saves", "datasets", "{}_Enemy[{:%d %b %H-%M-%S}].ds".format(exec_num, dt))
    e_dataset.save_to_file(e_path, condense=True)

    exec_num += 1
    fh = open(settings.path_to_exec_num, "w")
    fh.write(str(exec_num))
    fh.close()
