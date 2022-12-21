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
from django.shortcuts import get_object_or_404
from perusahaan.models import Perusahaan
from teknisi.models import DataTeknisi


@login_required
def daftarkan_customer(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	if request.method == 'POST':
		form = DataCustomersForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.perusahaan = perusahaan
			obj.save()

			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan customer!')

			return redirect('daftar_customer', slug=perusahaan.slug)
		else:
			return render(request, 'customers/daftarkan_customer.html', {'form': form})		
	else:
		form = DataCustomersForm()
	return render(request, 'customers/daftarkan_customer.html', {'form': form})


@login_required
def edit_data_customer(request, slug):
	instance = get_object_or_404(DataCustomers, slug=slug)
	if request.method == 'POST':
		form = DataCustomersForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan customer!')

			return redirect('detail_customer', slug=instance.slug)
		else:
			return render(request, 'customers/edit_data_customer.html', {'form': form})		
	else:
		form = DataCustomersForm(instance=instance)
	return render(request, 'customers/edit_data_customer.html', {'form': form})


@login_required
def daftar_customer(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	if request.user.profile.user_type != 'UMUM':
		customers = reversed(DataCustomers.objects.filter(perusahaan=perusahaan))
		context = {
			"customers": customers,
			"perusahaan": perusahaan
		}
		return render(request, 'customers/daftar_customer.html', context)
	else:
		return render(request, 'users/this_page_not_for_you.html')


@login_required
def detail_customer(request, slug):
	customer = get_object_or_404(DataCustomers, slug=slug)
	data_ac = reversed(DataAC.objects.filter(customer=customer))


	context = {
		'customer': customer,
		'data_ac': data_ac,
		'perusahaan': customer.perusahaan
	}

	return render(request, 'customers/detail_customer.html', context)



@login_required
def tambah_ac(request, slug):
	customer = get_object_or_404(DataCustomers, slug=slug)

	if request.method == 'POST':
		form = DataACForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.customer = customer
			obj.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan ac!')

			return redirect('detail_customer', slug=customer.slug)
		else:
			return render(request, 'customers/tambah_ac.html', {'form': form, 'customer': customer})		
	else:
		form = DataACForm()
	return render(request, 'customers/tambah_ac.html', {'form': form, 'customer': customer})


@login_required
def detail_ac(request, slug):
	ac = get_object_or_404(DataAC, slug=slug)
	riwayat_penanganan = reversed(RiwayatPenanganan.objects.filter(ac=ac))
	teknisi = get_object_or_404(DataTeknisi, perusahaan=ac.customer.perusahaan, user=request.user)


	context = {
		'ac': ac,
		'riwayat_penanganan': riwayat_penanganan,
		'teknisi': teknisi
	}

	return render(request, 'customers/detail_ac.html', context)


@login_required
def edit_data_ac(request, slug):
	instance = get_object_or_404(DataAC, slug=slug)
	if request.method == 'POST':
		form = DataACForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil edit data ac!')

			return redirect('detail_ac', slug=instance.slug)
		else:
			return render(request, 'customers/edit_data_ac.html', {'form': form, 'ac': instance})		
	else:
		form = DataACForm(instance=instance)
	return render(request, 'customers/edit_data_ac.html', {'form': form, 'ac': instance})


@login_required
def tambah_riwayat_penanganan(request, slug):
	ac = get_object_or_404(DataAC, slug=slug)

	if request.method == 'POST':
		form = RiwayatPenangananForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.ac = ac
			obj.teknisi = request.user.profile
			obj.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan ac!')

			return redirect('detail_ac', slug=ac.slug)
		else:
			return render(request, 'customers/tambah_riwayat_penanganan.html', {'form': form, 'ac': ac})		
	else:
		form = RiwayatPenangananForm()
	return render(request, 'customers/tambah_riwayat_penanganan.html', {'form': form, 'ac': ac})



def data_ac(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	customer = DataCustomers.objects.filter(perusahaan=perusahaan)
	
	all_ac = list(reversed(DataAC.objects.filter(customer__in=customer).order_by('date_created')))
	# all_ac = list(reversed(DataAC.objects.all().order_by('date_created')))
	context = {
		'all_ac': all_ac,
		'query': 'NONE'
	}
	return render(request, 'customers/data_ac.html', context)


@login_required
def detail_riwayat_penanganan(request, slug):
	penanganan = get_object_or_404(RiwayatPenanganan, slug=slug)
	belanja = DataBelanja.objects.filter(riwayat_penanganan=penanganan)
	
	context = {
		'penanganan': penanganan,
		'belanja': belanja
	}

	return render(request, 'customers/detail_riwayat_penanganan.html', context)


@login_required
def edit_riwayat_penanganan_ac(request, slug):
	instance = get_object_or_404(RiwayatPenanganan, slug=slug)
	if request.method == 'POST':
		form = RiwayatPenangananForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil edit data riwayat penanganan ac!')

			return redirect('detail_riwayat_penanganan', slug=instance.slug)
		else:
			return render(request, 'customers/edit_riwayat_penanganan_ac.html', {'form': form, 'riwayat': instance})		
	else:
		form = RiwayatPenangananForm(instance=instance)
	return render(request, 'customers/edit_riwayat_penanganan_ac.html', {'form': form, 'riwayat': instance})



@login_required
def tambah_data_belanja(request, slug):
	instance = get_object_or_404(RiwayatPenanganan, slug=slug)

	if request.method == 'POST':
		form = DataBelanjaForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.riwayat_penanganan = instance
			obj.teknisi = request.user.profile
			obj.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan ac!')

			return redirect('data_belanja', slug=instance.slug)
		else:
			return render(request, 'customers/tambah_data_belanja.html', {'form': form, 'penanganan': instance})		
	else:
		form = DataBelanjaForm()
	return render(request, 'customers/tambah_data_belanja.html', {'form': form, 'penanganan': instance})


@login_required
def edit_data_belanja(request, slug):
	instance = get_object_or_404(DataBelanja, slug=slug)
	if request.method == 'POST':
		form = DataBelanjaForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil edit data belanja penanganan ac!')

			return redirect('detail_riwayat_penanganan', slug=instance.riwayat_penanganan.slug)
		else:
			return render(request, 'customers/edit_data_belanja.html', {'form': form, 'riwayat': instance})		
	else:
		form = DataBelanjaForm(instance=instance)
	return render(request, 'customers/edit_data_belanja.html', {'form': form, 'riwayat': instance})



def data_belanja(request, slug):
	'''Slug riwayat'''
	riwayat_penanganan = get_object_or_404(RiwayatPenanganan, slug=slug)
	data = list(reversed(DataBelanja.objects.filter(riwayat_penanganan=riwayat_penanganan).order_by('date_created')))
	teknisi = get_object_or_404(DataTeknisi, perusahaan=riwayat_penanganan.ac.customer.perusahaan, user=request.user)
	context = {
		'data': data,
		'penanganan': riwayat_penanganan,
		'teknisi': teknisi
	}
	return render(request, 'customers/data_belanja.html', context)


@login_required
def all_data_belanja(request, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)
	customers = DataCustomers.objects.filter(perusahaan=perusahaan)
	all_ac = DataAC.objects.filter(customer__in=customers)

	riwayat_penanganan = RiwayatPenanganan.objects.filter(ac__in=all_ac)
	data = list(reversed(DataBelanja.objects.filter(riwayat_penanganan__in=riwayat_penanganan).order_by('date_created')))
	teknisi = get_object_or_404(DataTeknisi, perusahaan=perusahaan, user=request.user)
	context = {
		'data': data,
		'penanganan': riwayat_penanganan,
		'teknisi': teknisi,
		'perusahaan': perusahaan
	}
	return render(request, 'customers/all_data_belanja.html', context)
	



@login_required
def tambah_data_trouble_shooting(request, slug):
	instance = get_object_or_404(RiwayatPenanganan, slug=slug)

	if request.method == 'POST':
		form = TroubleShootingForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.riwayat_penanganan = instance
			obj.teknisi = request.user.profile
			obj.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan ac!')

			return redirect('data_trouble_shooting', slug=instance.slug)
		else:
			return render(request, 'customers/tambah_data_trouble_shooting.html', {'form': form, 'penanganan': instance})		
	else:
		form = TroubleShootingForm()
	return render(request, 'customers/tambah_data_trouble_shooting.html', {'form': form, 'penanganan': instance})


@login_required
def edit_data_trouble_shooting(request, slug):
	instance = get_object_or_404(TroubleShooting, slug=slug)
	if request.method == 'POST':
		form = TroubleShootingForm(request.POST, request.FILES, instance=instance)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil edit data belanja penanganan ac!')

			return redirect('data_trouble_shooting', slug=instance.riwayat_penanganan.slug)
		else:
			return render(request, 'customers/edit_data_trouble_shooting.html', {'form': form, 'penanganan': instance})		
	else:
		form = TroubleShootingForm(instance=instance)
	return render(request, 'customers/edit_data_trouble_shooting.html', {'form': form, 'penanganan': instance})



def data_trouble_shooting(request, slug):
	'''Slug riwayat'''
	riwayat_penanganan = get_object_or_404(RiwayatPenanganan, slug=slug)
	data = list(reversed(TroubleShooting.objects.filter(riwayat_penanganan=riwayat_penanganan).order_by('date_created')))
	teknisi = get_object_or_404(DataTeknisi, perusahaan=riwayat_penanganan.ac.customer.perusahaan, user=request.user)
	context = {
		'data': data,
		'penanganan': riwayat_penanganan,
		'teknisi': teknisi
	}
	return render(request, 'customers/data_trouble_shooting.html', context)




