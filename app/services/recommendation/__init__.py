from .recommender import TutoringRecommender
from .weighted_recommendation import RecommendationWeights, WeightedRecommendationStrategy
from ...models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

def get_tutoring_recommender(student_id: str, repository: FirebaseTutoringRepository):
  """
  Get a tutoring recommender for a student.
  Args:
      student_id (str): The ID of the student for whom to get recommendations.
      repository (FirebaseTutoringRepository): The repository to fetch tutorings from.
  Returns:
      TutoringRecommender: An instance of TutoringRecommender configured for the student.
  """
  default_recomendation_strategy = WeightedRecommendationStrategy()
  recomendator = TutoringRecommender(repository, default_recomendation_strategy)
  return recomendator.recommend_for_student(student_id)


