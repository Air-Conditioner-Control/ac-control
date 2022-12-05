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
from .forms import DataCustomersForm, DataACForm, RiwayatPenangananForm
from .models import DataCustomers, DataAC, RiwayatPenanganan
from django.shortcuts import get_object_or_404



@login_required
def daftarkan_customer(request):
	if request.method == 'POST':
		form = DataCustomersForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			
			# Flash message
			messages.success(request, f'Anda berhasil mendaftarkan customer!')

			return redirect('daftar_customer')
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
def daftar_customer(request):
	if request.user.profile.user_type != 'UMUM':
		customers = reversed(DataCustomers.objects.all())
		context = {
			"customers": customers
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
		'data_ac': data_ac
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


	context = {
		'ac': ac,
		'riwayat_penanganan': riwayat_penanganan
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



def data_ac(request):
	
	all_ac = list(reversed(DataAC.objects.all().order_by('date_created')))
	context = {
		'all_ac': all_ac,
		'query': 'NONE'
	}
	return render(request, 'customers/data_ac.html', context)


