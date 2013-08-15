# -*- coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User

from stechuhr.models import Job


class UserForm(forms.Form):
	first_name = forms.CharField(max_length=254)
	last_name = forms.CharField(max_length=254)
	email = forms.EmailField()

	def save(self, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.save()

class JobForm(forms.Form):
	pk = forms.IntegerField(required=False, widget=forms.HiddenInput)
	company = forms.CharField(max_length=254)
	department = forms.CharField(max_length=254, required=False)
	position = forms.CharField(max_length=254, required=False)
	joined_at = forms.DateField(widget=forms.DateInput)
	leaved_at = forms.DateField(widget=forms.DateInput, required=False)
	hours_per_week = forms.IntegerField(required=False)
	pause_minutes_per_day = forms.IntegerField(required=False)
	leave_days_per_year = forms.IntegerField(required=False)

	def save(self, user):
		job = Job()
		job.user = user
		job.company = self.cleaned_data['company']
		job.department = self.cleaned_data['department']
		job.position = self.cleaned_data['position']
		job.joined_at = self.cleaned_data['joined_at']
		job.leaved_at = self.cleaned_data['leaved_at']
		job.hours_per_week = self.cleaned_data['hours_per_week']
		job.pause_minutes_per_day = self.cleaned_data['pause_minutes_per_day']
		job.leave_days_per_year = self.cleaned_data['leave_days_per_year']
		job.save()
		return job

	def modify(self):
		job = Job.objects.get(pk=self.cleaned_data['pk'])
		job.company = self.cleaned_data['company']
		job.department = self.cleaned_data['department']
		job.position = self.cleaned_data['position']
		job.joined_at = self.cleaned_data['joined_at']
		job.leaved_at = self.cleaned_data['leaved_at']
		job.hours_per_week = self.cleaned_data['hours_per_week']
		job.pause_minutes_per_day = self.cleaned_data['pause_minutes_per_day']
		job.leave_days_per_year = self.cleaned_data['leave_days_per_year']
		job.save()
		return job

class SigninForm(forms.Form):
	username = forms.RegexField(max_length=30, regex=r'^[\w.@+-]+$')
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('duplicate_username')

	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError('password missmatch')
		return confirm_password

	def save(self):
		user = User()
		user.username = self.cleaned_data['username']
		user.set_password(self.cleaned_data["password"])
		user.save()
		return user

class ReportForm(forms.Form):

	WORKDAY_CHOICES = (
			(u'Daily routine', u'Daily routine'),
			(u'Training', u'Training'),
			(u'Seminar', u'Seminar'),
			(u'Business Trip', u'Business Trip'),
			(u'Unfitness for work', u'Unfitness for work'),
			(u'Leave day', u'Leave day'),
			(u'Flextime leave day', u'Flextime leave day'),
		)

	date = forms.DateField(widget=forms.DateInput)
	workday = forms.ChoiceField(choices=WORKDAY_CHOICES)
	start_time = forms.TimeField(widget=forms.TimeInput, required=False)
	end_time = forms.TimeField(widget=forms.TimeInput, required=False)
	pause_minutes = forms.IntegerField(required=False)
	workplace = forms.CharField(max_length=254, required=False)
	report = forms.CharField(widget=forms.Textarea, required=False)


# vim: set ft=python ts=4 sw=4 :
