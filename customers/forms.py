from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DataCustomers, DataAC, RiwayatPenanganan



class DataCustomersForm(forms.ModelForm):

	class Meta:
		model = DataCustomers
		fields = ['nama_lengkap', 'alamat', 'wa_number', 'image']

	def __init__(self, *args, **kwargs):
		super(DataCustomersForm, self).__init__(*args, **kwargs)


		self.fields['nama_lengkap'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Nama Lengkap'
			})
		self.fields['alamat'].widget.attrs.update({
			'class': 'input_form_style_text',
			'placeholder': 'Alamat'
			})
		self.fields['wa_number'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Nomor Whatsapp/hp'
			})
		self.fields['image'].widget.attrs.update({
			'placeholder': 'Foto'
			})


class DataACForm(forms.ModelForm):

	class Meta:
		model = DataAC
		fields = ['merk', 'kapasitas', 'ruangan', 'image']

	def __init__(self, *args, **kwargs):
		super(DataACForm, self).__init__(*args, **kwargs)


		self.fields['merk'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Merek AC'
			})
		self.fields['kapasitas'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Kapasitas AC'
			})
		self.fields['ruangan'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Ruangan'
			})
		self.fields['image'].widget.attrs.update({
			'placeholder': 'Foto'
			})


class RiwayatPenangananForm(forms.ModelForm):

	class Meta:
		model = RiwayatPenanganan
		fields = ['description', 'trouble_shooting', 'solusi', 'image']

	def __init__(self, *args, **kwargs):
		super(RiwayatPenangananForm, self).__init__(*args, **kwargs)


		self.fields['description'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Deskripsi penanganan'
			})
		self.fields['trouble_shooting'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Trouble shooting'
			})
		self.fields['solusi'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Solusi'
			})
		self.fields['image'].widget.attrs.update({
			'placeholder': 'Foto'
			})

