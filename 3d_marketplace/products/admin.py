from django.contrib import admin
from .models import Category, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('parent__name', 'name')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'parent')}),
        ('Описание', {'fields': ('description', 'icon')}),
        ('Статус', {'fields': ('is_active',)}),
        ('Даты', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


class ProductImageInline(admin.TabularInline):
    model = Product.product_images.through
    extra = 1
    verbose_name = 'Изображение'
    verbose_name_plural = 'Изображения'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'product_type', 'price', 'stock', 'rating', 'is_active', 'is_featured', 'created_at')
    list_filter = ('product_type', 'is_active', 'is_featured', 'category', 'created_at')
    search_fields = ('title', 'description', 'sku', 'seller__username')
    prepopulated_fields = {'sku': ('title',)}
    ordering = ('-created_at',)
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {'fields': ('seller', 'category', 'title', 'description')}),
        ('Тип товара', {'fields': ('product_type', 'sku')}),
        ('Цена и наличие', {'fields': ('price', 'old_price', 'stock')}),
        ('Характеристики 3D печати', {
            'fields': ('material', 'color', 'weight', 'dimensions', 'print_volume', 'layer_height', 'filament_diameter'),
            'classes': ('collapse',)
        }),
        ('Файлы', {'fields': ('model_file', 'file_format')}),
        ('Статус', {'fields': ('is_active', 'is_featured')}),
        ('Рейтинг', {'fields': ('rating', 'reviews_count')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'rating', 'reviews_count')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('product__title',)
    ordering = ('-is_main', '-created_at')
    fieldsets = (
        (None, {'fields': ('product', 'image', 'is_main')}),
        ('Даты', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('text', 'user__username', 'product__title')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('product', 'user', 'rating', 'text')}),
        ('Статус', {'fields': ('is_approved',)}),
        ('Даты', {'fields': ('created_at',)}),
    )
    readonly_fields = ('created_at',)
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Одобрить выбранные отзывы"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Снять одобрение с выбранных отзывов"
