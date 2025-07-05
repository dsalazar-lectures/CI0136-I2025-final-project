from abc import ABC, abstractmethod

class IScheduler(ABC):
    """
    Abstract base class for a scheduler that manages tasks.
    """

    @abstractmethod
    def schedule_task(self, task: callable, interval: int):
        """
        Schedule a task to run at a specified interval.

        :param task: The task to be scheduled.
        :param interval: The time interval for the task in minutes.
        """
        pass

    @abstractmethod
    def start(self):
        """
        Start the scheduler.
        """
        pass