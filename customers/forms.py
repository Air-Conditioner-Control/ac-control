from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *



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
		fields = ['label', 'merk', 'tipe', 
		'model_indoor', 'model_outdoor',
		'tanggal_pemasangan', 'kontraktor',
		'informasi_servis', 'periode_servis', 
		'kapasitas', 'ruangan', 'image']

	def __init__(self, *args, **kwargs):
		super(DataACForm, self).__init__(*args, **kwargs)


		self.fields['label'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Label perusahaan'
			})
		self.fields['merk'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Merek AC'
			})
		self.fields['tipe'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tipe'
			})
		self.fields['model_indoor'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Model indoor'
			})
		self.fields['model_outdoor'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Model outdoor'
			})
		self.fields['tanggal_pemasangan'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tanggal pemasangan'
			})
		self.fields['kontraktor'].widget.attrs.update({
			'class': 'input_form_style_text',
			'placeholder': 'Kontraktor'
			})
		self.fields['informasi_servis'].widget.attrs.update({
			'class': 'input_form_style_text',
			'placeholder': 'Informasi servis'
			})
		self.fields['periode_servis'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Periode servis'
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
		fields = ['tanggal', 'description',
		'tipe_pekerjaan', 'tekanan_low_press',
		'tekanan_high_press', 'arus_listrik',
		'noise', 'volatase', 'keterangan',
		'image']

	def __init__(self, *args, **kwargs):
		super(RiwayatPenangananForm, self).__init__(*args, **kwargs)


		self.fields['tanggal'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tanggal'
			})
		self.fields['description'].widget.attrs.update({
			'class': 'input_form_style_text',
			'placeholder': 'Deskripsi Penanganan'
			})
		self.fields['tipe_pekerjaan'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tipe Pekerjaan'
			})

		self.fields['tekanan_low_press'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tekanan Low Press'
			})
		self.fields['tekanan_high_press'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tekanan High Press'
			})
		self.fields['arus_listrik'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Arus Listrik'
			})
		self.fields['noise'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Nois/Suara'
			})
		self.fields['volatase'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Voltase'
			})
		self.fields['keterangan'].widget.attrs.update({
			'class': 'input_form_style_text',
			'placeholder': 'Keterangan'
			})
		self.fields['image'].widget.attrs.update({
			'placeholder': 'Foto'
			})


class TroubleShootingForm(forms.ModelForm):

	class Meta:
		model = TroubleShooting
		fields = ['tanggal', 'description',
		'analisa_awal', 'solusi', 
		'hasil_perbaikan', 'kategori_kerusakan',
		'image']

	def __init__(self, *args, **kwargs):
		super(TroubleShootingForm, self).__init__(*args, **kwargs)


		self.fields['tanggal'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tanggal'
			})
		self.fields['description'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Deskripsi Trouble Shooting'
			})

		self.fields['analisa_awal'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Analisa Awal'
			})
		self.fields['solusi'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Solusi'
			})
		self.fields['hasil_perbaikan'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Hasil Perbaikan'
			})
		self.fields['kategori_kerusakan'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Kategori Kerusakan'
			})
		self.fields['image'].widget.attrs.update({
			'placeholder': 'Foto'
			})


class DataBelanjaForm(forms.ModelForm):

	class Meta:
		model = DataBelanja
		fields = ['tanggal', 'nama_barang',
		'unit', 'harga_total',
		'foto_kuitansi']

	def __init__(self, *args, **kwargs):
		super(DataBelanjaForm, self).__init__(*args, **kwargs)


		self.fields['tanggal'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Tanggal'
			})
		self.fields['nama_barang'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Nama Barang'
			})
		self.fields['unit'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Unit'
			})
		self.fields['harga_total'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Harga Total',
			'localization': True
			})
		self.fields['foto_kuitansi'].widget.attrs.update({
			'placeholder': 'Foto Kuitansi'
			})

