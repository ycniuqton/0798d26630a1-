import os
import yaml

# Init section
ROOT_PATH = os.path.dirname(__file__)

CONFIG_FILE_PATH = os.path.join(ROOT_PATH, 'env.yaml')

if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, 'r') as r_file:
        config_data = yaml.safe_load(r_file)
else:
    config_data = dict()


class VIRTUALIZOR_CONFIG:
    data = config_data.get("VIRTUALIZOR_CONFIG")

    API_KEY = data.get("API_KEY")
    MANAGER_URL = data.get("MANAGER_URL")


class REDIS_CONFIG:
    data = config_data.get("REDIS_CONFIG")

    REDIS_URI = data.get("REDIS_URI")
