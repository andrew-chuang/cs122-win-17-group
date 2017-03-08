from django.shortcuts import render
from django.http import HttpResponse
import datetime


def search_form(request):
	return render(request, 'search_form.html')

def search(request):
	string = 'You searched for: {}'
	if 'n1' in request.GET:
		message1 = 'You searched for: %s' % request.GET['n1']
	if 'n2':
		pass
	else:
		message = 'You submitted an empty form.'
	return HttpResponse(message)


def current_datetime(request):
	now = datetime.datetime.now()
	return now

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "In %s hour(s), it will be  %s." % (offset, dt)
	dt

def current_future(request):
	now = current_datetime(request)
	fut = hours_ahead(request, 5)
	return render(request, 'current_future.html', {'current': now, 'future':now})
