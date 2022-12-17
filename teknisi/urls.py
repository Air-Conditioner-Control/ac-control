from django.urls import path
from . import views as teknisi_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('create_teknisi/<slug:slug>/', teknisi_view.create_teknisi, name='create_teknisi'),
    path('daftar_teknisi/<slug:slug>/', teknisi_view.daftar_teknisi, name='daftar_teknisi'),
    path('jadikan_admin/<slug:slug>/', teknisi_view.jadikan_admin, name='jadikan_admin'),
    path('delet_teknisi/<slug:slug>/', teknisi_view.delet_teknisi, name='delet_teknisi'),
]






