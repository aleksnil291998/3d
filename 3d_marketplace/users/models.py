from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользовательская модель с расширенными полями"""
    
    USER_TYPE_CHOICES = (
        ('customer', 'Покупатель'),
        ('seller', 'Продавец'),
        ('admin', 'Администратор'),
    )
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name='Тип пользователя'
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_seller(self):
        return self.user_type == 'seller' or self.user_type == 'admin'
    
    @property
    def is_customer(self):
        return self.user_type == 'customer'


class SellerProfile(models.Model):
    """Профиль продавца"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile', verbose_name='Пользователь')
    company_name = models.CharField(max_length=255, blank=True, verbose_name='Название компании')
    inn = models.CharField(max_length=20, blank=True, verbose_name='ИНН')
    ogrn = models.CharField(max_length=20, blank=True, verbose_name='ОГРН')
    description = models.TextField(blank=True, verbose_name='Описание')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Рейтинг')
    reviews_count = models.PositiveIntegerField(default=0, verbose_name='Количество отзывов')
    is_verified = models.BooleanField(default=False, verbose_name='Проверенный продавец')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Профиль продавца'
        verbose_name_plural = 'Профили продавцов'
        ordering = ['-rating', '-created_at']
    
    def __str__(self):
        return f"{self.company_name or self.user.username}"


class CustomerProfile(models.Model):
    """Профиль покупателя"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', verbose_name='Пользователь')
    address = models.TextField(blank=True, verbose_name='Адрес доставки')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Почтовый индекс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Профиль покупателя'
        verbose_name_plural = 'Профили покупателей'
    
    def __str__(self):
        return f"{self.user.username}"
