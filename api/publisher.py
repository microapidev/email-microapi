import pika, os, logging

logging.basicConfig()

# parse CloudAMQP URL.Fall back to localhost
url = os.environ.get("ClOUDAMQP_URL", "amqp://guest:guest@localhost/%2f")
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # Start a channel
channel.queue_declare(queue='mailprocess') # Declare a queue

# SEnd a message

channel.basic_publish(exchange='', routing_key='mailprocess', body='User Information')
print('[x] Message sent to consumer')
connection.close()

import pika

RABBITMQ_HOST = "localhost"

class MailQueuePublisher(object):
    def __init__(self):
        pass
    
    def connect_queue(self):
        if not hasattr(self, 'rabbitmq'):
            self.rabbitmq = pika.BlockingConnection(pika.ConnectionParameters(
                host= RABBITMQ_HOST
            ))
        return self.rabbitmq

    def get_mail_queue(self):
        if not hasattr(self, "mail_queue"):
            conn = connect_queue()
            channel = conn.channel()
            channel.queue_declare(queue="mail_queue", durable=True)
            channel.queue_bind(exchange="amq.direct", queue="mail_queue")
            self.welcome_queue = channel
        return self.welcome_queue

    def close_queue(self, error):
        if hasattr(self, 'rabbitmq'):
            self.rabbitmq.close()
