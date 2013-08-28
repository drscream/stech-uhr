# -*- coding: UTF-8 -*-

import datetime

def isoweek_startdate(year, week):
	startdate = datetime.datetime.strptime('%04d-%02d-1' % (year, week),
			'%Y-%W-%w')
	if datetime.date(year, 1, 4).isoweekday() > 4:
		startdate -= datetime.timedelta(days=7)
	return startdate

# vim: set ft=python ts=4 sw=4 :
