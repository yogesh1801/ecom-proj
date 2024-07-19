from django.urls import path, include
from auth_service import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
]