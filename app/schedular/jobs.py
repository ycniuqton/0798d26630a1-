from .__base__ import BaseJob
from adapters.redis_service import CachedVpsStatRepository


class UpdateVpsStat(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        cvr = CachedVpsStatRepository()
        cvr.reload()
        print("Vps stats updated!")
