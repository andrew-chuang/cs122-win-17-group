from django.shortcuts import render
from django.http import HttpResponse
import datetime 
from scraping.scraping import find_intended_restaurant
import final_project
import google_api_groupwork.g_maps as gmaps


def parse_search_inputs(request):
	'''
	Reads the inputs from the search form and parses them into a 
		usable dictionary. 
	Returns: dictionary containing the search terms (n1, l1, ..., n4, l4)
		or None if no inputs provided. 
	'''
	terms = None
	if request.GET:
		terms = {}
		q = request.GET
		if q['n1']:
			terms['r1'] = (str(q['n1']), str(q['l1']))
		if q['n2']:
			terms['r2'] = (str(q['n2']), str(q['l2']))
		if q['n3']:
			terms['r3'] = (str(q['n3']), str(q['l3']))
		if q['n4']:
			terms['r4'] = (str(q['n4']), str(q['l4']))
	return terms


def search(request):
	errors = []
	now = current_datetime(request)
	terms = parse_search_inputs(request)
	matches = {}
	
	if terms is None:
		return render(request, 'search_form.html', {'time': now})
	
	elif not terms:
		errors.append('Please submit a name and location.')

	else:
		for rest in terms:
			if not (terms[rest][0] and terms[rest][1]):
				errors.append('Please submit an equal amount \
					of locations and restaurants.')
			else:
				matches[rest] = find_intended_restaurant(terms[rest][0], 
					terms[rest][1])
	
	if not errors:
		return render(request, 'page2.html', 
			{'inputs': terms, 'matches': matches})
	else:
		return render(request, 'search_form.html', {'time': now,
			'errors': errors})


def recs(request):
	q = request.GET
	user_input = []
	if not q:
		return render(request, 'search_form.html')
	
	for key in q:
		if key != 'v':
			user_input.append(str(q[key]))

	df = final_project.go(user_input, 'asdf.db')
	results = final_project.post_processing(df, int(q['v']))

	addresses = []
	for i in results:
		addresses.append(i.address)
	google_map = gmaps.static_mapper(addresses)
	print(type(google_map))
	#print(google_map)
	
	return render(request, 'recs.html', {'results': results, 'map': google_map})
	
def details(request):



	return render(request, 'details.html', {})

def current_datetime(request):
	'''
	Returns current date and time. 
	'''
	now = datetime.datetime.now()
	return now
