from django.db import models
from PIL import Image
import uuid
from django.utils.text import slugify
from django.utils import timezone
from users.models import Profile
from perusahaan.models import Perusahaan



class DataCustomers(models.Model):
	"""Data ini jangan di delet"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	nama_lengkap = models.CharField(max_length=50)
	alamat = models.TextField(blank=True, null=True)

	wa_number = models.CharField(max_length=12)
	image = models.ImageField(default='customer/default.jpg', upload_to='customer')
	status_choices = (
		('AKTIF', 'AKTIF'),
		('TIDAK AKTIF', 'TIDAK AKTIF'),
		)
	status = models.CharField(max_length=50, choices=status_choices, default='AKTIF')
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.SET_NULL, null=True, default=None)
	
	def __str__(self):
		return f'{self.nama_lengkap}'
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.nama_lengkap) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('data_customers', kwargs = {'slug': self.slug})


class DataAC(models.Model):
	"""List username dan password teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	customer = models.ForeignKey(DataCustomers, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)
	
	ac_id = models.CharField(max_length=8)
	label = models.CharField(max_length=200, blank=True, null=True)
	merk = models.CharField(max_length=100)

	tipe = models.CharField(max_length=100, blank=True, null=True)
	model_indoor = models.CharField(max_length=200, blank=True, null=True)
	model_outdoor = models.CharField(max_length=200, blank=True, null=True)
	tanggal_pemasangan = models.CharField(max_length=100, blank=True, null=True)
	kontraktor = models.TextField(blank=True, null=True)
	informasi_servis = models.TextField(blank=True, null=True)
	periode_servis = models.IntegerField(blank=True, null=True)

	kapasitas = models.CharField(max_length=100, blank=True, null=True)
	ruangan = models.CharField(max_length=100, blank=True, null=True)

	image = models.ImageField(default='ac/default.png', upload_to='ac')
	
	def __str__(self):
		return f'{self.customer.nama_lengkap}-{self.ac_id}-{self.merk}-{self.kapasitas}'
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.customer.nama_lengkap) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()
		self.ac_id = 'AC-' + str(self.id)
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('data_ac', kwargs = {'slug': self.slug})


class RiwayatPenanganan(models.Model):
	"""List username dan password teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	ac = models.ForeignKey(DataAC, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)
	
	tanggal = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	tipe_pekerjaan = models.TextField(blank=True, null=True)
	tekanan_low_press = models.TextField(blank=True, null=True)
	tekanan_high_press = models.TextField(blank=True, null=True)
	arus_listrik = models.CharField(max_length=100, blank=True, null=True)
	noise = models.TextField(blank=True, null=True)
	volatase = models.CharField(max_length=100, blank=True, null=True)
	keterangan = models.TextField(blank=True, null=True)
	
	teknisi = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, default=None)

	image = models.ImageField(default='riwayat_penanganan/default.png', upload_to='riwayat_penanganan')
	
	def __str__(self):
		return f'{self.ac}{self.description}'[:20]
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.ac) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('riwayat_penanganan', kwargs = {'slug': self.slug})


class TroubleShooting(models.Model):
	"""List username dan password teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	riwayat_penanganan = models.ForeignKey(RiwayatPenanganan, on_delete=models.CASCADE, null=True)
	date_created = models.DateTimeField(default=timezone.now)
	
	tanggal = models.CharField(max_length=100, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	analisa_awal = models.TextField(blank=True, null=True)
	solusi = models.TextField(blank=True, null=True)
	hasil_perbaikan = models.TextField(blank=True, null=True)
	kategori_kerusakan = models.TextField(blank=True, null=True)
	
	teknisi = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, default=None)

	image = models.ImageField(default='trouble_shooting/default.png', upload_to='trouble_shooting')
	
	def __str__(self):
		return f'{self.riwayat_penanganan.ac}{self.description}'[:20]
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.riwayat_penanganan.ac) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('trouble_shooting', kwargs = {'slug': self.slug})


class DataBelanja(models.Model):
	"""List username dan password teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	riwayat_penanganan = models.ForeignKey(RiwayatPenanganan, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)
	
	tanggal = models.CharField(max_length=100, blank=True, null=True)
	nama_barang = models.CharField(max_length=200, blank=True, null=True)
	unit = models.IntegerField(blank=True, null=True)
	harga_total = models.FloatField(blank=True, null=True)
	
	teknisi = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, default=None)

	foto_kuitansi = models.ImageField(default='kuitansi/default.png', upload_to='kuitansi')
	
	def __str__(self):
		return f'{self.riwayat_penanganan.ac}{self.nama_barang}'[:20]
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.nama_barang) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()

		# img = Image.open(self.foto_kuitansi.path)

		# if img.height > 300 or img.width > 300:
		# 	output_size = (300, 300)
		# 	img.thumbnail(output_size)
		# 	img.save(self.foto_kuitansi.path)


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('data_belanja', kwargs = {'slug': self.slug})



