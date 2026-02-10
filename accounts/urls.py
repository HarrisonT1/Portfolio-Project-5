from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.view_account, name="profile"),
    path('order_detail/<order_number>', views.order_detail, name="order_detail"),
]
