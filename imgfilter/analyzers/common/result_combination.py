def collective_result(results, limit):
    certain, non_certain = [], []
    for prediction in results:
        if prediction is None:
            continue
        elif prediction <= limit or prediction >= 1 - limit:
            certain.append(prediction)
        else:
            non_certain.append(prediction)

    if certain:
        return sum(certain) / len(certain)
    else:
        return sum(non_certain) / len(non_certain)
