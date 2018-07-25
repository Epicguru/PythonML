verbose_log = []


def log_turn_action(friendly_index, opponent_index, action, friendlies, opponents, is_friendly):

    text = "%s '%s' (local index %d) used action %d on opponent '%s' (local index %d)" % ("Friendly" if is_friendly else "Enemy",
                                                                                          friendlies[friendly_index].name,
                                                                                          friendly_index,
                                                                                          action,
                                                                                          opponents[opponent_index].name,
                                                                                          opponent_index)
    verbose_log.append(text)
    print(text)
