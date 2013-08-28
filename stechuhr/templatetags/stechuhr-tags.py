import datetime
import markdown
import re

from django import template
from django.template.defaultfilters import stringfilter
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

@register.filter(name='timeuntil_tdelta')
def timeuntil_tdelta(tdelta):
	if not isinstance(tdelta, datetime.timedelta):
		raise TemplateSyntaxError("invalid timedelta object")
	return timeuntil(datetime.datetime.now() + tdelta)

@register.filter(name='tdelta_beautify')
def tdelta_beautify(tdelta, limit="h"):
	if not isinstance(tdelta, datetime.timedelta):
		raise TemplateSyntaxError("invalid timedelta object")
	if limit not in ["d","h","m","s"]:
		return ""

	re.findall("([0-9]+)", str(t))

	return tdelta


# vim: set ft=python ts=4 sw=4 :
