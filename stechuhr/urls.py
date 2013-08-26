# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

from stechuhr import views


urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		# authentication
		url(r'^login/$', 'django.contrib.auth.views.login',
			kwargs={'template_name': 'login.html'}, name='login'),
		url(r'^logout/$', 'django.contrib.auth.views.logout',
			kwargs={'template_name': 'logout.html'}, name='logout'),
		url(r'^signin/$', views.signin, name='signin'),
		# user
		url(r'^dashboard/$', views.dashboard, name='dashboard'),
		url(r'^settings/$', views.settings, name='settings'),
		url(r'^settings/basic/$', views.settings_basic, name='settings_basic'),
		url(r'^settings/jobs/$', views.settings_jobs,
			name='settings_jobs'),
		url(r'^settings/jobs/(?P<job_id>\d+)',
			views.settings_job_details,
			name='settings_job_details'),
		url(r'^settings/jobs/new/$',
			views.settings_job_new,
			name='settings_job_new'),
		# reports
		url(r'^reports/$', views.reports, name='reports'),
		url(r'^reports/day/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
			views.reports_day, name='reports_day'),
		url(r'^reports/day/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/view/$',
			views.reports_day_view, name='reports_day_view'),
		url(r'^reports/week/(?P<year>\d{4})/(?P<week>\d{1,2})/$',
			views.reports_week, name='reports_week'),
		url(r'^reports/month/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
			views.reports_month, name='reports_month'),
	)


# vim: set ft=python ts=4 sw=4 :
