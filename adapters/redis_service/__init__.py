from .__base__ import *
from .cached_resources import *
from .cached_repo import *
from .resources.cluster import CachedCluster
from .resources.full_data_server_group import CachedFullServerGroup


def clear_cache():
    cached_plan = CachedPlan()
    cached_os = CachedOS()
    cached_server = CachedServer()
    cached_server_group = CachedServerGroup()
    cached_full_server_group = CachedFullServerGroup()
    cached_cluster = CachedCluster()

    cached_plan.delete()
    cached_os.delete()
    cached_server.delete()
    cached_server_group.delete()
    cached_full_server_group.delete()
    cached_cluster.delete()
