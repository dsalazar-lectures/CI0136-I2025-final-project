# tests/test_weighted_strategy.py

import pytest
from app.services.recommendation.weighted_recommendation import WeightedRecommendationStrategy
from app.services.recommendation.weighted_recommendation import RecommendationWeights


class MockTutoring:
    def __init__(self, id, method, tutor_id, capacity):
        self.id = id
        self.method = method
        self.tutor_id = tutor_id
        self.capacity = capacity


@pytest.fixture
def strategy():
    weights = RecommendationWeights(method_match=5, preferred_tutor=3, capacity_penalty_step=5, capacity_penalty_limit=5)
    return WeightedRecommendationStrategy(weights)


def test_excludes_already_registered(strategy):
    available = [MockTutoring(1, "virtual", "T1", 10)]
    registered = [MockTutoring(1, "virtual", "T1", 10)]
    result = strategy.recommend(available, registered)
    assert result == []


def test_scores_method_match(strategy):
    available = [MockTutoring(2, "virtual", "T2", 10)]
    registered = [MockTutoring(1, "virtual", "T1", 10)]
    result = strategy.recommend(available, registered)
    assert result[0].id == 2


def test_scores_preferred_tutor(strategy):
    available = [MockTutoring(3, "presencial", "T1", 10)]
    registered = [MockTutoring(1, "virtual", "T1", 10)]
    result = strategy.recommend(available, registered)
    assert result[0].id == 3


def test_scores_capacity_penalty(strategy):
    available = [
        MockTutoring(4, "virtual", "T3", 5),   # Better capacity
        MockTutoring(5, "virtual", "T3", 30),  # Worse capacity
    ]
    registered = [MockTutoring(1, "virtual", "T1", 10)]
    result = strategy.recommend(available, registered)
    assert result[0].id == 4


def test_combined_scoring(strategy):
    available = [
        MockTutoring(6, "virtual", "T1", 5),   # Matches all
        MockTutoring(7, "presencial", "T3", 30), # Matches nothing
    ]
    registered = [MockTutoring(1, "virtual", "T1", 10)]
    result = strategy.recommend(available, registered)
    assert result[0].id == 6
