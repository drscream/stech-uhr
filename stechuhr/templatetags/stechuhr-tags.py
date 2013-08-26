import datetime
import markdown

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='append')
@stringfilter
def append(value, arg):
	if value and value != 'None':
		return '%s%s' % (value, arg)
	else:
		return ''

@register.filter(name='leading_zero')
def leading_zero(value):
	return '%02d' % (int(value))

@register.filter(name='md')
def md(value):
	return markdown.markdown(value)

# vim: set ft=python ts=4 sw=4 :
