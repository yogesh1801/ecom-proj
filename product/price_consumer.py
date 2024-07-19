import os
import sys
import django
import pika
import json
import logging
from contextlib import closing

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "product.settings")
django.setup()

from django.conf import settings
from django.shortcuts import get_object_or_404
from product_manage.models import Product

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
        credentials=credentials
    )
    logger.info(f"Attempting to connect to RabbitMQ: {settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}")
    return pika.BlockingConnection(parameters)

def callback(ch, method, properties, body):
    logger.info(f"Received message: {body}")
    try:
        request = json.loads(body)
        product_id = request['product_id']
        
        logger.info(f"Fetching price for product ID: {product_id}")
        price = get_product_price(product_id)
        
        response = json.dumps({'price': str(price)})
        logger.info(f"Sending response: {response}")
        
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                delivery_mode=2),
            body=response
        )
        logger.info(f"Response sent for product ID: {product_id}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Message acknowledged")

def get_product_price(product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        logger.info(f"Price fetched for product {product_id}: {product.price}")
        return str(product.price)
    except Exception as e:
        logger.error(f"Error fetching price for product {product_id}: {e}")
        return None

def start_consuming():
    try:
        logger.info("Attempting to connect to RabbitMQ...")
        with closing(get_rabbitmq_connection()) as connection:
            logger.info("Connected to RabbitMQ successfully")
            with closing(connection.channel()) as channel:
                logger.info("Channel opened")
                channel.queue_declare(queue='product_price_requests', durable=True)
                logger.info("Queue 'product_price_requests' declared")
                
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue='product_price_requests', on_message_callback=callback)
                
                logger.info('Waiting for price requests. To exit press CTRL+C')
                channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
    except KeyboardInterrupt:
        logger.info("Shutting down consumer...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    start_consuming()