from django.contrib import admin
from .models import User, SellerProfile, CustomerProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'phone', 'created_at', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('email', 'phone', 'avatar')}),
        ('Тип пользователя', {'fields': ('user_type',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'rating', 'reviews_count', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('company_name', 'user__username', 'inn')
    ordering = ('-rating', '-created_at')
    fieldsets = (
        (None, {'fields': ('user', 'company_name')}),
        ('Реквизиты', {'fields': ('inn', 'ogrn')}),
        ('Информация', {'fields': ('description',)}),
        ('Рейтинг', {'fields': ('rating', 'reviews_count', 'is_verified')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'postal_code', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('user__username', 'city')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Адрес', {'fields': ('address', 'city', 'postal_code')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
