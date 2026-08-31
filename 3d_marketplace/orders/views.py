from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


def get_or_create_cart(request):
    """Получить или создать корзину"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        # Для неавторизованных пользователей можно использовать сессию
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
            if not cart:
                # Создаем корзину без пользователя для гостя
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            # Создаем корзину без пользователя для гостя
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart


def cart_view(request):
    """Корзина покупок"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f'{product.title} добавлен в корзину')
    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.info(request, 'Товар удален из корзины')
    return redirect('orders:cart')


@login_required
def checkout(request):
    """Оформление заказа"""
    cart = get_or_create_cart(request)
    items = cart.items.select_related('product').all()
    
    if not items:
        messages.warning(request, 'Корзина пуста')
        return redirect('products:catalog')
    
    if request.method == 'POST':
        # Создание заказа
        order = Order.objects.create(
            user=request.user,
            delivery_address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            postal_code=request.POST.get('postal_code', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', request.user.email),
            subtotal=cart.total_amount,
            shipping_cost=0,  # Можно добавить расчет доставки
            discount=0,
            total=cart.total_amount,
            notes=request.POST.get('notes', '')
        )
        
        # Перенос элементов корзины в заказ
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total=item.total
            )
            # Уменьшаем остаток на складе
            if item.product.product_type != 'service':
                item.product.stock -= item.quantity
                item.product.save()
        
        # Очистка корзины
        cart.items.all().delete()
        
        messages.success(request, f'Заказ №{order.order_number} успешно оформлен!')
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'items': items,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def my_orders(request):
    """Мои заказы"""
    orders = request.user.orders.all().order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/my_orders.html', context)


@login_required
def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/order_detail.html', context)
