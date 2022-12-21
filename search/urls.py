from django.urls import path
from . import views as search_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('ac_search/<str:query>/<slug:slug>/', search_view.ac_search, name='ac_search'),
]






