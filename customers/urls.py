from django.urls import path
from . import views as customer_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('daftarkan_customer/', customer_view.daftarkan_customer, name='daftarkan_customer'),
    path('daftar_customer/', customer_view.daftar_customer, name='daftar_customer'),
    path('detail_customer/<slug:slug>/', customer_view.detail_customer, name='detail_customer'),
    path('edit_data_customer/<slug:slug>/', customer_view.edit_data_customer, name='edit_data_customer'),
    path('tambah_ac/<slug:slug>/', customer_view.tambah_ac, name='tambah_ac'),
    path('detail_ac/<slug:slug>/', customer_view.detail_ac, name='detail_ac'),
    path('edit_data_ac/<slug:slug>/', customer_view.edit_data_ac, name='edit_data_ac'),
    path('tambah_riwayat_penanganan/<slug:slug>/', customer_view.tambah_riwayat_penanganan, name='tambah_riwayat_penanganan'),
    path('data_ac/', customer_view.data_ac, name='data_ac'),
    path('detail_riwayat_penanganan/<slug:slug>/', customer_view.detail_riwayat_penanganan, name='detail_riwayat_penanganan'),
    path('edit_riwayat_penanganan_ac/<slug:slug>/', customer_view.edit_riwayat_penanganan_ac, name='edit_riwayat_penanganan_ac'),
    path('tambah_data_belanja/<slug:slug>/', customer_view.tambah_data_belanja, name='tambah_data_belanja'),
    path('edit_data_belanja/<slug:slug>/', customer_view.edit_data_belanja, name='edit_data_belanja'),
    path('data_belanja/<slug:slug>/', customer_view.data_belanja, name='data_belanja'),
    path('tambah_data_trouble_shooting/<slug:slug>/', customer_view.tambah_data_trouble_shooting, name='tambah_data_trouble_shooting'),
    path('edit_data_trouble_shooting/<slug:slug>/', customer_view.edit_data_trouble_shooting, name='edit_data_trouble_shooting'),
    path('data_trouble_shooting/<slug:slug>/', customer_view.data_trouble_shooting, name='data_trouble_shooting'),
]






