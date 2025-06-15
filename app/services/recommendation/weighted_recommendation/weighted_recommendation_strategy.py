from ..recommendation_strategy import RecommendationStrategy
from .recommendations_weights import RecommendationWeights

class WeightedRecommendationStrategy(RecommendationStrategy):
    def __init__(self, weights: RecommendationWeights = RecommendationWeights()):
        """
        Initialize the WeightedRecommendationStrategy with given weights.
        Args:
            weights (RecommendationWeights): Weights for scoring tutorings.
        """
        self.weights = weights

    def recommend(self, available, registered):
        # Get the most common method from registered tutorings
        preferred_method = self._most_common([t.method for t in registered])
        # Get all preferred tutors from registered tutorings
        preferred_tutors = {t.tutor_id for t in registered}
        # Get the IDs of registered tutorings to exclude them from recommendations
        registered_ids = {t.id for t in registered}

        # scored contains tuples of (score, tutoring)
        scored = []
        # Iterate through available tutorings and score them
        for t in available:
            # Skip if the tutoring is already registered
            if t.id in registered_ids:
                continue
            
            score = 0
            # Check if the tutoring method matches the preferred method
            if t.method == preferred_method:
                score += self.weights.method_match
            # Check if the tutoring is from a preferred tutor
            if t.tutor_id in preferred_tutors:
                score += self.weights.preferred_tutor
            # Apply capacity penalty based on the tutoring's capacity
            # Example: if capacity is 10 and step is 5, it will add 1 point (5 - 10 // 5)
            # Is like for each 5 students over the limit, we subtract 1 point
            score += max(0, self.weights.capacity_penalty_limit - t.capacity // self.weights.capacity_penalty_step)
            # Append the score and tutoring to the scored list
            scored.append((score, t))
        # Sort the scored list by score in descending order and return only the tutorings
        # reverse=True means higher scores come first
        scored.sort(key=lambda x: x[0], reverse=True)
        # Return only the tutorings, sorted by their score, the "_" is used to ignore the score in the final result
        return [t for _, t in scored]

    def _most_common(self, items):
        """
        Returns the most common item in a list.
        If the list is empty, returns None.
        """
        return max(set(items), key=items.count) if items else None
