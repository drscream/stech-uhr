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

# vim: set ft=python ts=4 sw=4 :
