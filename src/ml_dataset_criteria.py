chars = ["A", "B", "C", "D", "E", "F", "G", "H"]
input_width = 10


def is_a(chosen: [str]):
    return ("H" in chosen and "A" not in chosen) or chosen[0] == "E"

