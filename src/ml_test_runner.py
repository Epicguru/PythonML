

def main():

    print("Importing tensorflow, keras, plotting lib...")

    from keras.models import Sequential
    from keras.models import load_model
    from keras.layers import Dense
    import numpy
    from random import randrange as rr
    import ml_dataset_criteria as criteria
    import matplotlib.pyplot as plt

    # fix random seed for reproducibility
    numpy.random.seed(7)

    input_size = criteria.input_width

    load = False
    save = True

    dataset = numpy.loadtxt("Test Data Set.txt", delimiter=",")

    # split into input (X) and output (Y) variables
    X = dataset[:, 0:input_size]
    Y = dataset[:, input_size]

    if load:
        model = load_model("Model.h5")
    else:
        # create model
        model = Sequential()
        model.add(Dense(64, input_dim=input_size, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model...
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model using the example data, just once for now...
        history = model.fit(X, Y, epochs=150, batch_size=40, verbose=3)

        scores = model.evaluate(X, Y)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

        if save:
            model.save("Model.h5")

    chars = criteria.chars
    accuracy = 0
    count = 100

    predictions = []
    correct = []

    for i in range(count):
        chosen = []
        chosen_indices = []
        for j in range(input_size):
            index = rr(0, len(chars))
            chosen_indices.append(index)
            chosen.append(chars[index])
        predicted = model.predict(numpy.array(chosen_indices).reshape((1, input_size)))
        predictions.append(predicted[0][0])

        rounded = round(predicted[0][0])
        a_or_b = "x"
        if rounded == 1:
            a_or_b = "A"
        else:
            a_or_b = "B"

        line = ""
        for j in chosen:
            line += j + "  "
        line = line.strip()
        print("Given:")
        print(line)
        print("Predicted: " + a_or_b)

        # Check the criteria against the algorithm, assuming that the data has been generated automatically.
        is_a = criteria.is_a(chosen)
        correct.append(1.0 if is_a else 0.0)
        predicted_a = rounded == 1
        worked = is_a == predicted_a
        if worked:
            accuracy += 1
    accuracy /= count
    accuracy *= 100

    print("Accuracy (based on ml_dataset_criteria) is %s%%" % str(round(accuracy)))

    x = numpy.arange(0, count, 1);
    plt.plot(predictions)
    plt.plot(correct, "go")
    plt.title("Predictions")
    plt.xlabel("Test Number")
    plt.ylabel("Predicted Value")
    plt.axhline(y = 0.5, color="orange")
    for i in range(count):
        if not round(predictions[i]) == correct[i]:
            plt.axvline(x=i, color="red", ymin=0.4, ymax=0.6)
    plt.show()


if __name__ == "__main__":
    main()
