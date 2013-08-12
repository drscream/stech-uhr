import datetime

from django import template

register = template.Library()

@register.filter(name='leading_zero')
def leading_zero(value):
	return '%02d' % (int(value))


# vim: set ft=python ts=4 sw=4 :
