import datetime

from django import template

register = template.Library()

@register.tag(name='calendar_week')
def calendar_week(parser, token):
	return CurrentCalendarWeek()

class CurrentCalendarWeek(template.Node):
	def render(self, context):
		now = datetime.date.today()
		return now.isocalendar()[1]

# vim: set ft=python ts=4 sw=4 :
