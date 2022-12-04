from django.urls import path
from . import views as user_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_view.register, name='register'),
    path('this_page_not_for_you/', user_view.this_page_not_for_you, name='this_page_not_for_you'),
    
    path('lengkapi_profile/<str:username>/', user_view.lengkapi_profile, name='lengkapi_profile'),
    path('edit_profile/<slug:profile_slug>/', user_view.edit_profile, name='edit_profile'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('about/', user_view.about, name='about-page'),
    path('profile/<slug:slug>/', user_view.profile, name='profile'), 
    path('change_password/', user_view.change_password, name='change_password'),

]
