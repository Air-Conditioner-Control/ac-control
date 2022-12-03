from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from .models import *
import json



def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			# Flash message
			messages.success(request, f'Anda berhasil daftar!')

			return redirect('login')
		else:
			return render(request, 'users/register.html', {'form': form})		
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form': form})


@login_required
def lengkapi_profile(request, username):
	if request.user.username == username:
		if request.method == 'POST':
			instance = Profile(user=request.user)
			form = LengkapiProfileForm(request.POST, request.FILES, instance=instance)
			if form.is_valid():
				form.save()
				# Flash message
				messages.success(request, f'Profilemu sudah di update')
				# Messages Here
				welcome_message(request)

				return redirect('home')
		else:
			form = LengkapiProfileForm()
		context = {'form': form}
		return render(request, 'users/lengkapi_profile.html', context)
	else:
		return render(request, 'users/this_page_not_for_you.html', {})


@login_required
def this_page_not_for_you(request):
	return render(request, 'users/this_page_not_for_you.html', {})


@login_required
def edit_profile(request, profile_slug):	
	instance = get_object_or_404(Profile, slug=profile_slug)
	if request.method == 'POST':
		form = LengkapiProfileForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			# Flash message
			messages.success(request, f'Profilemu sudah di update')
			return redirect('profile', slug=instance.slug)
	else:
		form = LengkapiProfileForm(instance=instance)
	context = {'form': form}
	return render(request, 'users/edit_profile.html', context)
	


@login_required
def profile(request, slug):
	profile = get_object_or_404(Profile, slug=slug)

	

	if profile.user == request.user:
		is_owner = True
	else:
		is_owner = False

	context = {
		'page_name': 'Profile',
		'profile': profile
	}

	return render(request, 'users/profile.html', context)



@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)

			# Flash message
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'users/change_password.html', {'form': form})



# @login_required
# def pilih_cabor(request, username):
# 	if request.user.username == username:
# 		if request.method == 'POST':
# 			instance = Profile(user=request.user)
# 			form = LengkapiProfileForm(request.POST, request.FILES, instance=instance)
# 			if form.is_valid():
# 				form.save()
# 				# Flash message
# 				messages.success(request, f'Profilemu sudah di update')
# 				return redirect('home_sepakbola')
# 		else:
# 			form = LengkapiProfileForm()
# 		context = {'form': form}
# 		return render(request, 'users/lengkapi_profile.html', context)
# 	else:
# 		return render(request, 'users/this_page_not_for_you.html', {})



def about(request: WSGIRequest):
	return render(request, 'users/about.html', {'page': 'about'})


def this_page_not_for_you(request):
	return render(request, 'users/this_page_not_for_you.html')

