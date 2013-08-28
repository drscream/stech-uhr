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
	today = datetime.date.today()

	context = {}

	try:
		report = Report.objects. \
			filter(user=request.user.pk). \
			filter(date=today). \
			get()
	except Report.DoesNotExist:
		pass
	else:
		day = {
			'report': report,
			'is_working_day': report.is_working_day(),
			'start_date': report.get_start_time_as_date(),
			'end_date': report.get_end_time_as_date(),
		}
		context.update(day=day)

	week = today.isocalendar()[1]
	start_date = isoweek_startdate(today.year, week)
	end_date = start_date + datetime.timedelta(days=6)
	try:
		reports = Report.objects. \
			filter(user=request.user.pk). \
			filter(date__range=(start_date, end_date)). \
			order_by('date')
	except:
		pass
	else:
		opened = [report.is_opened() for report in reports].count(True)
		working_days = [report.is_working_day() for report in reports].count(True)
		leave_days = [report.is_leave_day() for report in reports].count(True)
		sick_days = [report.is_sick_day() for report in reports].count(True)
		working_time = sum([report.get_working_time() for report in reports],
			datetime.timedelta(seconds=0))
		week = {
			'reports': {
				'count': {
					'opened': opened,
					'working_days': working_days,
					'leave_days': leave_days,
					'sick_days': sick_days,
				},
				'working_time': working_time,
			}
		}
		context.update(week=week)

	return render(request, 'dashboard.html', context)

@login_required(login_url='/stechuhr/login/')
def settings(request):
	try:
		job = Job.objects. \
			filter(user=request.user.pk). \
			latest('joined_at')
	except Job.DoesNotExist:
		context = {}
	else:
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
def settings_jobs(request):
	if request.method == 'POST':
		job = Job.objects.get(pk=request.POST.get('pk'))
		job.delete()

	jobs = Job.objects.filter(user=request.user.pk)
	context = { 
		'jobs': jobs,
	}

	return render(request, 'settings/jobs.html', context)

@login_required(login_url='/stechuhr/login/')
def settings_job_details(request, job_id=None):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			if request.POST.__contains__('save'):
				form.modify()
			elif request.POST.__contains__('delete'):
				form.delete()
			return redirect('settings_jobs')
	else:
		form = JobForm(request)

	job = get_object_or_404(Job, pk=job_id)

	context = { 
		'job': job,
		'form': form,
	}

	return render(request, 'settings/jobs/details.html', context)

@login_required(login_url='/stechuhr/login/')
def settings_job_new(request):
	if request.method == 'POST':
		form = JobForm(request.POST)
		if form.is_valid():
			form.new(request.user)
			return redirect('settings_jobs')
	else:
		form = JobForm(request)

	context = {
		'form': form,
	}

	return render(request, 'settings/jobs/new.html', context)

@login_required(login_url='/stechuhr/login/')
def reports(request):
	return render(request, 'reports.html')

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
			elif request.POST.__contains__('reset'):
				form.delete()
	else:
		form = ReportForm()

	try:
		date = datetime.date(int(year), int(month), int(day))
	except ValueError:
		raise Http404

	try:
		report = Report.objects. \
			filter(user=request.user.pk). \
			filter(date=date). \
			get()
	except Report.DoesNotExist:
		report = None

	try:
		job = Job.objects.filter(
			Q(user=request.user),
			Q(joined_at__lte=date),
			Q(leaved_at__gte=date) | Q(leaved_at=None)
		).order_by('joined_at').get()
	except Job.DoesNotExist:
		job = None

	context = {
		'date': date,
		'report': report,
		'job': job,
		'form': form,
	}

	return render(request, 'reports/day.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_week(request, year, week):
	try:
		date = isoweek_startdate(int(year), int(week))
	except:
		raise Http404

	start_date = date
	end_date = start_date + datetime.timedelta(days=6)

	try:
		reports = Report.objects. \
			filter(user=request.user.pk). \
			filter(date__range=(start_date, end_date)). \
			order_by('date')
	except Report.DoesNotExist:
		reports = None

	context = {
		'date': date,
		'reports': reports,
	}

	return render(request, 'reports/week.html', context)

@login_required(login_url='/stechuhr/login/')
def reports_month(request, year, month):
	try:
		date = datetime.date(int(year), int(month), 1)
	except:
		raise Http404

	try:
		report_objs = Report.objects. \
			filter(user=request.user.pk). \
			filter(date__month=int(month)). \
			order_by('date')
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
		'date': date,
		'reports': reports,
	}

	return render(request, 'reports/month.html', context)

def permission_denied(request):
	return HttpResponse('<h1>Permission denied (403)</h1>')


# vim: set ft=python ts=4 sw=4 :
