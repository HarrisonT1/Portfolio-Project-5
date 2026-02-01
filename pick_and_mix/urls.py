from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.pick_and_mix, name="pick_and_mix"),
    path('products/<slug:slug>', views.pick_and_mix_products, name="pick_and_mix_products"),
    path('products/<slug:bag_slug>/add/<slug:product_slug>', views.pick_and_mix_add, name="pick_and_mix_add"),
]
