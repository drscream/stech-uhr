from django import forms
from django.contrib.auth.models import User

class UserBasicSettingsForm(forms.Form):
	first_name = forms.CharField(max_length=254)
	last_name = forms.CharField(max_length=254)
	email = forms.EmailField()

	def save(self, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.save()

# vim: set ft=python ts=4 sw=4 :
