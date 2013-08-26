# -*- coding: UTF-8 -*-

import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_days_per_week(days):
	if days not in range(7):
		raise ValidationError('Too many workdays per week.')

def validate_hours_per_week(hours):
	if hours not in range(168):
		raise ValidationError('Too many workday hours per week.')

def validate_leave_days_per_year(days):
	if days not in range(365):
		raise ValidationError('Too many leave days per year.')

def validate_pause_minutes_per_day(minutes):
	if minutes not in range(1440):
		raise ValidationError('Too many pause minutes per day.')


class Job(models.Model):
	class Meta:
		ordering = ('-joined_at', 'user', )
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
	days_per_week = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_days_per_week])
	hours_per_week = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_hours_per_week])
	pause_minutes_per_day = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_pause_minutes_per_day])
	leave_days_per_year = models.PositiveSmallIntegerField(null=True,
			blank=True, validators=[validate_leave_days_per_year])

	def get_days_per_week_as_timedelta(self):
		if self.days_per_week is None:
			return None
		return datetime.timedelta(days=self.days_per_week)

	def get_hours_per_week_as_timedelta(self):
		if self.hours_per_week is None:
			return None
		return datetime.timedelta(hours=self.hours_per_week)

	def get_pause_minutes_per_day_as_timedelta(self):
		if self.pause_minutes_per_day is None:
			return None
		return datetime.timedelta(minutes=self.pause_minutes_per_day)

class Report(models.Model):
	class Meta:
		ordering = ('-date', 'user',)
		unique_together = (('user', 'date'),)

	WORKDAY_CHOICES = (
			(u'Daily routine', u'Daily routine'),
			(u'Training', u'Training'),
			(u'Seminar', u'Seminar'),
			(u'Business Trip', u'Business Trip'),
			(u'Unfitness for work', u'Unfitness for work'),
			(u'Leave day', u'Leave day'),
			(u'Flextime leave day', u'Flextime leave day'),
			(u'Holiday', u'Holiday'), 
		)

	def __unicode__(self):
		return '%s %s' % (self.user, self.date.strftime('%y/%m/%d'))

	user = models.ForeignKey(User)
	created_date = models.DateTimeField(default=timezone.now)
	date = models.DateField(auto_now_add=False)
	workday = models.CharField(max_length=255, choices=WORKDAY_CHOICES,
			default='Daily routine')
	start_time = models.TimeField(auto_now_add=False, null=True, blank=True)
	end_time = models.TimeField(auto_now_add=False, null=True,
			blank=True)
	pause_minutes = models.PositiveSmallIntegerField(null=True, blank=True,
			validators=[validate_pause_minutes_per_day])
	workplace = models.CharField(max_length=255, null=True, blank=True)
	log = models.TextField(null=True, blank=True)

	def get_start_time_as_date(self):
		if self.start_time is None:
			return None
		return datetime.datetime.combine(self.date, self.start_time)

	def get_end_time_as_date(self):
		if self.end_time is None:
			return None
		return datetime.datetime.combine(self.date, self.end_time)

	def get_pause_minutes_as_timedelta(self):
		if self.pause_minutes is None:
			return None
		return datetime.timedelta(minutes=self.pause_minutes)

	def get_work_time(self):
		try:
			work_time = self.get_end_time_as_date() - self.get_start_time_as_date()
		except:
			return None
		try:
			work_time -= self.get_pause_minutes_as_timedelta()
		except:
			pass
		return work_time

	def is_started(self):
		if self.start_time is not None:
			return True
		else:
			return False

	def is_finished(self):
		if self.workday == 'Unfitness for work':
			return True

		if self.workday == 'Leave day':
			return True

		if self.workday == 'Flextime leave day':
			return True

		if self.workday == 'Holiday':
			return True

		if self.start_time is not None and self.end_time is not None:
			return True
		else:
			return False

	is_finished.boolean = True
	is_finished.short_description = 'Finished'


# vim: set ft=python ts=4 sw=4 :
