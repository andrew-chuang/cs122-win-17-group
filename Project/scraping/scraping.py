import bs4
import urllib3
import json
import re
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

MAX_REVIEWS = 50

pm = urllib3.PoolManager()

# read API keys
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

# client = Client(auth)

class business:

	def __init__(self, biz_id):
		'''
		Uses the Yelp API to obtain basic information about a business. 
		'''
		biz = client.get_business(biz_id).business
		
		self.biz_name = biz.name
		self.biz_id = biz.id
		#self.address = biz.location.address[0] + \
			#biz.location.city + biz.location.state_code
		self.address = ' '.join((biz.location.address[0], 
			biz.location.city, biz.location.state_code))
		self.review_count = biz.review_count
		self.rating = biz.rating
		self.url = biz.url.split('?')[0] + '?'
		self.attrs = {}
		self.scrape_biz_attributes()


	def scrape_biz_attributes(self):
		url = self.url
		
		html = pm.urlopen(url=url, method="GET").data
		soup = bs4.BeautifulSoup(html, "html.parser")

		attrs = soup.find_all('dt', class_='attribute-key')[2:]

		for attr in attrs:
			attribute = attr.text.strip()
			value = attr.find_next().text.strip()
			
			if value == 'Yes':
				value = True
			elif value == 'No':
				value = False

			self.attrs[attribute] = value


def find_intended_restaurant(name, loc):
	'''
	Returns the top 5 results given by the Yelp Search API for the given
		restaurant name and location (neighborhood, city, zip, etc).
	'''
	name = str(name)
	location = str(loc)

	results = client.search(term=name, location=loc, limit=4).businesses

	return results



def scrape_biz_reviews(biz_id):
	'''
	Given a business ID, scrapes all reviews for the business. Includes:
		user ID, date, stars, text. 

	Returns: List of dictionaries, each dictionary containing information
		for one review. 

	Example usage: reviews = scrape_biz_reviews('medici-on-57th-chicago')
	'''
	review_list = []
	user_set = set()

	biz = business(biz_id)
	threshold = biz.rating // 1
	pages = range(0, biz.review_count, 20)

	for page in pages:
		url = biz.url + 'start={}'.format(page)
		
		html = pm.urlopen(url=url, method="GET").data
		soup = bs4.BeautifulSoup(html, "html.parser")

		rev_data = soup.find_all('div', itemprop='review')
		users = soup.find_all('div', class_='review review--with-sidebar')

		date_list = []

		for i in range(0, len(rev_data)):
			review_dict = {}

			stars = float(rev_data[i].find('meta', 
				itemprop='ratingValue')['content'])
			if stars >= threshold:

				review_dict['biz_id'] = biz.biz_id

				review_dict['text'] = rev_data[i].find('p', \
					itemprop='description').text.strip()

				review_dict['date'] = rev_data[i].find('meta', \
					itemprop='datePublished')['content']

				review_dict['stars'] = float(stars)

				user_id = users[i]['data-signup-object'].split(':')[1]
				review_dict['user_id'] = user_id
				user_set.add(user_id)

				review_list.append(review_dict)
				
				if len(review_list) >= MAX_REVIEWS:
					return biz.__dict__, review_list, user_set 



def scrape_user_reviews(user_id):
	'''
	Given a user ID, scrapes all of the user's reviews. Includes: 
		user ID, date, business ID, stars, text. 

	Returns: List of dictionaries, each dictionary containing information 
		for one review. 
	'''
	pass


def scrape_biz_basics(biz_id):
	'''
	Given a business ID, scrapes basic information. 
	'''
	biz_url = make_url(biz_id = biz_id)

	html = pm.urlopen(url=biz_url, method="GET").data
	soup = bs4.BeautifulSoup(html, "html.parser")

	address = soup.find_all('address')[1].text.strip()

	aggregate_info = soup.find_all('div', itemprop='aggregateRating')[0]

	review_count = int(aggregate_info.text.strip())
	
	agg_rating = aggregate_info.find('meta')['content']
	agg_rating = float(agg_rating)


	return (address, review_count, agg_rating)

def make_url(biz_id=None, user_id=None):
	'''
	Constructs the URL for either a business page or a user's page.

	Inputs:
		EITHER biz_id or user_id, strings
	'''
	if biz_id:
		url = 'https://www.yelp.com/biz/{}?'.format(biz_id)

	elif user_id:
		url = 'https://www.yelp.com/user_details_reviews_self?'\
		'userid={}&rec_pagestart=0'.format(user_id)

	return url

