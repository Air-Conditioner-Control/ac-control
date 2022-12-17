from django.urls import path
from . import views as home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home_view.superadmin, name='superadmin'),
]
