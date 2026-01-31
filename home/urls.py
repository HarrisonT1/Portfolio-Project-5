from django.urls import path  # import path, similar to project's urls.py
from . import views  # import views.py from the current directory


urlpatterns = [
    path('', views.home, name="home"),

]
