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
		url(r'^user/dashboard/$', views.user_dashboard, name='user_dashboard'),
		url(r'^user/settings/$', views.user_settings, name='user_settings'),
		url(r'^user/settings/basic/$', views.user_settings_basic,
			name='user_settings_basic'),
		url(r'^user/settings/work/$', views.user_settings_work,
			name='user_settings_work'),
		url(r'^user/settings/work/(?P<work_id>\d+)',
			views.user_settings_work_details,
			name='view.user_settings_work_details'),
		# reports
		url(r'^reports/day/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
			views.reports_day, name='reports_day'),
		url(r'^reports/week/(?P<year>\d{4})/(?P<week>\d{1,2})/$',
			views.reports_week, name='reports_week'),
		url(r'^reports/month/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
			views.reports_month, name='reports_month'),
		url(r'^reports/year/(?P<year>\d{4})/$',
			views.reports_year, name='reports_year'),
	)


# vim: set ft=python ts=4 sw=4 :
