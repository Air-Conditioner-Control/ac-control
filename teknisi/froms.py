from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class TeknisiCreationForm(forms.Form):
	username = forms.CharField(max_length=20)
	password = forms.CharField(max_length=20)
	email = forms.EmailField()

	def __init__(self, *args, **kwargs):
		super(TeknisiCreationForm, self).__init__(*args, **kwargs)


		self.fields['username'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'username'
			})
		self.fields['email'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'email'
			})
		self.fields['password'].widget.attrs.update({
			'class': 'input_form_style',
			'placeholder': 'password'
			})
		