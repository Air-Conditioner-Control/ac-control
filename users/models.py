from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.utils.text import slugify
from django.utils import timezone



class Profile(models.Model):
	"""Untuk admin dan teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)
	image = models.ImageField(default='profile/default.jpg', upload_to='profile')
	full_name = models.CharField(max_length=200)
	admin_type_choices = (
		('ADMIN', 'ADMIN'),
		('TEKNISI', 'TEKNISI'),
		('UMUM', 'UMUM'),
		)
	user_type = models.CharField(max_length=200, choices=admin_type_choices, default='UMUM')
	wa_number = models.CharField(max_length=12)
	

	def __str__(self):
		if self.full_name:
			return f'{self.full_name}'
		else:
			return f'{self.user.username}'

	def save(self):
		# Slug stuff
		if self.full_name:
			slug_ = slugify(self.full_name) + '-' + str(self.uid)
			self.slug = slug_[:254]
		else:
			slug_ = slugify(self.user.username)[:254-len(str(self.uid))] + '-' + str(self.uid)
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
		return reverse('profile', kwargs = {'slug': self.slug})

