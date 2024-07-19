from django.urls import path
from product_manage import views

urlpatterns = [
    path('create/', views.create, name='create_product'),
    path('edit/<int:pk>/', views.edit, name='edit_product'),
    path('details/<int:pk>/', views.details, name='product_details'),
    path('user_products/<int:page>/', views.user_products, name='user_products'),
    path('all_products/<int:page>/', views.all_products, name='all_products'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('product_status/<int:pk>/', views.product_status, name='product_status'),
    path('price/<int:product_id>/', views.get_price, name='get_price'),
]