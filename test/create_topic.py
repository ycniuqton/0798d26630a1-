from kafka.admin import KafkaAdminClient, NewTopic


def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1, bootstrap_servers='localhost:9092'):
    # Initialize Kafka admin client
    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id='topic-creation-script'
    )

    # Create a new topic
    topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    try:
        # Attempt to create the topic
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"Topic '{topic_name}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the topic: {e}")
    finally:
        admin_client.close()


# Example usage
create_kafka_topic("new_topic", bootstrap_servers='157.66.25.1:9092')
