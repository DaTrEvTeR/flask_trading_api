import pika

from app.config.settings import settings

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=settings.rabbitmq_host, port=int(settings.rabbitmq_port))
)
channel = connection.channel()
channel.queue_declare(queue="strategy_queue")
