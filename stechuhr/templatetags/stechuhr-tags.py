import datetime
import markdown

from django import template
from django.template.defaultfilters import stringfilter, pluralize
from django.template.base import TemplateSyntaxError

from django.utils.timesince import timesince, timeuntil

register = template.Library()

@register.filter(name='append')
@stringfilter
def append(value, arg):
	if value and value != 'None':
		return '%s%s' % (value, arg)
	else:
		return ''

@register.filter(name='md')
def md(value):
	return markdown.markdown(value)

@register.filter(name='timeelapsed')
def timeelapsed(delta, unit='h'):

	if not isinstance(delta, datetime.timedelta):
		raise TemplateSyntaxError('invalid timedelta object')

	if unit not in ['d', 'h', 'w']:
		return ''

	if delta.days <= 0 and delta.seconds <= 60:
		return '0 minutes'

	if unit == 'w':
		days = delta.days
		weeks, days = divmod(days, 7)
		since = delta.seconds
	if unit == 'd':
		weeks = 0
		days = delta.days
		since = delta.seconds
	if unit == 'h':
		weeks = 0
		days = 0
		since = delta.days * 24 * 60 * 60 + delta.seconds

	hours, remainder = divmod(since, 3600)
	minutes, seconds = divmod(remainder, 60)

	slices = (
		('week', weeks),
		('day', days),
		('hour', hours),
		('minute', minutes),
	)

	elapsed = ''
	for unit, num in slices:
		if num > 0:
			elapsed = "%s %d %s%s" % (elapsed, num, unit, pluralize(num))

	return elapsed.strip()

# vim: set ft=python ts=4 sw=4 :
