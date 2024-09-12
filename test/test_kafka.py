from kafka import KafkaProducer

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers='157.66.25.1:9092')

# Define the topic you want to send the message to
topic = 'vps-manager-events'

# Define the message you want to send
message = 'Hello, Kafka!'

# Send the message to the specified topic
producer.send(topic, message.encode('utf-8'))

# Flush to make sure the message is sent
producer.flush()

# Close the producer
producer.close()

print("Message sent to Kafka topic successfully!")
