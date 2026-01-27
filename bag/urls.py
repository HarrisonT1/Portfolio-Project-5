from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.view_bag, name="view_bag"),
    path('add_to_bag/<slug:slug>/', views.add_to_bag, name="add_to_bag"),
]
