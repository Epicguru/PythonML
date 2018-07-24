

def main():

    from dataset import DataSet
    from random import randrange as rr
    import input_helper as ih
    import ml_dataset_criteria as criteria

    ds = DataSet()

    chars = criteria.chars
    number_to_give = criteria.input_width

    manual = False
    count = 50000

    m = 0
    while True:

        m += 1
        i = m < (count + 1)

        if manual:
            i = ih.get_bool("Do you want to continue?", anything_but_false_is_true=True)
        if i:
            # Make random char list...
            chosen = []
            for j in range(number_to_give):
                chosen.append(chars[rr(0, len(chars))])

            # Make a strip a line based on the chosen chars
            line = ""
            for c in chosen:
                line += c + "  "
            line = line.strip()

            print("Given the following chars, what do you choose?")
            print("   " + line)

            if manual:
                op = ih.get_bool("Choose A or B, based on a fixed criteria.", false_text="B", true_text="A")
            else:
                op = criteria.is_a(chosen)

            if not manual:
                if op:
                    print("Auto-chose A")
                else:
                    print("Auto-chose B")

            # Add the source and chosen option to the dataset.
            k = 0
            for c in chosen:
                ds.write_column(k, chars.index(c))
                k += 1

            op_value = 0
            if op:
                op_value = 1
            ds.write_column(k, op_value)
            ds.next()
        else:
            print("Done! Printing and saving dataset...")
            break

    print(ds)
    ds.save_to_file("Test Data Set.txt", condense=True)


if __name__ == "__main__":
    main()
