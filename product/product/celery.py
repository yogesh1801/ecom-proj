import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product.settings')

app = Celery('product_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('product_queue', Exchange('product_queue'), routing_key='product_queue'),
)

app.conf.task_routes = {
    'product_manage.tasks.get_product_price': {'queue': 'product_queue'},
}