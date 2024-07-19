from django.shortcuts import render
from auth_service import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, alogout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            return JsonResponse({
                'message': f"Account Created for {username}" 
            }, status=201)
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)

    else:
        return JsonResponse({
            'message': 'Invalid Method'
        }, status=405)


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({
                    'message': "User Logged in Successfully"
                }, status=200)
            else:
                return JsonResponse({
                    'message': "The user does not exsist or credentials are wrong"
                }, status=400)
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'message': 'Invalid Method'
        }, status=405)


@csrf_exempt
def signout(request):
    if request.method == 'GET':
        alogout(request)
        return JsonResponse({
            'message': "Logged out Successfully"
        },status=200)
    else:
        return JsonResponse({
            'message': 'Invalid Method'
        }, status=405)

@csrf_exempt
def changepassword(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'message': "User is not Logged In please log in"
        }, status=400)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return JsonResponse({
                'message': "Password Changed Successfully"
            }, status=200)
        else:
            return JsonResponse({
                'message': "Please Fill all the required fields correctly",
                'error': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'message': 'Invalid Method'
        }, status=405)
    


