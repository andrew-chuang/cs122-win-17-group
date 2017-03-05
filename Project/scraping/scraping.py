import bs4
import urllib3
import json
import re
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
urllib3.disable_warnings()

MAX_REVIEWS = 50

pm = urllib3.PoolManager()

# read API keys
with open('scraping/config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

# client = Client(auth)

class business:

	def __init__(self, business_id):
		'''
		Uses the Yelp API to obtain basic information about a business. 
		'''
		biz = client.get_business(business_id).business
		
		self.name = biz.name
		self.business_id = biz.id
		#self.address = biz.location.address[0] + \
			#biz.location.city + biz.location.state_code
		self.address = ' '.join((biz.location.address[0], 
			biz.location.city, biz.location.state_code))
		self.review_count = biz.review_count
		self.rating = biz.rating
		self.url = biz.url.split('?')[0] + '?'
		self.attributes = {}
		self.scrape_biz_attributes()


	def scrape_biz_attributes(self):
		url = self.url
		
		html = pm.urlopen(url=url, method="GET").data
		soup = bs4.BeautifulSoup(html, "html.parser")

		attributes = soup.find_all('dt', class_='attribute-key')[2:]

		for attr in attributes:
			attribute = attr.text.strip()
			value = attr.find_next().text.strip()

			if value == 'Yes':
				value = True
			elif value == 'No':
				value = False

			self.attributes[attribute] = value


def find_intended_restaurant(name, loc):
	'''
	Returns the top 5 results given by the Yelp Search API for the given
		restaurant name and location (neighborhood, city, zip, etc).
	'''
	name = str(name)
	location = str(loc)

	results = client.search(term=name, location=loc, limit=4).businesses

	return results



def scrape_biz_reviews(business_id):
	'''
	Given a business ID, scrapes all reviews for the business. Includes:
		user ID, date, stars, text. 

	Returns: List of dictionaries, each dictionary containing information
		for one review. 

	Example usage: reviews = scrape_biz_reviews('medici-on-57th-chicago')
	'''
	review_list = []
	user_set = set()

	biz = business(business_id)
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

				review_dict['business_id'] = biz.business_id

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
		user ID, business ID, stars, text. 

	Returns: List of dictionaries, each dictionary containing information 
		for one review. 
	'''
	review_list = []
	url = 'https://www.yelp.com/user_details_reviews_self?'\
		'userid={}&rec_pagestart={}'

	html = pm.urlopen(url=url.format(user_id, 0), method="GET").data
	soup = bs4.BeautifulSoup(html, "html.parser")

	rev_count = soup.find_all('li', 
		class_='review-count')[0].text.strip().split(' ')[0]

	pages = range(0, int(rev_count), 10)

	for page in pages:
		html = pm.urlopen(url=url.format(user_id, page), method="GET").data
		soup = bs4.BeautifulSoup(html, "html.parser")

		rev_data = soup.find_all('div', class_='review-content')

		for i in range(1, len(rev_data), 2):
			review_dict = {}

			stars = float(rev_data[i].find_all('div', 
				class_='i-stars')[0]['title'].split(' ')[0])

			if stars > 3.0:
				review_dict['user_id'] = user_id

				review_dict['business_id'] = soup.find_all('a', 
					class_='biz-name')[(i-1)//2]['href'].split('/')[2]

				review_dict['stars'] = stars

				text = rev_data[i].find_all('p', 
					lang='en')
				if text:
					review_dict['text'] = text[0].text

				review_list.append(review_dict)

				#if len(review_list) >= MAX_REVIEWS:


	return review_list


def scrape_biz_basics(business_id):
	'''
	Given a business ID, scrapes basic information. 
	'''
	biz_url = make_url(business_id = business_id)

	html = pm.urlopen(url=biz_url, method="GET").data
	soup = bs4.BeautifulSoup(html, "html.parser")

	address = soup.find_all('address')[1].text.strip()

	aggregate_info = soup.find_all('div', itemprop='aggregateRating')[0]

	review_count = int(aggregate_info.text.strip())
	
	agg_rating = aggregate_info.find('meta')['content']
	agg_rating = float(agg_rating)


	return (address, review_count, agg_rating)

def make_url(business_id=None, user_id=None):
	'''
	Constructs the URL for either a business page or a user's page.

	Inputs:
		EITHER business_id or user_id, strings
	'''
	if business_id:
		url = 'https://www.yelp.com/biz/{}?'.format(business_id)

	elif user_id:
		url = 'https://www.yelp.com/user_details_reviews_self?'\
		'userid={}&rec_pagestart=0'.format(user_id)

	return url

