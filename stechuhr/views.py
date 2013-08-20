# -*- coding: UTF-8 -*-

import datetime

from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from stechuhr.models import Job, Report
from stechuhr.forms import UserForm, JobForm, SigninForm, ReportForm
from stechuhr.utils import *


def index(request):
	if request.user.is_authenticated():
		return redirect('dashboard')
	return render(request, 'index.html')

def signin(request):
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(index)
	else:
		form = SigninForm()

	return render(request, 'signin.html', { 'form': form, })

@login_required(login_url='/stechuhr/login/')
def dashboard(request):
	return render(request, 'dashboard.html')

@login_required(login_url='/stechuhr/login/')
def settings(request):
	job = None
	try:
		job = Job.objects.filter(user=request.user.pk).latest('joined_at')
	except Job.DoesNotExist:
		context = {}
	if job:
		context = {
				'job': job,
			}
	return render(request, 'settings.html', context)

@login_required(login_url='/stechuhr/login/')
def settings_basic(request):
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			form.save(request.user)
	else:
		form = UserForm(request)

	return render(request, 'settings/basic.html', { 'form': form, })

@login_required(login_url='/stechuhr/login/')
def settings_job(request):
	if request.method == 'POST':
		job = Job.objects.get(pk=request.POST.get('pk'))
		job.delete()
	jobs = Job.objects.filter(user=request.user.pk)
	context = { 
			'jobs': jobs,
		}
	return render(request, 'settings/job.html', context)

@login_required(login_url='/stechuhr/login/')
def settings_job_details(request, job_id=None):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			form.modify()
			return redirect('settings_job')
	else:
		form = JobForm(request)

	job = get_object_or_404(Job, pk=job_id)

	context = { 
			'job': job,
			'form': form,
		}
	return render(request, 'settings/job/details.html', context)

@login_required(login_url='/stechuhr/login/')
def settings_job_new(request):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			form.new(request.user)
			return redirect('settings_job')
	else:
		form = JobForm(request)

	context = { 
			'form': form,
		}
	return render(request, 'settings/job/new.html', context)

@login_required(login_url='/stechuhr/login/')
def reports(request):
	now = datetime.date.today()
	context = {
			'year': now.year,
			'month': now.month,
			'day': now.day,
			'week': now.isocalendar()[1]
		}
	return render(request, 'reports.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_day(request, year, month, day):
	if request.method == 'POST':
		form = ReportForm(request.POST)
		if form.is_valid():
			if request.POST.__contains__('save'):
				if request.POST.__contains__('pk'):
					form.modify()
				else:
					form.new(request.user)
			elif request.POST.__contains__('export'):
					return form.export()
			elif request.POST.__contains__('reset'):
					form.delete()
	else:
		form = ReportForm()

	try:
		date = datetime.date(int(year), int(month), int(day))
	except ValueError:
		raise Http404

	try:
		report = Report.objects.filter(user=request.user).filter(date=date).get()
	except Report.DoesNotExist:
		report = None

	try:
		job = Job.objects.filter(
			Q(user=request.user),
			Q(joined_at__lte=date),
			Q(leaved_at__gte=date) | Q(leaved_at=None)
		).order_by('joined_at')
	except Job.DoesNotExist:
		job = None

	if job:
		job = job[0]
	else:
		job = None

	context = {
		'year': year,
		'month': month,
		'day': day,
		'report': report,
		'job': job,
		'form': form,
		'prev_day': (date - datetime.timedelta(days=1)),
		'next_day': (date + datetime.timedelta(days=1)),
	}
	return render(request, 'reports/day.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_week(request, year, week):
	if int(week) not in range(1,53):
		raise Http404

	start_date = isoweek_startdate(int(year), int(week))
	end_date = start_date + datetime.timedelta(days=6)

	if int(week) == 1:
		prev_week = "%d/%d/" % (int(year) - 1, 52)
	else:
		prev_week = "%d/%d/" % (int(year), int(week) - 1)

	if int(week) == 52:
		next_week = "%d/%d" % (int(year) + 1, 1)
	else:
		next_week = "%d/%d" % (int(year), int(week) + 1)

	try:
		reports = Report.objects.filter(date__gte=start_date).filter(date__lte=end_date).order_by('date')
	except Report.DoesNotExist:
		reports = None

	context = {
			'year': year,
			'week': week,
			'reports': reports,
			'prev_week': prev_week,
			'next_week': next_week,
			'start_date': start_date,
		}
	return render(request, 'reports/week.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_month(request, year, month):
	if int(month) not in range(1,13):
		raise Http404

	startdate = datetime.date(int(year), int(month), 1)
	if int(month) == 12:
		enddate = datetime.date(int(year) + 1, 1, 1) - datetime.timedelta(days=1)
	else:
		enddate = datetime.date(int(year), int(month) + 1, 1) - datetime.timedelta(days=1)

	if int(month) == 12:
		next_mon = "%d/%d/" % (int(year) + 1, 1)
	else:
		next_mon = "%d/%d/" % (int(year), int(month) + 1)
	if int(month) == 1:
		prev_mon = "%d/%d/" % (int(year) - 1, 12)
	else:
		prev_mon = "%d/%d/" % (int(year), int(month) - 1)

	try:
		report_objs = Report.objects.filter(date__gte=startdate).filter(date__lte=enddate).order_by('date')
	except Report.DoesNotExist:
		report_objs = None

	if report_objs:
		paginator = Paginator(report_objs, 5)
	
		page = request.GET.get('page')
		try:
			reports = paginator.page(page)
		except PageNotAnInteger:
			reports = paginator.page(1)
		except EmptyPage:
			reports = paginator.page(paginator.num_pages)
	else:
		reports = None

	context = {
			'year': year,
			'month': month,
			'prev_mon': prev_mon,
			'next_mon': next_mon,
			'reports': reports,
		}
	return render(request, 'reports/month.html', context)

def permission_denied(request):
	return HttpResponse('<h1>Permission denied (403)</h1>')


# vim: set ft=python ts=4 sw=4 :
