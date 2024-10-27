from .__base__ import *
from .cached_resources import *
from .cached_repo import *
from .resources.cluster import CachedCluster
from .resources.full_data_server_group import CachedFullServerGroup


def clear_cache(plan=False, os=False, server=False, server_group=False, full_server_group=False, cluster=False):
    if plan:
        CachedPlan().delete()

    if os:
        CachedOS().delete()

    if server:
        CachedServer().delete()

    if server_group:
        CachedServerGroup().delete()

    if full_server_group:
        CachedFullServerGroup().delete()

    if cluster:
        CachedCluster().delete()
