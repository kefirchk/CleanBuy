from confluent_kafka.admin import AdminClient, NewTopic

from src.kafka import kafka_config


def create_topic(topic_name, num_partitions=1, replication_factor=1):
    conf = {
        'bootstrap.servers': kafka_config.KAFKA_BOOTSTRAP_SERVERS
    }
    admin_client = AdminClient(conf)

    # Создание топика
    new_topic = NewTopic(
        topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )
    fs = admin_client.create_topics([new_topic])

    # Проверка статуса создания топика
    for topic, future in fs.items():
        try:
            future.result()
            print(f"[INFO] Topic {topic} created successfully")
        except Exception as e:
            print(f"[ERROR] Failed to create topic {topic}: {e}")