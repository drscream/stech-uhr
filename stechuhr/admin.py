# -*- coding: UTF-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from stechuhr.models import UserProfile, WorkDay, Meeting


class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'profile'


class UserAdmin(UserAdmin):
	inlines = (UserProfileInline, )


class MeetingAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'user', 'title', 'kind', 'begin', 'end')
	search_fields = ('user', 'title', )
	date_hierachy = 'date'
	list_filter = ('date', )
	list_display_links = ('title', 'id', )


class WorkDayAdmin(admin.ModelAdmin):
	list_display = ('id', 'date', 'user', 'kind', 'begin', 'end', )
	search_fields = ('user', )
	date_hierachy = 'date'
	list_filter = ('date', )
	list_display_links = ('user', 'id', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(WorkDay, WorkDayAdmin)
admin.site.register(Meeting, MeetingAdmin)

# vim: set ft=python ts=4 sw=4 :
