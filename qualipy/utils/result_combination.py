"""
Contains functions that can be used to construct a single
prediction from multiple predictions.
"""


def collective_result(results, limit):
    """Combines many results in the range [0, 1] into a single
    value in the range [0, 1]. A limit can be specified for a
    value that is regarded as certain enough. If any certain
    results are found, the mean of all certain results is
    returned, otherwise the mean of all results is returned.

    :param results: the list of results to be combined
    :type results: list
    :param limit: a limit in the range [0, 1] for a result
                  to be considered correct
    :type limit: float
    :returns: float
    """
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
