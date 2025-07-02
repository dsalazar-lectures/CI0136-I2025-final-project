from datetime import datetime
from .recommendation_strategy import RecommendationStrategy
from ...models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

class TutoringRecommender:
    def __init__(self, tutoring_repo: FirebaseTutoringRepository, strategy: RecommendationStrategy):
        """
        Initialize the recommender with a tutoring repository and a recommendation strategy.
        Args:
            tutoring_repo (TutoringRepository): Repository to fetch tutorings.
            strategy (RecommendationStrategy): Strategy to use for recommendations.
        """
        self.repo = tutoring_repo
        self.strategy = strategy

    def recommend_for_student(self, student_id):
        """
        Recommend future tutorings for a student based on their registered tutorings.
        Args:
            student_id (str): The ID of the student for whom to recommend tutorings.
        Returns:
            list: A list of recommended tutorings for the student.
        """
        if not student_id:
            return []

        future_tutorings = [
            t for t in self.repo.get_list_tutorials()
            if datetime.strptime(t.date, "%Y-%m-%d") > datetime.now()
        ]
        registered = self.repo.get_tutorials_by_student(student_id)
        return self.strategy.recommend(future_tutorings, registered)
