# -*- coding: UTF-8 -*-

import datetime

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from stechuhr.models import UserSettings, WorkDay
from stechuhr.forms import UserBasicSettingsForm, UserWorkSettingsForm


def index(request):
	if request.user.is_authenticated():
		return redirect('user_dashboard')
	return render(request, 'index.html')

def signin(request):
	return render(request, 'signin.html')

@login_required(login_url='/stechuhr/login/')
def user_dashboard(request):
	now = datetime.date.today()
	context = {
			'year': now.year,
			'month': now.month,
			'day': now.day,
			'week': now.isocalendar()[1]
		}
	return render(request, 'user/dashboard.html', context)

@login_required(login_url='/stechuhr/login/')
def user_settings(request):
	settings = None
	try:
		settings = UserSettings.objects.filter(user=request.user.pk).latest('joined_at')
	except UserSettings.DoesNotExist:
		context = {}
	if settings:
		context = {
				'settings': settings,
			}
	return render(request, 'user/settings.html', context)

@login_required(login_url='/stechuhr/login/')
def user_settings_basic(request):
	if request.method == 'POST':
		form = UserBasicSettingsForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect(user_settings)
	else:
		form = UserBasicSettingsForm(request)

	return render(request, 'user/settings/basic.html', { 'form': form, })

@login_required(login_url='/stechuhr/login/')
def user_settings_work(request):
	if request.method == 'POST':
		form = UserWorkSettingsForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect(user_settings)
	else:
		form = UserWorkSettingsForm(request)

	settings = UserSettings.objects.filter(user=request.user.pk)
	context = { 
			'settings': settings,
			'form': form,
		}
	return render(request, 'user/settings/work.html', context)

@login_required(login_url='/stechuhr/login/')
def user_settings_work_details(request, work_id=None):
	if request.method == 'POST':
		form = UserWorkSettingsForm(request.POST)
		if form.is_valid():
			form.modify()
			return redirect(user_settings)
	else:
		form = UserWorkSettingsForm(request)

	try:
		settings = UserSettings.objects.get(pk=work_id)
	except UserSettings.DoesNotExist:
		raise Http404
	context = { 
			'settings': settings,
			'form': form,
		}
	return render(request, 'user/settings/work_details.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_day(request, year, month, day):
	return HttpResponse('<h1>%s/%s/%s</h1>' % (year, month, day))

@login_required(login_url='/stechuhr/login/')
def reports_week(request, year, week):
	return HttpResponse('<h1>%s/%s</h1>' % (year, week))

@login_required(login_url='/stechuhr/login/')
def reports_month(request, year, month):
	return HttpResponse('<h1>%s/%s</h1>' % (year, month))

@login_required(login_url='/stechuhr/login/')
def reports_year(request, year):
	return HttpResponse('<h1>%s</h1>' % (year))

def permission_denied(request):
	return HttpResponse('<h1>Permission denied (403)</h1>')


# vim: set ft=python ts=4 sw=4 :
