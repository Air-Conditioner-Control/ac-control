from django.db import models
from PIL import Image
import uuid
from django.utils.text import slugify
from django.utils import timezone
from users.models import Profile



class DataCustomers(models.Model):
	"""Data ini jangan di delet"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	nama_lengkap = models.CharField(max_length=50)
	alamat = models.CharField(max_length=200)
	wa_number = models.CharField(max_length=12)
	image = models.ImageField(default='customer/default.jpg', upload_to='customer')
	status_choices = (
		('AKTIF', 'AKTIF'),
		('TIDAK AKTIF', 'TIDAK AKTIF'),
		)
	status = models.CharField(max_length=50, choices=status_choices, default='AKTIF')
	
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
	merk = models.CharField(max_length=100)
	kapasitas = models.CharField(max_length=100)
	ruangan = models.CharField(max_length=100)

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
	
	teknisi = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, default=None)
	
	description = models.TextField(blank=True, null=True)
	trouble_shooting = models.TextField(blank=True, null=True)
	solusi = models.TextField(blank=True, null=True)

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




