from .__base__ import *
from .cached_resources import *
from .cached_repo import *


def clear_cache():
    cached_plan = CachedPlan()
    cached_os = CachedOS()
    cached_server = CachedServer()
    cached_server_group = CachedServerGroup()

    cached_plan.delete()
    cached_os.delete()
    cached_server.delete()
    cached_server_group.delete()
