# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User

from stechuhr.models import UserSettings


class UserBasicSettingsForm(forms.Form):
	first_name = forms.CharField(max_length=254)
	last_name = forms.CharField(max_length=254)
	email = forms.EmailField()

	def save(self, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.save()

class UserWorkSettingsForm(forms.Form):
	pk = forms.IntegerField(required=False)
	company = forms.CharField(max_length=254)
	department = forms.CharField(max_length=254, required=False)
	position = forms.CharField(max_length=254, required=False)
	joined_at = forms.DateField()
	leaved_at = forms.DateField(required=False)
	hours_per_week = forms.IntegerField(required=False)
	pause_minutes_per_day = forms.IntegerField(required=False)
	leave_days_per_year = forms.IntegerField(required=False)

	def save(self, user):
		settings = UserSettings()
		settings.user = user
		settings.company = self.cleaned_data['company']
		settings.department = self.cleaned_data['department']
		settings.position = self.cleaned_data['position']
		settings.joined_at = self.cleaned_data['joined_at']
		settings.leaved_at = self.cleaned_data['leaved_at']
		settings.hours_per_week = self.cleaned_data['hours_per_week']
		settings.pause_minutes_per_day = self.cleaned_data['pause_minutes_per_day']
		settings.leave_days_per_year = self.cleaned_data['leave_days_per_year']
		settings.save()
		return settings

	def modify(self):
		settings = UserSettings.objects.get(pk=self.cleaned_data['pk'])
		settings.company = self.cleaned_data['company']
		settings.department = self.cleaned_data['department']
		settings.position = self.cleaned_data['position']
		settings.joined_at = self.cleaned_data['joined_at']
		settings.leaved_at = self.cleaned_data['leaved_at']
		settings.hours_per_week = self.cleaned_data['hours_per_week']
		settings.pause_minutes_per_day = self.cleaned_data['pause_minutes_per_day']
		settings.leave_days_per_year = self.cleaned_data['leave_days_per_year']
		settings.save()
		return settings

class SigninForm(forms.Form):
	username = forms.RegexField(max_length=30, regex=r'^[\w.@+-]+$')
	first_name = forms.CharField(max_length=254)
	last_name = forms.CharField(max_length=254)
	email = forms.EmailField()
	confirm_email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('duplicate_username')

	def clean_confirm_email(self):
		email = self.cleaned_data.get('email')
		confirm_email = self.cleaned_data.get('confirm_email')
		if email != confirm_email:
			raise forms.ValidationError('email missmatch')
		return confirm_email

	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError('password missmatch')
		return confirm_password

	def save(self):
		user = User()
		user.username = self.cleaned_data['username']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.set_password(self.cleaned_data["password"])
		user.save()
		return user

# vim: set ft=python ts=4 sw=4 :
