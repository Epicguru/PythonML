

def get_int(message: str, allow_negatives: bool=True,
            error_message="Invalid integer input!",
            negative_error_message="Invalid input, must be greater to equal to zero!"):

    while True:

        typed = input(message.strip() + " ")
        try:
            num = int(typed)
            if not allow_negatives and num < 0:
                print(negative_error_message)
            else:
                return num
        except ValueError:
            print(error_message)


def get_float(message: str, allow_negatives: bool=True,
              error_message="Invalid real number input!",
              negative_error_message="Invalid input, must be greater to equal to zero!"):

    while True:

        typed = input(message.strip() + " ")
        try:
            num = float(typed)
            if not allow_negatives and num < 0:
                print(negative_error_message)
            else:
                return num
        except ValueError:
            print(error_message)


def get_bool(message: str, error_message="Invalid input! Choose one of the options!", anything_but_true_is_false: bool=False,
             anything_but_false_is_true: bool = False,
             true_text: str="y", false_text="n"):

    while True:

        typed = input(message.strip() + " [" + true_text.strip().upper() + "/" + false_text.strip().upper() + "] ").strip().lower()

        if anything_but_true_is_false:
            if typed == true_text.strip().lower():
                return True
            else:
                return False
        elif anything_but_false_is_true:
            if typed == false_text.strip().lower():
                return False
            else:
                return True
        else:
            if typed == true_text.strip().lower():
                return True
            elif typed == false_text.strip().lower():
                return False
            else:
                print(error_message)
