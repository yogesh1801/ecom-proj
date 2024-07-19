from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from product_manage import forms, models
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.serializers import serialize
import json
from celery.result import AsyncResult

# Create your views here.

@csrf_exempt
def create(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        form = forms.ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return JsonResponse({
                'message': f"product created with id: {product.id}"
            }, status=200)
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
def edit(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        product = get_object_or_404(models.Product, pk=pk, created_by=request.user)
        if product:
            form = forms.ProductForm(request.POST, instance=product)
            if form.is_valid():
                return JsonResponse({
                    'message': "Product details updated successfully."
                }, status=201)
            else:
                return JsonResponse({
                    'message': "Please Fill all the required fields correctly",
                    'error': form.errors
                }, status=400)
        else:
            return JsonResponse({
                'message': "The product either does not exsists or does not belong to you"
            }, status=400)
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def details(request, pk):
    if request.method == 'GET':
        product = get_object_or_404(models.Product, pk=pk)
        if product:
            return JsonResponse({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'category': product.category,
                'stock': product.stock,
                'created_on': product.created_on,
                'price': product.price,
                'is_active': product.is_active, 
            })
        else:
            return JsonResponse({
                'message': "Product with this id does not exsist."
            })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)
        

@csrf_exempt
def user_products(request, page):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'GET':
        products = models.Product.objects.filter(created_by=request.user).order_by('-created_on')
        if products:
            paginator = Paginator(products, 10)
            page_obj = paginator.get_page(page)
            products_data = json.loads(serialize('json', page_obj.object_list))
            products_list = [item['fields'] for item in products_data]
            for i, item in enumerate(products_data):
                products_list[i]['id'] = item['pk']

            return JsonResponse({
                'products': products_list,
                'page': {
                    'current': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                }
            }, status=200)
        else:
            return JsonResponse({
                'message': "You have not created any products yet, create one"
            })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def all_products(request, page):
    if request.method == 'GET':
        products = models.Product.objects.filter(is_active=True).order_by('-created_on')
        if products:
            paginator = Paginator(products, 10)
            page_obj = paginator.get_page(page)
            products_data = json.loads(serialize('json', page_obj.object_list))
            products_list = [item['fields'] for item in products_data]
            for i, item in enumerate(products_data):
                products_list[i]['id'] = item['pk']

            return JsonResponse({
                    'products': products_list,
                    'page': {
                        'current': page_obj.number,
                        'has_next': page_obj.has_next(),
                        'has_previous': page_obj.has_previous(),
                        'total_pages': paginator.num_pages,
                        'total_items': paginator.count,
                    }
                }, status=200)
        else:
            return JsonResponse({
                'message': "No products listed yet"
            })  
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)

@csrf_exempt
def delete_product(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        product = get_object_or_404(models.Product, pk=pk, created_by=request.user)
        if product:
            product.delete()
            return JsonResponse({
                'message': "Product Deleted Successfully"
            })
        else:
            return JsonResponse({
                'message': "This product does not exsists or does not belong to you"
            })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)


@csrf_exempt
def product_status(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        product = get_object_or_404(models.Product, pk=pk, created_by=request.user)
        if product:
            product.is_active = not product.is_active
            status = product.is_active
            product.save()
            return JsonResponse({
                'message': f"Active status Successfully set to {status}"
            })
        else:
            return JsonResponse({
                'message': "This product does not exsists or does not belong to you"
            })
    else:
        return JsonResponse({
            'message': "Invalid Method"
        }, status=405)
    

@csrf_exempt
def get_price(request, product_id):
    product = get_object_or_404(models.Product, id=product_id)
    return JsonResponse({
        'price': str(product.price)
    })
    
        
    

        
        



