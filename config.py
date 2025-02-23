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
    APP_DOMAIN = _data.get('APP_DOMAIN', 'worldsever.com')
    BANK_NAME = _data.get('BANK_NAME')
    BANK_ACCOUNT = _data.get('BANK_ACCOUNT')
    BANK_USERNAME = _data.get('BANK_USERNAME')
    WEBHOOK_TOKEN = _data.get('WEBHOOK_TOKEN')
    VND_USD_EXCHANGE_RATE = _data.get('VND_USD_EXCHANGE_RATE', 26000)
    MINIMUM_SUSPEND_THRESHOLD = _data.get('MINIMUM_SUSPEND_THRESHOLD', 2)
    VPS_REFUND_HOURS = _data.get('VPS_REFUND_HOURS', 24)
    LOG_PATH = _data.get('LOG_PATH', './info.log')
    CRYPTO_API_KEY = _data.get('CRYPTO_API_KEY', '1234567890123456')
    MERCHANT_ID = _data.get('MERCHANT_ID', '1234567890123456')
    CRYPTO_RETURN_URL = _data.get('CRYPTO_RETURN_URL', 'http://localhost:5000/api/v1/payment/callback')
    CRYPTO_WEBHOOK_URL = _data.get('CRYPTO_WEBHOOK_URL', 'http://localhost:5000/api/v1/payment/webhook')
    STRIPE_API_KEY = _data.get('STRIPE_API_KEY', '1234567890123456')
    STRIPE_RETURN_URL = _data.get('STRIPE_RETURN_URL', 'http://localhost:5000/api/v1/payment/callback')


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


class MailSenderConfig:
    _data = config_data.get("MAIL_SENDER", {})

    MAIL_SERVER = _data.get("MAIL_SERVER")
    MAIL_PORT = _data.get("MAIL_PORT")
    MAIL_USERNAME = _data.get("MAIL_USERNAME")
    MAIL_PASSWORD = _data.get("MAIL_PASSWORD")


class NotificationGatewayConfig:
    _data = config_data.get("NOTIFICATION_GATEWAY", {})

    KAFKA_SERVER = _data.get("KAFKA_SERVER")
    TOPIC = _data.get("TOPIC")
    CONSUMER_GROUP = _data.get("CONSUMER_GROUP")
    ENABLE_KAFKA_SSL = _data.get('ENABLE_KAFKA_SSL')
    KAFKA_SECURITY_PROTOCOL = _data.get('KAFKA_SECURITY_PROTOCOL')
    KAFKA_SASL_MECHANISM = _data.get('KAFKA_SASL_MECHANISM')
    KAFKA_SASL_PLAIN_USERNAME = _data.get('KAFKA_SASL_PLAIN_USERNAME')
    KAFKA_SASL_PLAIN_PASSWORD = _data.get('KAFKA_SASL_PLAIN_PASSWORD')
    KAFKA_SSL_CHECK_HOSTNAME = _data.get('KAFKA_SSL_CHECK_HOSTNAME')
    KAFKA_SSL_CA_FILE = _data.get('KAFKA_SSL_CA_FILE')


class CustomInfo:
    _data = config_data.get("CUSTOM_INFO", {})

    INVOICE_TERM_CONDITION = _data.get("INVOICE_TERM_CONDITION", "No refund")
    COMPANY_ADDRESS = _data.get("COMPANY_ADDRESS", "Hanoi, Vietnam")
    COMPANY_PHONE = _data.get("COMPANY_PHONE", "0123456789")
    APP_DOMAIN = _data.get("APP_DOMAIN", "https://yourdomain.com")


class VNCConfig:
    _data = config_data.get("VNC_CONFIG", {})
    DOMAIN_URL = _data.get("DOMAIN_URL", "localhost")
    PORT = _data.get("PORT", 6081)
    SESSION_DURATION = _data.get("SESSION_DURATION", 30)  # Default 6 hours


class GoogleOAuthConfig:
    _data = config_data.get("GOOGLE_OAUTH2", {})

    CLIENT_ID = _data.get("CLIENT_ID", '')
    CLIENT_SECRETS_FILE = _data.get("CLIENT_SECRETS_FILE", "client_secrets.json")
    REDIRECT_URI = _data.get("REDIRECT_URI", "http://localhost:8000/oauth2/callback")
    INSECURE_TRANSPORT = _data.get("INSECURE_TRANSPORT", '1')
