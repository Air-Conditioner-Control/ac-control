from django.urls import path
from . import views as perusahaan_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', perusahaan_view.home, name='home'),
    path('tambah_perusahaan/', perusahaan_view.tambah_perusahaan, name='tambah_perusahaan'),
    path('data_perusahaan/', perusahaan_view.data_perusahaan, name='data_perusahaan'),
    path('detail_perusahaan/<slug:slug>/', perusahaan_view.detail_perusahaan, name='detail_perusahaan'),
    path('edit_perusahaan/<slug:slug>/', perusahaan_view.edit_perusahaan, name='edit_perusahaan'),
    
    path('tambah_layanan/<slug:slug>/', perusahaan_view.tambah_layanan, name='tambah_layanan'),
    path('edit_layanan/<slug:slug>/', perusahaan_view.edit_layanan, name='edit_layanan'),
    path('tambah_testimoni/<slug:slug>/', perusahaan_view.tambah_testimoni, name='tambah_testimoni'),
    path('edit_testimoni/<slug:slug>/', perusahaan_view.edit_testimoni, name='edit_testimoni'),
    path('delet_layanan/<slug:slug>/', perusahaan_view.delet_layanan, name='delet_layanan'),
    path('delet_testimoni/<slug:slug>/', perusahaan_view.delet_testimoni, name='delet_testimoni'),

    path('<slug:slug>/', perusahaan_view.home_perusahaan, name='home_perusahaan'),
]






