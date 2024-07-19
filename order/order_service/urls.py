from django.urls import path
from order_service import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('get_orders/', views.get_orders, name='get_orders'),
    path('<int:order_id>/', views.get_order_detail, name='get_order_detail'),
    path('<int:order_id>/total/', views.get_order_total, name='get_order_total'),
    path('<int:order_id>/add_item/', views.add_order_item, name='add_order_item'),
    path('item/<int:item_id>/update/', views.update_order_item, name='update_order_item'),
]