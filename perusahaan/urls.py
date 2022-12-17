from django.urls import path
from . import views as perusahaan_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', perusahaan_view.home, name='home'),
    path('tambah_perusahaan/', perusahaan_view.tambah_perusahaan, name='tambah_perusahaan'),
    path('data_perusahaan/', perusahaan_view.data_perusahaan, name='data_perusahaan'),
    path('detail_perusahaan/<slug:slug>/', perusahaan_view.detail_perusahaan, name='detail_perusahaan'),
    path('edit_perusahaan/<slug:slug>/', perusahaan_view.edit_perusahaan, name='edit_perusahaan'),
    path('<slug:slug>/', perusahaan_view.home_perusahaan, name='home_perusahaan'),
]






