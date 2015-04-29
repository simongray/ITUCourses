from collections import defaultdict
from shared.utils import powerset
from itertools import combinations

class Apriori:
    """
    Implementation of apriori algorithm adapted from the book's description on pp. 248-253.
    """
    dataset = None
    min_support = None
    min_support_count = None
    min_confidence = None
    _frequent_patterns = None
    _association_rules = None

    def __init__(self, dataset: list, min_support: float, min_confidence: float):
        self.dataset = dataset
        self.min_support = min_support
        self.min_support_count = int(len(dataset) * min_support)
        self.min_confidence = min_confidence

    def _first_level(self) -> set:
        """
        Step one in apriori algorithm - create a set of candidate 1-itemsets and prune in one go.
        """
        candidate_items = defaultdict(int)

        for itemset in self.dataset:
            for item in itemset:
                candidate_items[item] += 1

        return {
            frozenset({item})  # frozenset necessary as Python cannot put regular sets inside sets
            for item, count
            in candidate_items.items()
            if count >= self.min_support_count
        }

    def _prune(self, candidates: set) -> set:
        """
        Prune a set of candidate itemsets according to their support in a dataset.
        """
        pruned_itemsets = set()

        for candidate_itemset in candidates:
            count = 0

            for itemset in self.dataset:
                if candidate_itemset.issubset(itemset):
                    count += 1

            if count >= self.min_support_count:
                pruned_itemsets.add(candidate_itemset)

        return pruned_itemsets

    @classmethod
    def join(cls, itemsets: set) -> set:
        """
        Join two itemsets together, producing l_k+1 from l_k.

        The joined itemsets are bounded by the apriori property.
        """
        k = 0
        next_level = set()

        for itemset_1 in itemsets:
            for itemset_2 in itemsets:
                if itemset_1 != itemset_2:
                    next_level.add(itemset_1.union(itemset_2))

                if not k:
                    k = len(itemset_1)  # so we can limit itemsets to length k+1

        return {
            itemset
            for itemset
            in next_level
            if len(itemset) == k + 1

            # only include itemsets satisfying apriori property
            and all(
                set(subset) in itemsets
                for subset
                in combinations(itemset, len(itemset) - 1)
            )
        }

    @classmethod
    def powerset(cls, itemset) -> set:
        """
        Return the powerset of a set, e.g. powerset({a, b}) = {}, {a}, {b}, {a, b}.
        """
        return [
            frozenset(subset)
            for subset
            in powerset(itemset)
        ]

    def _confidence(self, itemset_a, itemset_b) -> float:
        """
        Confidence(A => B) = P(B|A) = support_count(A.union(B))/support_count(A).
        """
        count_a = 0
        count_ab = 0

        itemset_ab = itemset_a.union(itemset_b)

        for itemset in self.dataset:
            if itemset_a.issubset(itemset):
                count_a += 1

            if itemset_ab.issubset(itemset):
                count_ab += 1

        return count_ab/count_a

    def get_frequent_patterns(self) -> set:
        """
        Get all frequent patterns/itemsets.
        """
        frequent_patterns = set()
        current_level = self._first_level()

        while current_level:
            current_level = self.join(current_level)
            current_level = self._prune(current_level)
            frequent_patterns = frequent_patterns.union(current_level)

        return frequent_patterns

    def get_association_rules(self, itemset: set) -> set:
        """
        Generate association rules for a single frequent pattern/itemset.
        """
        subsets = {
            subset
            for subset
            in self.powerset(itemset)
            if subset
            and itemset != subset
        }

        return {
            (subset_1, subset_2)
            for subset_1 in subsets
            for subset_2 in subsets
            if len(itemset) == len(subset_1) + len(subset_2) == len(subset_1.union(subset_2))
            and self._confidence(subset_1, subset_2) >= self.min_confidence
        }

    @property
    def frequent_patterns(self) -> set:
        if not self._frequent_patterns:
            self._frequent_patterns = self.get_frequent_patterns()

        return self._frequent_patterns

    @property
    def association_rules(self) -> set:
        if not self._association_rules:
            self._association_rules = {
                rule
                for itemset in self.frequent_patterns
                for rule in self.get_association_rules(itemset)
            }

        return self._association_rules

    @property
    def interesting_rules(self) -> set:
        pass  # TODO: use Kulczynski + Imbalance ratio as recommended in book on pp. 267-271.
