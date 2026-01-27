from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.all_products, name="products"),
    path('details/<slug:slug>/', views.product_detail, name="product_detail"),
]
