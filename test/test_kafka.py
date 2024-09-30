import json

from kafka import KafkaProducer

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers='157.66.24.255:9092')

# Define the topic you want to send the message to
topic = 'vps-manager-notification-gateway'

# Define the message you want to send
message = {
    'event_type': 'send_mail',
    'payload': {
        "type": "REGISTER",
        "data": {
            "receiver": "ngohongqui@gmail.com",
            "subject": "Welcome to VPS Manager",
            "body": "This is a test email from VPS Manager.",
            'recipient_name': 'Quincy',
            'platform_name': 'World Sever',
            'current_year': 2024
        }
    }
}
message = {
    'event_type': 'send_mail',
    'payload': {
        "type": "VERIFY_EMAIL",
        "data": {
            "receiver": "ngohongqui@gmail.com",
            "subject": "World Sever - Verify Your Email Address",
            'recipient_name': 'Quincy',
            'platform_name': 'World Sever',
            'verification_link': 'https://worldsever.com/verify?token=abcd1234',
            'current_year': 2024

        }
    }
}

message = {
    'event_type': 'send_mail',
    'payload': {
        "type": "CREATE_VPS",
        "data": {
            "receiver": "ngohongqui@gmail.com",
            "subject": "Your VPS has been created successfully",
            'customer_name': 'John Doe',
            'vps_hostname': 'vps123.worldsever.com',
            'vps_ip': '192.168.1.100',
            'vps_os': 'Ubuntu 20.04',
            'vps_username': 'root',
            'vps_password': 'password1234',
            'current_year': 2024,
            'platform_name': 'WorldSever VPS Services'
        }
    }
}

message = json.dumps(message)

# Send the message to the specified topic
producer.send(topic, message.encode('utf-8'))

# Flush to make sure the message is sent
producer.flush()

# Close the producer
producer.close()

print("Message sent to Kafka topic successfully!")
