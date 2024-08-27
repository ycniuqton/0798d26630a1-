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


class KafkaConfig:
    _data = config_data.get('KAFKA', {})

    KAFKA_SERVER = _data.get('KAFKA_SERVER')
    TOPIC = _data.get('TOPIC')
    CONSUMER_GROUP = _data.get('CONSUMER_GROUP')
    ENABLE_KAFKA_SSL = _data.get('ENABLE_KAFKA_SSL')
    KAFKA_SECURITY_PROTOCOL = _data.get('KAFKA_SECURITY_PROTOCOL')
    KAFKA_SASL_MECHANISM = _data.get('KAFKA_SASL_MECHANISM')
    KAFKA_SASL_PLAIN_USERNAME = _data.get('KAFKA_SASL_PLAIN_USERNAME')
    KAFKA_SASL_PLAIN_PASSWORD = _data.get('KAFKA_SASL_PLAIN_PASSWORD')
    KAFKA_SSL_CHECK_HOSTNAME = _data.get('KAFKA_SSL_CHECK_HOSTNAME')
    KAFKA_SSL_CA_FILE = _data.get('KAFKA_SSL_CA_FILE')


class PGDBConfig:
    _data = config_data.get('PGDB', {})

    DB_URI = _data.get('DB_URI')

