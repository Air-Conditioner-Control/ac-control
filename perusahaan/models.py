from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class Perusahaan(models.Model):
	"""Untuk admin dan teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	name = models.CharField(max_length=200)
	wa_number = models.CharField(max_length=12)
	wa_link = models.CharField(max_length=200)
	email = models.CharField(max_length=50, blank=True, null=True)
	alamat = models.TextField(blank=True, null=True)
	motto = models.TextField(blank=True, null=True)
	logo = models.ImageField(default='perusahaan/default.jpg', upload_to='perusahaan')
	

	def __str__(self):
		if self.name:
			return f'{self.name}'
		else:
			return f'{self.user.username}'

	def save(self):
		# Slug stuff
		if self.name:
			slug_ = slugify(self.name) + '-' + str(self.uid)
			self.slug = slug_[:254]
		else:
			slug_ = slugify(self.user.username)[:254-len(str(self.uid))] + '-' + str(self.uid)
			self.slug = slug_

		super().save()

		img = Image.open(self.logo.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.logo.path)

	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('perusahaan', kwargs = {'slug': self.slug})




# class AnggotaPerusahaan(models.Model):
# 	"""Untuk admin dan teknisi"""
# 	uid = models.UUIDField(default=uuid.uuid4, editable=False)
# 	slug = models.SlugField(unique=True, null=False, max_length = 255)
# 	date_created = models.DateTimeField(default=timezone.now)

# 	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.SET_NULL, null=True, default=None)
# 	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

# 	admin_type_choices = (
# 		('ADMIN', 'ADMIN'),
# 		('TEKNISI', 'TEKNISI'),
# 		('UMUM', 'UMUM'),
# 		('SUPERADMIN', 'SUPERADMIN')
# 		)
# 	user_type = models.CharField(max_length=200, choices=admin_type_choices, default='UMUM')


# 	def __str__(self):
# 		if self.user.username:
# 			return f'{self.user.username}'
# 		else:
# 			return f'{self.user.username}'

# 	def save(self):
# 		# Slug stuff
# 		if self.user.username:
# 			slug_ = slugify(self.user.username + '-' + str(self.perusahaan)) + '-' + str(self.uid)
# 			self.slug = slug_[:254]
# 		else:
# 			slug_ = slugify(self.user.username)[:254-len(str(self.uid))] + '-' + str(self.uid)
# 			self.slug = slug_

# 		super().save()


# 	def get_absolute_url(self):
# 		'''
# 		Slug stuff'''
# 		from django.urls import reverse
# 		return reverse('anggota_perusahaan', kwargs = {'slug': self.slug})


class PelangganKami(models.Model):
	"""[not used]Untuk admin dan teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	logo = models.ImageField(default='pelanggan_kami/default.jpg', upload_to='pelanggan_kami')
	name = models.CharField(max_length=200)
	

	def __str__(self):
		return f'{self.name}'
		

	def save(self):
		# Slug stuff
		if self.name:
			slug_ = slugify(self.name) + '-' + str(self.uid)
			self.slug = slug_[:254]
		else:
			slug_ = str(self.uid)
			self.slug = slug_

		super().save()

		img = Image.open(self.logo.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.logo.path)

	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('pelanggan_kami', kwargs = {'slug': self.slug})



class LayananKami(models.Model):
	"""Untuk admin dan teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	image = models.ImageField(default='layanan_kami/default.png', upload_to='layanan_kami')
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	

	def __str__(self):
		return f'{self.name}'
		

	def save(self):
		# Slug stuff
		if self.name:
			slug_ = slugify(self.name) + '-' + str(self.uid)
			self.slug = slug_[:254]
		else:
			slug_ = str(self.uid)
			self.slug = slug_

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
		return reverse('layanan_kami', kwargs = {'slug': self.slug})


class Testimoni(models.Model):
	"""Untuk admin dan teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	date_created = models.DateTimeField(default=timezone.now)
	
	perusahaan = models.ForeignKey(Perusahaan, on_delete=models.CASCADE)
	image = models.ImageField(default='testimoni/default.jpg', upload_to='testimoni')
	name = models.CharField(max_length=200)
	testimoni = models.TextField(blank=True, null=True)
	jabatan = models.CharField(max_length=200)
	

	def __str__(self):
		return f'{self.name}'
		

	def save(self):
		# Slug stuff
		if self.name:
			slug_ = slugify(self.name) + '-' + str(self.uid)
			self.slug = slug_[:254]
		else:
			slug_ = str(self.uid)
			self.slug = slug_

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
		return reverse('testimoni', kwargs = {'slug': self.slug})




