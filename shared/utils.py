from math import sqrt
from collections import Counter
import csv
from itertools import combinations, chain


def load(csv_file, labels: list=None,as_dictionary: bool=False) -> (list, dict):
    """
    Load a CSV file.

    Can optionally load a 2-row CSV file into a dictionary (first row -> key, second fow -> value).
    """
    rows = csv.reader(csv_file)

    if as_dictionary:
        result = {}
    else:
        result = []

    for row in rows:
        if not labels:
            labels = row
        else:
            if as_dictionary:
                if len(row) != 2:
                    raise Exception('can only use 2-row CSV-files with as_dictionary=True')

                result[row[0]] = row[1]
            else:
                result.append(
                    {labels[index]: row[index] for index in range(0, len(row))}
                )

    return result


def euclidian_distance(a: dict, b: dict, ignored: list=None) -> float:
    """
    Calculate the euclidian distance between two data points.

    Attributes such as 'class' can be ignored if specified.
    """
    distances = []

    for key, value in [(attribute, value) for attribute, value in a.items() if attribute not in ignored]:
        if type(value) in (int, float):
            distances.append(float(value - b[key]))
        else:
            if value != b[key]:
                distances.append(1.0)
            else:
                distances.append(0.0)

    return sqrt(sum([distance*distance for distance in distances]))


def mode(datapoints: list, feature: str):
    """
    Get the most common of some feature/attribute in a list of datapoints.
    """
    features = [datapoint[feature] for datapoint in datapoints]
    return Counter(features).most_common(1)[0][0]


def powerset(itemset):
    """
    Return the powerset of a set, e.g. powerset({a, b}) = {}, {a}, {b}, {a, b}.

    Adapted from: https://docs.python.org/3/library/itertools.html
    """
    return chain.from_iterable(
        combinations(itemset, r)
        for r
        in range(len(itemset)+1)
    )


def normalize(dataset: list):
    numerical_attributes = {attribute for attribute, value in dataset[0].items() if type(value) in (int, float)}

    max_datapoint = {}

    # find the max values for every numerical attribute
    for attribute in numerical_attributes:
        max_datapoint[attribute] = max([datapoint[attribute] for datapoint in dataset])

    normalized_dataset = []

    # normalize to range from 0.0 to 1.0
    for datapoint in dataset:
        for attribute in numerical_attributes:
            datapoint[attribute] = datapoint[attribute]/max_datapoint[attribute]

        normalized_dataset.append(datapoint)

    return normalized_dataset
