from shared.utils import euclidian_distance


class KNearestNeighbors:

    @staticmethod
    def neighbors(k: int, unknown_datapoint: dict, dataset: list, ignored: list=None) -> list:
        """
        Return the K-nearest neighbors from a dataset for an unknown datapoint.
        """
        dataset = dataset.copy()  # so that the input dataset can be re-used

        if ignored is None:
            ignored = []

        distances = [
            euclidian_distance(a=unknown_datapoint, b=datapoint, ignored=ignored)
            for datapoint
            in dataset
        ]

        nearest_datapoints = []

        # iteratively fetch datapoint in dataset with smallest distance to the unknown
        while k > 0:
            min_distance = min(distances)
            min_distance_index = distances.index(min_distance)
            nearest_datapoints.append(dataset.pop(min_distance_index))
            distances.pop(min_distance_index)
            k -= 1

        return nearest_datapoints
