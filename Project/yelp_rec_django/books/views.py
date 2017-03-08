from django.shortcuts import render
from django.http import HttpResponse
import datetime


def search_form(request):
	return render(request, 'search_form.html')

def parse_search_inputs(request):
	terms = {}
	for i in request.GET:
		if (request.GET[i]):
			terms[str(i)] = str(request.GET[i])
	print(terms)
	return terms

def search(request):
	terms = parse_search_inputs(request)
	return render(request, 'page2.html', {'dict': terms})


def current_datetime(request):
	now = datetime.datetime.now()
	return render(request, 'current_datetime.html', {'current_date': now})

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
