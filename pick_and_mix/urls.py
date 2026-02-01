from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.pick_and_mix, name="pick_and_mix"),
    path('products/', views.pick_and_mix_all_products, name="pick_and_mix_all_products"),
]
