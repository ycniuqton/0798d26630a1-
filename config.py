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


class ADMIN_CONFIG:
    data = config_data.get("ADMIN_CONFIG", {})

    API_KEY = data.get("API_KEY")
    URL = data.get("URL")


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


class APPConfig:
    _data = config_data.get('APP_CONFIG', {})
    APP_ROLE = _data.get('APP_ROLE', 'ctv')
    APP_NAME = _data.get('APP_NAME', 'World Server')
    BANK_NAME = _data.get('BANK_NAME')
    BANK_ACCOUNT = _data.get('BANK_ACCOUNT')
    BANK_USERNAME = _data.get('BANK_USERNAME')
    WEBHOOK_TOKEN = _data.get('WEBHOOK_TOKEN')
    VND_USD_EXCHANGE_RATE = _data.get('VND_USD_EXCHANGE_RATE', 26000)



class KafkaNotifierConfig:
    _data = config_data.get('KAFKA_NOTIFIER', {})

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


class PaypalConfig:
    _data = config_data.get("PAYPAL_CONFIG", {})

    CLIENT_ID = _data.get("CLIENT_ID")
    CLIENT_SECRET = _data.get("CLIENT_SECRET")
    MODE = _data.get("MODE")
    RETURN_URL = _data.get("RETURN_URL")
    CANCEL_URL = _data.get("CANCEL_URL")

