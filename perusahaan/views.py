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
from .forms import *
from .models import *
from teknisi.models import DataTeknisi
from django.shortcuts import get_object_or_404


def home(request):
	if request.user.is_authenticated:
		if request.user.profile.user_type == 'SUPERADMIN':
			return redirect('data_perusahaan')
		else:
			# Teknisi type
			teknisis = DataTeknisi.objects.filter(user=request.user)
			if teknisis:
				teknisi = teknisis[0]
				perusahaan = teknisi.perusahaan
				return redirect('home_perusahaan', slug=perusahaan.slug)
			else:
				return redirect('this_page_not_for_you')
	else:
		return redirect('login')


def home_perusahaan(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	teknisi = get_object_or_404(DataTeknisi, user=request.user, perusahaan=perusahaan)
	context = {
		'perusahaan': perusahaan,
		'teknisi': teknisi
	}
	return render(request, 'perusahaan/home_perusahaan.html', context)



@login_required
def tambah_perusahaan(request):
	'''If user SUPER ADMIN'''

	if request.method == 'POST':
		form = PerusahaanForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			name = form.cleaned_data.get('name')
			obj.save()

			# Creating super admin
			superadmin = DataTeknisi(perusahaan=obj, user_type='SUPERADMIN', user=request.user, username="superadmin"+'-'+name, password="superadmin"+'-'+name)
			# superadmin = AnggotaPerusahaan(perusahaan=obj, user_type='SUPERADMIN', user=request.user)
			superadmin.save()

			return redirect('home_perusahaan', slug=obj.slug)
			# return redirect('data_perusahaan')
		else:
			return render(request, 'perusahaan/tambah_perusahaan.html', {'form': form, 'perusahaan': obj})		
	else:
		form = PerusahaanForm()
	return render(request, 'perusahaan/tambah_perusahaan.html', {'form': form})


@login_required
def edit_perusahaan(request, slug):
	instance = get_object_or_404(Perusahaan, slug=slug)
	if request.method == 'POST':
		form = PerusahaanForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			return redirect('detail_perusahaan', slug=instance.slug)
		else:
			return render(request, 'perusahaan/edit_perusahaan.html', {'form': form, 'perusahaan': instance})		
	else:
		form = PerusahaanForm(instance=instance)
	return render(request, 'perusahaan/edit_perusahaan.html', {'form': form, 'perusahaan': instance})



def data_perusahaan(request):
	'''If user SUPER ADMIN'''
	data = list(reversed(Perusahaan.objects.all().order_by('date_created')))
	context = {
		'data': data,
	}
	return render(request, 'perusahaan/data_perusahaan.html', context)


@login_required
def detail_perusahaan(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	teknisi = reversed(DataTeknisi.objects.filter(perusahaan=perusahaan))
	
	context = {
		'perusahaan': perusahaan,
		'teknisi': teknisi
	}
	return render(request, 'perusahaan/detail_perusahaan.html', context)



