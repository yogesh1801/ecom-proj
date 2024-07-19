# In tasks.py

from celery import shared_task
import requests
from django.conf import settings

@shared_task
def fetch_price(product_id, ordered_item_id):
    from .models import OrderedItem
    product_service_url = f"http://127.0.0.1:8000/api/product/price/{product_id}/"
    
    try:
        response = requests.get(product_service_url)
        response.raise_for_status()
        data = response.json()
        price = data.get('price')
        price = int(price)
        
        if price is not None:
            ordered_item = OrderedItem.objects.get(id=ordered_item_id)
            ordered_item.price = price
            ordered_item.save()
            return price
        else:
            raise ValueError("Price not found in the response")
    
    except requests.RequestException as e:
        print(f"Error fetching price for product {product_id}: {str(e)}")
        return None
    
    except OrderedItem.DoesNotExist:
        print(f"OrderedItem with id {ordered_item_id} not found")
        return None
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

