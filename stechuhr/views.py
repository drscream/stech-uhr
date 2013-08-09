# -*- coding: UTF-8 -*-

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from stechuhr.models import UserProfile, WorkDay


def index(request):
	if request.user.is_authenticated():
		return redirect('user_dashboard')
	return render(request, 'index.html')

def signin(request):
	return render(request, 'signin.html')

@login_required(login_url='/stechuhr/login/')
def user_dashboard(request):
	return render(request, 'user/dashboard.html')

@login_required(login_url='/stechuhr/login/')
def user_settings(request):
	return HttpResponse('<h1>Settings</h1>')

def permission_denied(request):
	return HttpResponse('<h1>Permission denied (403)</h1>')


# vim: set ft=python ts=4 sw=4 :
