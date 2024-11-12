def preprocess_exclude_paths(endpoints):
    allowed_paths = [
        '/api/account/profile/',
        '/api/account/balance/',
        '/api/vps/create',
        '/api/vps/stop/',
        '/api/vps/start/',
        '/api/vps/restart/',
        '/api/vps/rebuild/',
        '/api/vps/change_pass/',
        '/api/vps/',
        '/api/vps/configurations',
    ]
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if path in allowed_paths
    ]


