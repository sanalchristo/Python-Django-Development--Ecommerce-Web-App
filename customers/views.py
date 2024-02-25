from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import Customer
from django.contrib import messages
# Create your views here.

def sign_out(request):
    logout(request)
    return redirect('home')

def show_account(request):
    context={}
    if request.POST and 'register' in request.POST:
        context['register']=True
        try:
            username= request.POST.get('username')
            password= request.POST.get('password')
            email= request.POST.get('email')
            address= request.POST.get('address')
            phone= request.POST.get('phone')
            # creates user account
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            # creates customer account
            customer=Customer.objects.create(
                name=username,
                user=user,
                address=address,
                phone=phone,
            )
            success_message="User registered successfully"
            messages.success(request, success_message)
        except Exception as e:
            error_message="Duplicate username or Invalid inputs"
            messages.error(request, error_message)

    if request.POST and 'login' in request.POST:
        context['register']=False
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid credentials')

    return render(request, 'account.html', context)