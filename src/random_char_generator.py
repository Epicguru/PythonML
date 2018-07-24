
def run(take_input=True, line_count=10, min_chars_per_line=10, max_chars_per_line=20):
    print("Running the random character generator...")
    print("")

    import input_helper as ih
    import random

    # Take keyboard input, if required.
    if take_input:
        line_count = ih.get_int("Char line count:")
        min_chars_per_line = ih.get_int("Min chars per line:", allow_negatives=False)
        max_chars_per_line = ih.get_int("Max chars per line:", allow_negatives=False)

    # Validate input.
    if line_count == 0 or max_chars_per_line == 0:
        print("Line count or max chars per line are 0, quitting...")
        return

    if min_chars_per_line > max_chars_per_line:
        print("The min number of chars per line ("
              + str(min_chars_per_line) +
              ") cannot be larger than the max number of chars per line ("
              + str(max_chars_per_line) +
              ")! The minimum has been adjusted to be equal to the maximum.")
        min_chars_per_line = max_chars_per_line

    # Populate a char array with all 256 single-byte characters.
    # Not really necessary, but allows for possible limit/pool of characters to choose from.
    chars = []
    for i in range(50, 100):
        chars.append(chr(i))

    # Generate random sequences of characters based on the input.
    lines = []
    for i in range(line_count):
        cc = random.randrange(min_chars_per_line, max_chars_per_line)
        line = ""
        for j in range(cc):
            line += chars[random.randrange(0, len(chars) - 1)]
        lines.append(line)

    # Print the lines...
    for line in lines:
        print(line)

    # And return them
    return lines


if __name__ == "__main__":
    ls = run(take_input=True)
