
def run():

    # Create a model that will execute one action, on one enemy, give only the current environment variables.
    # For now it will control the friendly team but it could also be used to control the enemy team, using the same
    # learned data, essentially making the enemy play like the player does.

    from keras.models import Sequential
    from keras.models import load_model
    from keras.layers import Dense
    import numpy
    from random import randrange as rr
    import ml_dataset_criteria as criteria
    import matplotlib.pyplot as plt
    import os
    import input_helper

    # First find all available datasets to load...
    files = os.listdir(os.path.join("saves", "datasets"))

    # What are we going to train, and using what data?
    training_file = None

    for i, file in enumerate(files):
        num = int(file.split("_")[0])
        is_friendly = "Friendly" in file

        print("%d: Exec %d, %s" % (i, num, "Friendly" if is_friendly else "Enemy"))

    chosen_index = -1
    while True:
        chosen_index = input_helper.get_int("Choose an option index:", allow_negatives=False)
        if chosen_index < len(files):
            break

    training_file = files[chosen_index]
    files = None

    # Lets train the action taken, which is at index 0
    target_index = 0

    # Lets load the dataset...
    dataset = numpy.genfromtxt(os.path.join("saves", "datasets", training_file), delimiter=",")

    x = dataset[:, 2:]
    y = dataset[:, 0:2]

    # Let's make a model...
    model = Sequential()
    model.add(Dense(64, input_dim=len(x[0]), activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2, activation='sigmoid'))

    # Compile model...
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model using the example data, just once for now...
    history = model.fit(x, y, epochs=500, batch_size=20, verbose=3)

    scores = model.evaluate(x, y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    txt = "0.875, 100.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0"
    split = txt.split(",")
    flts = []
    for t in split:
        flts.append(float(t))

    predictions = model.predict(numpy.array(flts).reshape((1, len(split))))[0]
    print(str(predictions[0]) + ", " + str(predictions[1]))
    print("k bye")


if __name__ == "__main__":
    run()
