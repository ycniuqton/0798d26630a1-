from abc import ABC, abstractmethod


class BaseJob(ABC):
    """
    Abstract base class for jobs.
    All jobs should inherit from this class and implement the run() method.
    """

    @abstractmethod
    def run(self):
        """
        This method should be implemented by each job to define the actual task.
        """
        pass
