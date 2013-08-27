# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from stechuhr.models import Job, Report


class JobAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'joined_at', 'leaved_at', 'company',
			'days_per_week', 'hours_per_week', 'pause_minutes_per_day',
			'leave_days_per_year', )
	search_fields = ('user', )
	list_filter = ('joined_at', 'leaved_at', )
	list_display_links = ('id', 'user', 'joined_at', )


class ReportAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'user', 'workday', 'start_time',
			'end_time', 'is_closed', )
	search_fields = ('user', )
	date_hierachy = ('date', )
	list_filter = ('date', 'workday', )
	list_display_links = ('user', 'id', )


admin.site.register(Job, JobAdmin)
admin.site.register(Report, ReportAdmin)

# vim: set ft=python ts=4 sw=4 :
