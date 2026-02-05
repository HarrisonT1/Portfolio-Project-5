from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory
from .webhooks import webhook


urlpatterns = [
    path('', views.checkout, name="checkout"),
    path('success/<str:order_number>', views.checkout_success, name="checkout_success"),
    path('wh/', webhook, name='webhook')
]
