# -*- coding: UTF-8 -*-

from datetime import date, timedelta

def first_day_isoweek(year, week):
	# The Jan 4th must be in week 1  according to ISO
	d = date(year, 1, 4)
	return d + timedelta(weeks=(week-1), days=-d.weekday())

def last_day_isoweek(year, week):
	return first_day_isoweek(year, week) + timedelta(days=6)

# vim: set ft=python ts=4 sw=4 :
