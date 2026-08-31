from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Wishlist, WishlistItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    verbose_name = 'Элемент заказа'
    verbose_name_plural = 'Элементы заказа'
    readonly_fields = ('product', 'quantity', 'price', 'total', 'print_settings', 'custom_notes')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'payment_status', 'total', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__username', 'email')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {'fields': ('order_number', 'user', 'status', 'payment_status')}),
        ('Адрес доставки', {'fields': ('delivery_address', 'city', 'postal_code', 'phone', 'email')}),
        ('Цены', {'fields': ('subtotal', 'shipping_cost', 'discount', 'total')}),
        ('Комментарий', {'fields': ('notes',)}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    actions = ['confirm_order', 'cancel_order', 'mark_as_paid']
    
    def confirm_order(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_order.short_description = "Подтвердить выбранные заказы"
    
    def cancel_order(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_order.short_description = "Отменить выбранные заказы"
    
    def mark_as_paid(self, request, queryset):
        queryset.update(payment_status='paid')
    mark_as_paid.short_description = "Отметить как оплаченные"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total')
    list_filter = ('order__status',)
    search_fields = ('product__title', 'order__order_number')
    ordering = ('-order__created_at',)
    readonly_fields = ('order', 'product', 'quantity', 'price', 'total', 'print_settings', 'custom_notes')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'items_count', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_amount', 'items_count')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__title', 'cart__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('cart', 'product', 'quantity', 'total', 'created_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__title', 'wishlist__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
