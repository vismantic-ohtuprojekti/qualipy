def collective_result_certain_limit(algorithms, certain_limit, input):
    non_certain_predictions = []
    certain_predictions = []

    for algorithm in algorithms:
        prediction = algorithm(input)

        if prediction == None:
            continue
        elif prediction <= (certain_limit) or prediction >= (1.0 - certain_limit):
            certain_predictions.append(prediction)
        else:
            non_certain_predictions.append(prediction)

    if len(certain_predictions) != 0:
        return sum(certain_predictions) / len(certain_predictions)
    else:
        return sum(non_certain_predictions) / len(non_certain_predictions)
