from django.db import models
from django.conf import settings


class Category(models.Model):
    """Категории товаров и услуг"""
    
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Иконка')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительская категория')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['parent__name', 'name']
    
    def __str__(self):
        return self.name
    
    def get_children(self):
        return self.children.filter(is_active=True)


class Product(models.Model):
    """Товар/Услуга"""
    
    PRODUCT_TYPE_CHOICES = (
        ('product', 'Товар'),
        ('service', 'Услуга'),
        ('model', '3D Модель'),
        ('filament', 'Филамент'),
        ('printer', '3D Принтер'),
        ('part', 'Запчасть'),
        ('printed_item', 'Готовое изделие'),
    )
    
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', verbose_name='Продавец')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name='Категория')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='product', verbose_name='Тип')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Старая цена')
    stock = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    
    # Специфичные поля для 3D печати
    material = models.CharField(max_length=255, blank=True, verbose_name='Материал')
    color = models.CharField(max_length=100, blank=True, verbose_name='Цвет')
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Вес (г)')
    dimensions = models.CharField(max_length=100, blank=True, verbose_name='Габариты (ДхШхВ)')
    print_volume = models.CharField(max_length=100, blank=True, verbose_name='Область печати')
    layer_height = models.CharField(max_length=50, blank=True, verbose_name='Толщина слоя')
    filament_diameter = models.CharField(max_length=50, blank=True, verbose_name='Диаметр филамента')
    
    # Файлы для 3D моделей
    model_file = models.FileField(upload_to='models/', blank=True, null=True, verbose_name='Файл модели')
    file_format = models.CharField(max_length=20, blank=True, verbose_name='Формат файла (STL, OBJ, etc)')
    
    product_images = models.ManyToManyField('ProductImage', blank=True, related_name='product_items', verbose_name='Изображения')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Рейтинг')
    reviews_count = models.PositiveIntegerField(default=0, verbose_name='Количество отзывов')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемый')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.seller.username})"
    
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        return self.stock > 0 or self.product_type == 'service'


class ProductImage(models.Model):
    """Изображения товара"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['-is_main', '-created_at']
    
    def __str__(self):
        return f"Изображение для {self.product.title}"
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)


class Review(models.Model):
    """Отзывы о товарах"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField(verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.title}"
