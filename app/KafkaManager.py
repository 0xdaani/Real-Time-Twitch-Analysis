from confluent_kafka.admin import AdminClient
from kafka import KafkaProducer

import json


class KafkaManager:
    """docstring for KafkaManager"""

    def __init__(self, server: str, topic: str):
        # Configure the Kafka admin client
        self.admin_client = AdminClient({'bootstrap.servers': server})

        # Initialize the Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize messages into JSON
        )

        self.topic = topic

        print(f"[*] Kafka server ready on: {server}")


    # List available topics
    def get_topics_list(self) -> AdminClient:
        return self.admin_client.list_topics()

    # Display the topics
    def print_topics(self) -> None:
        # Lister les topics
        print("[*] List of Kafka topics:")

        # Display the topic names
        for topic in self.admin_client.list_topics().topics:
            print(f"- {topic}")


    # Example function that sends messages to Kafka
    def send_comment_to_kafka(self, comment: str) -> None:
        self.producer.send(self.topic, value=comment)
        self.producer.flush()


if __name__ == '__main__':
    SERVER = 'localhost:9092'
    TOPIC_KAFKA = 'twitch-comments'

    # Usage example
    kafkaManager = KafkaManager(SERVER, TOPIC_KAFKA)
    kafkaManager.print_topics()

    comment = {
        'user': 'viewer123',
        'message': 'Wow, this stream is amazing!',
        'timestamp': '2024-11-30T12:34:56'
    }
    kafkaManager.send_comment_to_kafka(TOPIC_KAFKA, comment)