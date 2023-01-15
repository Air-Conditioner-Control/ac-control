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
from django.db.models import Q
from customers.models import DataCustomers


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
	customers = DataCustomers.objects.filter(perusahaan=perusahaan)
	
	layanan = LayananKami.objects.filter(perusahaan=perusahaan)
	testimoni = Testimoni.objects.filter(perusahaan=perusahaan)

	context = {
		'perusahaan': perusahaan,
		'teknisi': teknisi,
		'customers': customers,
		'layanan': layanan,
		'testimoni': testimoni
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


@login_required
def data_perusahaan(request):
	'''If user SUPER ADMIN'''
	if request.user.profile.user_type == 'SUPERADMIN':
		data = list(reversed(Perusahaan.objects.all().order_by('date_created')))
		context = {
			'data': data,
		}
		return render(request, 'perusahaan/data_perusahaan.html', context)
	else:
		return redirect('this_page_not_for_you')

@login_required
def detail_perusahaan(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	teknisi_i = get_object_or_404(DataTeknisi, perusahaan=perusahaan, user=request.user)

	if teknisi_i.user_type in ['SUPERADMIN', 'ADMIN']:

		layanan = LayananKami.objects.filter(perusahaan=perusahaan)
		testimoni = Testimoni.objects.filter(perusahaan=perusahaan)

		if teknisi_i.user_type != 'SUPERADMIN':
			teknisi = reversed(DataTeknisi.objects.filter(~Q(user_type='SUPERADMIN'), perusahaan=perusahaan))
		else:
			teknisi = reversed(DataTeknisi.objects.filter(perusahaan=perusahaan))

		context = {
			'perusahaan': perusahaan,
			'teknisi': teknisi,
			'teknisi_i': teknisi_i,
			'layanan': layanan,
			'testimoni': testimoni
		}
		return render(request, 'perusahaan/detail_perusahaan.html', context)
	else:
		return redirect('this_page_not_for_you')

# XXXXXXXXXXXXXXX
@login_required
def tambah_layanan(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)

	if request.method == 'POST':
		form = LayananKamiForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.perusahaan = perusahaan
			obj.save()

			return redirect('detail_perusahaan', slug=perusahaan.slug)
		else:
			return render(request, 'perusahaan/tambah_layanan.html', {'form': form, 'perusahaan': obj})		
	else:
		form = LayananKamiForm()
	return render(request, 'perusahaan/tambah_layanan.html', {'form': form})


@login_required
def edit_layanan(request, slug):
	instance = get_object_or_404(LayananKami, slug=slug)
	if request.method == 'POST':
		form = LayananKamiForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			return redirect('detail_perusahaan', slug=instance.perusahaan.slug)
		else:
			return render(request, 'perusahaan/edit_layanan.html', {'form': form, 'perusahaan': instance})		
	else:
		form = LayananKamiForm(instance=instance)
	return render(request, 'perusahaan/edit_layanan.html', {'form': form, 'perusahaan': instance})


@login_required
def delet_layanan(request, slug):
	layanan = get_object_or_404(LayananKami, slug=slug)
	perusahaan = layanan.perusahaan
	teknisi_i = get_object_or_404(DataTeknisi, perusahaan=perusahaan, user=request.user)

	if teknisi_i.user_type in ['ADMIN', 'SUPERADMIN']:
		layanan.delete()
		return redirect('detail_perusahaan', slug=perusahaan.slug)
	else:
		return redirect('this_page_not_for_you')


@login_required
def tambah_testimoni(request,slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)

	if request.method == 'POST':
		form = TestimoniForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.perusahaan = perusahaan
			obj.save()

			return redirect('detail_perusahaan', slug=perusahaan.slug)
		else:
			return render(request, 'perusahaan/tambah_testimoni.html', {'form': form, 'perusahaan': obj})		
	else:
		form = TestimoniForm()
	return render(request, 'perusahaan/tambah_testimoni.html', {'form': form})


@login_required
def edit_testimoni(request, slug):
	instance = get_object_or_404(Testimoni, slug=slug)
	if request.method == 'POST':
		form = TestimoniForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			return redirect('detail_perusahaan', slug=instance.perusahaan.slug)
		else:
			return render(request, 'perusahaan/edit_testimoni.html', {'form': form, 'perusahaan': instance})		
	else:
		form = TestimoniForm(instance=instance)
	return render(request, 'perusahaan/edit_testimoni.html', {'form': form, 'perusahaan': instance})


@login_required
def delet_testimoni(request, slug):
	testimoni = get_object_or_404(Testimoni, slug=slug)
	perusahaan = testimoni.perusahaan
	teknisi_i = get_object_or_404(DataTeknisi, perusahaan=perusahaan, user=request.user)

	if teknisi_i.user_type in ['ADMIN', 'SUPERADMIN']:
		testimoni.delete()
		return redirect('detail_perusahaan', slug=perusahaan.slug)
	else:
		return redirect('this_page_not_for_you')


