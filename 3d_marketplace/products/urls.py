from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('category/<slug:slug>/', views.category_products, name='category'),
]
