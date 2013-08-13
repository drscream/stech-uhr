# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from stechuhr.models import UserProfile, UserSettings, WorkDay


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )


class UserSettingsAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'joined_at', 'leaved_at', 'company',
			'hours_per_week', 'pause_minutes_per_day', 'leave_days_per_year', )
	search_fields = ('user', )
	list_filter = ('joined_at', 'leaved_at', )
	list_display_links = ('id', 'user', 'joined_at', )


class WorkDayAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'user', 'kind_of_workday', 'start_time',
			'end_time', )
	search_fields = ('user', )
	date_hierachy = ('date', )
	list_filter = ('date', 'kind_of_workday', )
	list_display_links = ('user', 'id', )


admin.site.unregister(User)
admin.site.register(UserSettings, UserSettingsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(WorkDay, WorkDayAdmin)

# vim: set ft=python ts=4 sw=4 :
