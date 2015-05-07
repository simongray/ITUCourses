from collections import defaultdict
from shared.utils import powerset
from itertools import combinations
import logging
import sys

logger = logging.getLogger('apriori')


class Apriori:
    """
    Implementation of apriori algorithm adapted from the book's description on pp. 248-253.
    """
    dataset = None
    min_support = None
    min_support_count = None
    min_confidence = None
    only_closed = False
    _frequent_patterns = None
    _association_rules = None
    _interesting_rules = None

    def __init__(self, dataset: list, min_support: float, min_confidence: float, closed_patterns: bool=False):
        self.dataset = dataset
        self.min_support = min_support
        self.min_support_count = int(len(dataset) * min_support)
        self.min_confidence = min_confidence
        self.only_closed = closed_patterns  # limit to only closed frequent patterns

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

    def _closed(self, pattern_a):
        """
        Is this frequent pattern closed?
        """
        # TODO: not super efficient to check every pattern + superpatterns against entire dataset...

        occurrences = {
            frequent_pattern: 0
            for frequent_pattern in self._frequent_patterns
            if frequent_pattern.issuperset(pattern_a)
        }

        for itemset in self.dataset:
            for pattern in occurrences.keys():
                if pattern.issubset(itemset):
                    occurrences[pattern] += 1

        for pattern, frequency in occurrences.items():
            if pattern != pattern_a and frequency == occurrences[pattern_a]:
                return False

        return True

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

    def lift(self, rule: tuple):
        """
        Return the Lift correlation measure of some association rule, e.g.

                         P(A union B)
        P(A -> B)   =   -------------
                          P(A)*P(B)

        Exactly 1 implies independence, below 1 implies negative correlation and above 1 positive.
        """
        a = rule[0]
        b = rule[1]
        a_union_b = a.union(b)

        a_occurrences = 0
        b_occurrences = 0
        a_union_b_occurrences = 0
        all_occurrences = len(self.dataset)

        for itemset in self.dataset:
            if a.issubset(itemset):
                a_occurrences += 1
            if b.issubset(itemset):
                b_occurrences += 1
            if a_union_b.issubset(itemset):
                a_union_b_occurrences += 1

        probability_a_union_b = a_union_b_occurrences/all_occurrences
        probability_a = a_occurrences/all_occurrences
        probability_b = b_occurrences/all_occurrences

        return probability_a_union_b/(probability_a*probability_b)

    @property
    def frequent_patterns(self) -> set:
        """
        Frequent patterns as defined by support.
        """
        if not self._frequent_patterns:
            logger.info('calculating frequent patterns')
            frequent_patterns = set()
            current_level = self._first_level()

            while current_level:
                current_level = self.join(current_level)
                current_level = self._prune(current_level)
                frequent_patterns = frequent_patterns.union(current_level)

            self._frequent_patterns = frequent_patterns
            logger.info('finished calculating frequent patterns')

        # limit to only closed patterns to reduce noise
            if self.only_closed:
                logger.info('reducing to only closed frequent patterns')
                closed_patterns = []

                for pattern in self._frequent_patterns:
                    if self._closed(pattern):
                        closed_patterns.append(pattern)

                self._frequent_patterns = closed_patterns
                logger.info('finished reducing to only closed frequent patterns')

        return self._frequent_patterns

    @property
    def association_rules(self) -> set:
        """
        Association rules from frequent patterns as defined by confidence.
        """
        if not self._association_rules:
            logger.info('calculating association rules')

            self._association_rules = {
                rule
                for itemset in self.frequent_patterns
                for rule in self.get_association_rules(itemset)
            }

            logger.info('finished calculating association rules')

        return self._association_rules

    @property
    def interesting_rules(self) -> set:
        """
        Interesting rules from association rules as defined by Lift.
        """
        if not self._interesting_rules:
            logger.info('calculating interesting rules')

            self._interesting_rules = {
                rule
                for rule in self.association_rules
                if self.lift(rule) > 1
            }

            logger.info('finished calculating interesting rules')

        # TODO: use Kulczynski + Imbalance ratio as alternate measure as recommended in book on pp. 267-271.
        return self._interesting_rules
