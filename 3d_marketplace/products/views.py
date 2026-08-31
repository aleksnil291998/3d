from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def catalog(request):
    """Каталог товаров"""
    products = Product.objects.filter(is_active=True).select_related('seller', 'category')
    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    
    # Фильтры
    product_type = request.GET.get('type')
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if product_type:
        products = products.filter(product_type=product_type)
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    products = products.order_by(sort_by)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/catalog.html', context)


def product_detail(request, pk):
    """Детальная страница товара"""
    product = get_object_or_404(Product.objects.select_related('seller', 'category'), pk=pk)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/detail.html', context)


def category_products(request, slug):
    """Товары категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/catalog.html', context)
