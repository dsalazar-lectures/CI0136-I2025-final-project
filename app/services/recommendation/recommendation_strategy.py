from abc import ABC, abstractmethod

# This is an abstract base class for recommendation strategies.
class RecommendationStrategy(ABC):
    """
    Abstract base class for recommendation strategies.
    This class defines the interface for recommending tutorings based on available and registered tutorings.
    It should be extended by concrete strategies that implement the `recommend` method.
    """
    @abstractmethod
    def recommend(self, available, registered):
        """
        Recommend tutorings based on available and registered tutorings.
        Args:
            - available(list): List of available tutorings.
            - registered(list): List of tutorings the student is already registered in.
        Returns:
            - list: List of recommended tutorings.
        """
        pass


