import logging
import functools
import json

from logging_setup import setup_logging
setup_logging()
from pika_client.environment_variables import EnvironmentVariable
from pika_client.base import Connector
from pika_client.consumers import BasePubSubConsumer

LOGGER = logging.getLogger(__name__)


class EmailConsumer(BasePubSubConsumer):
    pass


def subscribe(connector):
    consumer = EmailConsumer(
        connector,
        app_id='EMAIL_SERVICE',
        queue='emails',
        exchange='notifications_x',
        exchange_type='topic',
        routing_key='notifications.email'
    )
    consumer.register_callback('on_message', send_email)
    LOGGER.info("Starting email consumer.")
    consumer.start()  # start listening infinitely.


def send_email(body):
    body = json.loads(body)
    recepients = body.get('recepients')
    content = body.get('text')
    LOGGER.info("Mocking email.")
    LOGGER.info("Recepients %s.", recepients)
    LOGGER.info("Content is %s.", content)


def main():
    connector = Connector(EnvironmentVariable.AMQP_URL)
    callback = functools.partial(subscribe, connector)
    connector.register_callback('on_channel_open', callback)
    connector.run()


if __name__ == '__main__':
    main()
