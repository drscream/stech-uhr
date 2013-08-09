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
	)


# vim: set ft=python ts=4 sw=4 :
