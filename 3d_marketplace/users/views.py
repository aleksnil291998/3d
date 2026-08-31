from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, SellerProfile, CustomerProfile


def login_view(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'users/login.html')


def register_view(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        user_type = request.POST.get('user_type', 'customer')
        
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'users/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            user_type=user_type
        )
        
        # Создаем профиль в зависимости от типа пользователя
        if user_type == 'seller':
            SellerProfile.objects.create(user=user)
        else:
            CustomerProfile.objects.create(user=user)
        
        login(request, user)
        messages.success(request, 'Регистрация успешна! Добро пожаловать!')
        return redirect('core:home')
    
    return render(request, 'users/register.html')


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('core:home')


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/profile.html')


@login_required
def seller_dashboard(request):
    """Кабинет продавца"""
    if not request.user.is_seller:
        messages.error(request, 'Доступ только для продавцов')
        return redirect('core:home')
    
    seller_profile = getattr(request.user, 'seller_profile', None)
    products = request.user.products.all()
    orders = request.user.orders.filter(status__in=['pending', 'confirmed', 'processing'])
    
    context = {
        'seller_profile': seller_profile,
        'products': products,
        'orders': orders,
    }
    return render(request, 'users/seller_dashboard.html', context)
