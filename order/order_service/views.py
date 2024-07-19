from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from order_service import forms, models
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers import serialize
import json

@csrf_exempt
def create_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        form = forms.OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.ordered_by = request.user
            order.save()
            return JsonResponse({
            'message': f"Order created Successfully with id {order.id}"
            })
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)

@csrf_exempt
def get_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'GET':
        orders = models.Order.objects.filter(ordered_by=request.user)
        page_number = request.GET.get('page', 1)
        paginator = Paginator(orders, 10) 
        page_obj = paginator.get_page(page_number)
        
        orders_data = []
        for order in page_obj:
            order_data = {
                'id': order.id,
                'status': order.status,
                'created_at': order.created_at,
                'total_price': float(order.get_total_price()),
                'items_count': order.items.count()
            }
            orders_data.append(order_data)

        return JsonResponse({
            'orders': orders_data,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number
        })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def get_order_detail(request, order_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'GET':
        order = get_object_or_404(models.Order, id=order_id, ordered_by=request.user)
        items_data = []
        for item in order.items.all():
            item_data = {
                'item_id': item.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'status': item.status,
                'price': float(item.get_cost()),
            }
            items_data.append(item_data)

        order_data = {
            'id': order.id,
            'status': order.status,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'total_price': float(order.get_total_price()),
            'items': items_data
        }
        return JsonResponse(order_data)
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def add_order_item(request, order_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        order = get_object_or_404(models.Order, id=order_id, ordered_by=request.user)
        if not order:
            return JsonResponse({
                'message': f"Order with {order_id} does not exsists or does not belong to you. "
            }, status=400)
        form = forms.OrderedItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            item.fetch_price() 
            return JsonResponse({
                'message': f"Item added Successfully to order {order_id}",
                'item_id': item.id,
                'product_id': item.product_id,
                'quantity': item.quantity,
                'status': item.status,
                'price': float(item.get_cost())
            })
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def get_order_total(request, order_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'GET':
        order = get_object_or_404(models.Order, id=order_id, ordered_by=request.user)
        total = order.get_total_price()
        return JsonResponse({
            'order_id': order_id,
            'total_price': float(total),
            'item_count': order.items.count()
        })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def update_order_item(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'PUT':
        item = get_object_or_404(models.OrderedItem, id=item_id, order__ordered_by=request.user)
        if not item:
            JsonResponse({
                'message': f"Item with {item_id} does not exsists"
            })
        data = json.loads(request.body)
        form = forms.OrderedItemForm(data, instance=item)
        if form.is_valid():
            updated_item = form.save()
            return JsonResponse({
                'message': "Item updated Successfully",
                'item_id': updated_item.id,
                'product_id': updated_item.product_id,
                'quantity': updated_item.quantity,
                'status': updated_item.status,
                'price': float(updated_item.get_cost())
            })
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)

