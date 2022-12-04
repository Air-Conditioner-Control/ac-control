from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from django.utils.text import slugify
from django.utils import timezone



class DataTeknisi(models.Model):
	"""List username dan password teknisi"""
	uid = models.UUIDField(default=uuid.uuid4, editable=False)
	slug = models.SlugField(unique=True, null=False, max_length = 255)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now)
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	
	def __str__(self):
		return f'{self.username}'
		
	def save(self):
		# Slug stuff
		slug_ = slugify(self.username) + '-' + str(self.uid)
		self.slug = slug_[:254]
		super().save()


	def get_absolute_url(self):
		'''
		Slug stuff'''
		from django.urls import reverse
		return reverse('data_teknisi', kwargs = {'slug': self.slug})

