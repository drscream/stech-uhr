# -*- coding: UTF-8 -*-

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
	class Meta:
		ordering = ['user']

	def __unicode__(self):
		return '%s' % self.user

	user = models.OneToOneField(User)
	company = models.CharField(max_length=255, null=True, blank=True)
	department = models.CharField(max_length=255, null=True, blank=True)
	position = models.CharField(max_length=255, null=True, blank=True)
	place = models.CharField(max_length=255, null=True, blank=True)
	#workdays_per_week = models.PositiveSmallIntegerField(null=True, blank=True)
	hours_per_week = models.PositiveSmallIntegerField(null=True, blank=True)
	pause_per_day = models.TimeField(null=True, blank=True)
	core_working_time_begin = models.TimeField(null=True, blank=True)
	core_working_time_end = models.TimeField(null=True, blank=True)
	days_of_holiday_per_year = models.PositiveSmallIntegerField(null=True,
			blank=True)

	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			UserProfile.objects.create(user=instance)

	post_save.connect(create_user_profile, sender=user)


class Meeting(models.Model):
	class Meta:
		ordering = ['-date', 'user']

	def __unicode__(self):
		title = (self.title[:25] + '...') if len(self.title) > 25 else self.title
		return '%s' % title

	MEETING_CHOICES = (
			('ONE', 'One on one interview'),
			('TEAM', 'Team meeting'),
			('REG', 'Regular meeting'),
			('CONF', 'Conference'),
			('DISC', 'Discussion'),
			('PHONE', 'Telephone Conference'),
			('VIDEO', 'Video Conference'),
		)

	user = models.ForeignKey(UserProfile)
	date = models.DateField(auto_now_add=False)
	title = models.CharField(max_length=255)
	kind = models.CharField(max_length=255, choices=MEETING_CHOICES,
			default='TEAM')
	begin = models.TimeField(auto_now_add=False)
	end = models.TimeField(auto_now_add=False)


class WorkDay(models.Model):
	class Meta:
		ordering = ['-date', 'user']

	WORKDAY_CHOICES = (
			('DR', u'Daily routine'),
			('UFW', u'Unfitness for work'),
			('T', u'Training'),
			('S', u'Seminar'),
			('BT', u'Business Trip'),
			('WT', u'Works outing')
		)

	def __unicode__(self):
		return '%s %s' % (self.user, self.date.strftime('%y/%m/%d'))

	user = models.ForeignKey(UserProfile)
	date = models.DateField(auto_now_add=False, unique=True)
	kind = models.CharField(max_length=255, choices=WORKDAY_CHOICES,
			default='DR')
	begin = models.TimeField(auto_now_add=False)
	end = models.TimeField(auto_now_add=False, null=True,
			blank=True)
	pause = models.TimeField(auto_now_add=False, null=True, blank=True)
	place = models.CharField(max_length=255, null=True, blank=True)
	meetings = models.ManyToManyField(Meeting, null=True, blank=True,
			related_name='meetings')
	description = models.TextField()

	def get_duration(self):
		if self.end is None:
			return None
		else:
			return self.end - self.begin

# vim: set ft=python ts=4 sw=4 :
