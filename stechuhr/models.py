# -*- coding: UTF-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_workday_hours_per_week(hours):
	if hours not in range(168):
		raise ValidationError('Too many workday hours per week.')

def validate_leave_days_per_year(days):
	if days not in range(365):
		raise ValidationError('Too many leave days per year.')

def validate_pause_minutes_per_day(minutes):
	if minutes not in range(1440):
		raise ValidationError('Too many pause minutes per day.')


class UserSettings(models.Model):
	class Meta:
		ordering = ('-joined_at', 'user', )
		verbose_name_plural = 'User settings'
		unique_together = (('user', 'joined_at'), )

	def __unicode__(self):
		return '%s %s' % (self.company, self.joined_at.strftime('%y/%m/%d'))

	user = models.ForeignKey(User)
	create_date = models.DateTimeField(default=timezone.now)
	company = models.CharField(max_length=255)
	department = models.CharField(max_length=255, null=True, blank=True)
	position = models.CharField(max_length=255, null=True, blank=True)
	joined_at = models.DateField(default=timezone.now)
	leaved_at = models.DateField(auto_now_add=False, null=True, blank=True)
	hours_per_week = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_workday_hours_per_week])
	pause_minutes_per_day = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_pause_minutes_per_day])
	leave_days_per_year = models.PositiveSmallIntegerField(null=True,
			blank=True, validators=[validate_leave_days_per_year])


class UserProfile(models.Model):
	class Meta:
		ordering = ('user',)

	def __unicode__(self):
		return '%s' % self.user

	user = models.OneToOneField(User)
	settings = models.ForeignKey(UserSettings, null=True, blank=True)

	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(user=instance)

	post_save.connect(create_user_profile, sender=user)


class WorkDay(models.Model):
	class Meta:
		ordering = ('-date', 'user',)

	WORKDAY_CHOICES = (
			(u'Daily routine', u'Daily routine'),
			(u'Training', u'Training'),
			(u'Seminar', u'Seminar'),
			(u'Business Trip', u'Business Trip'),
			(u'Unfitness for work', u'Unfitness for work'),
			(u'Leave day', u'Leave day'),
			(u'Flextime leave day', u'Flextime leave day'),
		)

	def __unicode__(self):
		return '%s %s' % (self.user, self.date.strftime('%y/%m/%d'))

	user = models.ForeignKey(User)
	created_date = models.DateTimeField(default=timezone.now)
	date = models.DateField(auto_now_add=False)
	kind_of_workday = models.CharField(max_length=255, choices=WORKDAY_CHOICES,
			default='Daily routine')
	start_time = models.TimeField(auto_now_add=False)
	end_time = models.TimeField(auto_now_add=False, null=True,
			blank=True)
	pause_minutes = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_pause_minutes_per_day])
	workplace = models.CharField(max_length=255, null=True, blank=True)
	report = models.TextField(null=True, blank=True)

	def get_attendance_time(kind='gross'):
		if self.end_time is None:
			return None
		elif kind == 'gross':
			return self.end_time - self.start_time
		elif kind == 'net':
			return self.end_time - self.start_time - self.pause_minutes
		else:
			return None


# vim: set ft=python ts=4 sw=4 :
