import os
import logging
import functools
import json

from logging_setup import setup_logging
setup_logging()
from pika_client.environment_variables import EnvironmentVariable
from pika_client.base import Connector
from pika_client.consumers import BasePubSubConsumer

LOGGER = logging.getLogger(__name__)
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'no-reply@example.com')


class EmailConsumer(BasePubSubConsumer):
    def __init__(
            self,
            service,
            connector,
            app_id='EMAIL_SERVICE',
            queue='emails',
            durable=False,
            exchange='notifications_x',
            exchange_type='topic',
            routing_key='notifications.email'):
        super().__init__(self, connector, app_id, queue, durable, exchange, exchange_type, routing_key)
        self.service = service

    def send_email(self, body):
        body = json.loads(body)
        recepients = body.get('recepients')
        content = body.get('text')
        self.service.send(recepients, content)


class DummyMailService(object):
    def send(self, recepients, body, from_email=FROM_EMAIL):
        LOGGER.info("Mocking email.")
        LOGGER.info("Recepients %s.", recepients)
        LOGGER.info("Content is %s.", content)
        LOGGER.info("From address %s.", from_email)


def subscribe(connector):
    consumer = EmailConsumer(service=DummyMailService(), connector=connector)
    consumer.register_callback('on_message', consumer.send_email)
    LOGGER.info("Starting email consumer.")
    consumer.start()  # start listening infinitely.


def main():
    connector = Connector(EnvironmentVariable.AMQP_URL)
    callback = functools.partial(subscribe, connector)
    connector.register_callback('on_channel_open', callback)
    connector.run()


if __name__ == '__main__':
    main()
