from dataclasses import dataclass

@dataclass
class RecommendationWeights:
    """
    Weights for the recommendation strategy.
    These weights are used to score available tutorings based on their attributes.
    """
    # Weights for scoring tutorings
    # method_match is the weight for matching the tutoring method with the most common method of registered tutorings
    method_match: int = 5
    # preferred_tutor is the weight for matching the tutoring with a tutor that has been preferred by the student
    preferred_tutor: int = 3
    # capacity_penalty_step is the step for the capacity penalty, which is applied based on the capacity of the tutoring
    capacity_penalty_step: int = 5
    # capacity_penalty_limit is the limit for the capacity penalty, which is applied based on the capacity of the tutoring
    capacity_penalty_limit: int = 5 
