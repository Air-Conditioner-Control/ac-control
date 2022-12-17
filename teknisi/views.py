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
from perusahaan.models import Perusahaan
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.db.models import Q


def is_user_exist(username):
	while True:
		is_user = User.objects.filter(username=username)
		if is_user:
			username = username + str(np.random.random_integers(10))
		else:
			break
	return username


@login_required
def create_teknisi(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
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
			profile.full_name = username
			profile.save()

			# Simpan data
			data_teknisi = DataTeknisi(user=user, username=username, password=password, perusahaan=perusahaan, user_type='TEKNISI')
			data_teknisi.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil daftar!')
			if request.user.profile.user_type == 'SUPERADMIN':
				return redirect('detail_perusahaan', slug=perusahaan.slug) 
			else:
				return redirect('daftar_teknisi', slug=perusahaan.slug)
		else:
			return render(request, 'teknisi/create_teknisi.html', {'form': form})		
	else:
		form = TeknisiCreationForm()
	return render(request, 'teknisi/create_teknisi.html', {'form': form})


@login_required
def daftar_teknisi(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	teknisi_i = get_object_or_404(DataTeknisi, perusahaan=perusahaan, user=request.user)

	if teknisi_i.user_type in ['ADMIN', 'SUPERADMIN']:
		teknisi = reversed(DataTeknisi.objects.filter( ~Q(user_type='SUPERADMIN'), perusahaan=perusahaan))
		
		context = {
			"teknisi": teknisi,
			"teknisi_i": teknisi_i
		}
		return render(request, 'teknisi/daftar_teknisi.html', context)
	else:
		return render(request, 'users/this_page_not_for_you.html')


@login_required
def jadikan_admin(request, slug):
	'''Teknisi slug'''
	teknisi_i = get_object_or_404(DataTeknisi, slug=slug)
	admin = get_object_or_404(DataTeknisi, user=request.user, perusahaan=teknisi_i.perusahaan)
	if (request.user.profile.user_type in ['ADMIN', 'SUPERADMIN']) or (admin.user_type in ['ADMIN', 'SUPERADMIN']):
		
		if teknisi_i.user_type == 'ADMIN':
			teknisi_i.user_type = 'TEKNISI'
		elif teknisi_i.user_type == 'SUPERADMIN':
			pass
		else:
			teknisi_i.user_type = 'ADMIN'
		teknisi_i.save()
		
		if request.user.profile.user_type == 'SUPERADMIN':
			return redirect('detail_perusahaan', slug=teknisi_i.perusahaan.slug)
		else:
			return redirect('daftar_teknisi', slug=teknisi_i.perusahaan.slug)
	else:
		return render(request, 'users/this_page_not_for_you.html')


@login_required
def delet_teknisi(request, slug):
	'''Teknisi slug'''
	teknisi_i = get_object_or_404(DataTeknisi, slug=slug)
	admin = get_object_or_404(DataTeknisi, user=request.user, perusahaan=teknisi_i.perusahaan)

	# if request.user.profile.user_type in ['ADMIN', 'SUPERADMIN']:
	if (request.user.profile.user_type in ['ADMIN', 'SUPERADMIN']) or (admin.user_type in ['ADMIN', 'SUPERADMIN']):
		
		perusahaan = teknisi_i.perusahaan
		profile = teknisi_i.user.profile
		teknisi_i.delete()
		profile.user_type = 'UMUM'
		profile.save()
		
		if request.user.profile.user_type == 'SUPERADMIN':
			return redirect('detail_perusahaan', slug=teknisi_i.perusahaan.slug)
		else:
			return redirect('daftar_teknisi', slug=perusahaan.slug)
	else:
		return render(request, 'users/this_page_not_for_you.html')




