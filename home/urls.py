# Standard libary imports
# Third-party imports
# Django imports
from django.urls import path  # import path, similar to project's urls.py
# Local imports
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.home, name="home"),
    path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
]
