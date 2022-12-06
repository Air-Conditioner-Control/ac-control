from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json
from django.http import HttpResponse
import csv
import numpy as np
from .froms import TeknisiCreationForm
from .models import DataTeknisi
from users.models import Profile
from django.shortcuts import get_object_or_404

def is_user_exist(username):
	while True:
		is_user = User.objects.filter(username=username)
		if is_user:
			username = username + str(np.random.random_integers(10))
		else:
			break
	return username


@login_required
def create_teknisi(request):
	if request.method == 'POST':
		form = TeknisiCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			email = form.cleaned_data.get('email')
			username = is_user_exist(username)
			user = User.objects.create_user(
				username=username,
				password=password,
				email=email
				)
			user.save()
			# Creating profile
			# Profile otomatis tercreate karena adanya signal
			profile = get_object_or_404(Profile, user=user)
			profile.user_type = 'TEKNISI'
			profile.save()

			# Simpan data
			data_teknisi = DataTeknisi(user=user, username=username, password=password)
			data_teknisi.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil daftar!')

			return redirect('daftar_teknisi')
		else:
			return render(request, 'teknisi/create_teknisi.html', {'form': form})		
	else:
		form = TeknisiCreationForm()
	return render(request, 'teknisi/create_teknisi.html', {'form': form})


@login_required
def daftar_teknisi(request):
	if request.user.profile.user_type == 'ADMIN':
		teknisi = reversed(DataTeknisi.objects.all())
		context = {
			"teknisi": teknisi
		}
		return render(request, 'teknisi/daftar_teknisi.html', context)
	else:
		return render(request, 'users/this_page_not_for_you.html')


@login_required
def jadikan_admin(request, slug):
	'''Teknisi slug'''
	if request.user.profile.user_type == 'ADMIN':
		teknisi_i = get_object_or_404(DataTeknisi, slug=slug)
		profile_teknisi = teknisi_i.user.profile
		if profile_teknisi.user_type == 'ADMIN':
			profile_teknisi.user_type = 'TEKNISI'
		else:
			profile_teknisi.user_type = 'ADMIN'
		profile_teknisi.save()
		
		return redirect('daftar_teknisi')
	else:
		return render(request, 'users/this_page_not_for_you.html')



