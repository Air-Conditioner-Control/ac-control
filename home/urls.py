from django.urls import path
from . import views as home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view.superadmin, name='superadmin'),
    path('dk-883783-03984783-93749/', home_view.dk, name='dk'),
]
