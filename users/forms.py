from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField() # By default required = True

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)


		self.fields['username'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'username'
			})
		self.fields['email'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'email'
			})
		self.fields['password1'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'password'
			})
		self.fields['password2'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'tulis kembali password'
			})


class LengkapiProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'full_name', 'wa_number']

	def __init__(self, *args, **kwargs):
		super(LengkapiProfileForm, self).__init__(*args, **kwargs)
		
		self.fields['image'].widget.attrs.update({
			'class': 'image_form_style',
			'placeholder': 'foto profile anda'
			})
		self.fields['full_name'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'Nama Lengkap'
			})
		self.fields['wa_number'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'contoh: 085xxxxxxxxx'
			})


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField() # Default required = True

	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'full_name', ]

	def __init__(self, *args, **kwargs):
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)
		self.fields['full_name'].label = "Nama lengkap"
		self.fields['full_name'].widget.attrs['placeholder'] = "Ketik nama lengkap anda di sini!"
		self.fields['image'].label = "Foto profile"
		self.fields['image'].widget.attrs['placeholder'] = "Foto profile"
