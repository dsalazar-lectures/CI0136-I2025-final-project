from .i_scheduler import IScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

class APScheduler(IScheduler):
    """
    Concrete implementation of IScheduler using APScheduler.
    """

    def __init__(self):
        self.scheduler = BlockingScheduler()

    def schedule_task(self, task: callable, interval: int):
        """
        Schedule a task to run at a specified interval.
        :param task: The task to be scheduled (a callable).
        :param interval: The time interval for the task in minutes.
        """
        self.scheduler.add_job(func=task, trigger='interval', minutes=interval)

    def start(self):
        """
        Start the scheduler.
        """
        self.scheduler.start()