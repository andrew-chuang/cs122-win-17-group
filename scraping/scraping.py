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
		self.address = biz.location.address[0] + \
			biz.location.city + biz.location.state_code
		self.review_count = biz.review_count
		self.rating = biz.rating
		self.url = biz.url.split('?')[0] + '?'


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

	biz = business(biz_id)

	if biz.review_count <= MAX_REVIEWS:
		pages = range(0, biz.review_count, 20)
	else:
		pages = range(0, MAX_REVIEWS, 20)


	for page in pages:
		url = biz.url + 'start={}'.format(page)
		
		html = pm.urlopen(url=url, method="GET").data
		soup = bs4.BeautifulSoup(html, "html.parser")

		# Only scraping English reviews
		'''
		reviews = soup.find_all('p', lang='en')
		review_dates = soup.find_all('span', class_="rating-qualifier")
		'''

		rev_data = soup.find_all('div', itemprop='review')
		users = soup.find_all('div', class_='review review--with-sidebar')

		date_list = []

		for i in range(0, len(rev_data)):
			review_dict = {}

			review_dict['text'] = rev_data[i].find('p', \
				itemprop='description').text.strip()

			review_dict['date'] = rev_data[i].find('meta', \
				itemprop='datePublished')['content']

			stars = rev_data[i].find('meta', itemprop='ratingValue')['content']
			review_dict['stars'] = float(stars)

			review_dict['user_id'] = users[i]['data-signup-object'].split(':')[1]

			review_list.append(review_dict)
			'''
			if len(date.attrs['class']) > 1:
				continue 

			is_updated = date.find_all('small')
			if is_updated:
				if is_updated[0].text == 'Previous review':
					continue 
				else:
					date_list.append(date.text.strip().split('\n')[0])
			else:
				date_list.append(date.text.strip())



		for i in range(0, len(reviews)):

			review_dict = {}				


			rev_text = reviews[i].get_text(separator=' ')

			review_dict['text'] = rev_text

			review_dict['date'] = date_list[i]

			review_list.append(review_dict)
		'''

	return review_list




def scrape_user_reviews(user_id):
	'''
	Given a user ID, scrapes all of the user's reviews. Includes: 
		user ID, date, business ID, stars, text. 

	Returns: List of dictionaries, each dictionary containing information 
		for one review. 
	'''
	pass


def scrape_biz_attributes():
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

