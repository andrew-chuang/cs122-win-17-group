import bs4
import urllib3
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from multiprocessing.pool import ThreadPool

MAX_BIZ_REV = 50
MAX_USER_REV = 15

# Supress warning output from urllib3
urllib3.disable_warnings()
# Set number of connections in order to use threading
pm = urllib3.PoolManager(num_pools=5, maxsize=10)

# read API keys for Yelp
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

##########################################################################
############################# BUSINESS CLASS #############################
##########################################################################

class business:
	'''
	Holds some basic information about a business. Also scrapes the
		attributes of business as listed on Yelp.
	'''

	def __init__(self, business_id):
		'''
		Uses the Yelp API to obtain basic information about a business. 
		'''
		biz = client.get_business(business_id).business
		
		self.name = biz.name
		self.business_id = biz.id
		self.address = ' '.join((biz.location.address[0], 
			biz.location.city, biz.location.state_code))
		self.review_count = biz.review_count
		self.rating = biz.rating
		self.url = biz.url.split('?')[0] + '?'
		self.attributes = {}
		self.scrape_biz_attributes()


	def scrape_biz_attributes(self):
		'''
		Scrapes attributes (ex: takes reservations, delivery, parking, etc)
			and adds them to the business instance. 
		'''
		html = pm.urlopen(url=self.url, method="GET").data
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


##########################################################################
############################### FUNCTIONS ################################
##########################################################################


def find_intended_restaurant(name, loc):
	'''
	Returns the top 4 results given by the Yelp Search API for the given
		restaurant name and location (neighborhood, city, zip, etc).

	This is used to determine which restaurant(s) the user 'likes', 
		because we cannot programmatically convert a name to a business ID.

	Inputs:
		name: string inputted by user (medici, harolds, etc)
		loc: some location identifier (city, zip, etc)
	'''
	name = str(name)
	location = str(loc)

	results = client.search(term=name, location=loc, limit=4).businesses

	return results



def scrape_biz_reviews(business_id):
	'''
	Given a business ID, scrapes up to MAX_BIZ_REV reviews for the business. 
	Only scrapes 'positive' reviews - reviews at/above the business's
		average rating. 

	Returns: Tuple
		1: biz.__dict__: namespace for the business, containing attributes
		2: List of dictionaries, each dictionary containing information
			for one review. Includes: user ID, date, stars, text. 
		3: Set containing all of the user IDs and their review counts
			corresponding to the scraped reviews. 
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
		user_rev_num = soup.find_all('ul', class_="user-passport-stats")

		print('----------------------')

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

				user_num = int(user_rev_num[i].find('b').text)

				user_set.add((user_id, user_num))

				review_list.append(review_dict)
				print('XXXXXXXXXXXXXXXXXXX', user_id)
				
				if len(review_list) >= MAX_BIZ_REV:
					return biz.__dict__, review_list, user_set 
	
	return biz.__dict__, review_list, user_set 



def scrape_user_reviews(user_id, count):
	'''
	Given a user ID, scrapes up to MAX_USER_REV of the user's reviews. 
	Only scrapes reviews with 4 or 5 stars. Uses threading to save time.

	Inputs:
		user_id: string, unique to each Yelp user
		count: how many reviews that user has made. This is found in
			scrape_biz_reviews. 
	
	Returns: List of dictionaries, each dictionary containing information 
		for one review. Includes: user ID, business ID, stars, text. 

	Example: usr_rev = scrape_user_reviews('29buG-NLQkLHwz8B2Newcw', 338)
	'''
	review_list = []

	url = 'https://www.yelp.com/user_details_reviews_self?'\
	'userid={}&review_sort=rating&rec_pagestart={}'

	pages = range(0, count, 10)

	urls = [url.format(user_id, i) for i in pages]
	urls = [urls[i:i + 5] for i in range(0, len(urls), 5)]

	for url_set in urls:
		soups = ThreadPool(5).imap(fetch_soup, url_set)

		for soup in soups:
			rev_data = soup.find_all('div', class_='review-content')

			print('==============================')
			for i in range(1, len(rev_data), 2):

				review_dict = {}

				stars = float(rev_data[i].find_all('div', 
					class_='i-stars')[0]['title'].split(' ')[0])

				if stars > 3.0:
					text = rev_data[i].find_all('p', 
							lang='en')

					if text:
						review_dict['text'] = text[0].text

						review_dict['user_id'] = user_id

						review_dict['business_id'] = soup.find_all('a', 
							class_='biz-name')[(i-1)//2]['href'].split('/')[2]

						review_dict['stars'] = stars
						
						review_list.append(review_dict)
						print(review_dict['business_id'], review_dict['stars'])	
					if len(review_list) >= MAX_USER_REV:
						return review_list
		return review_list


def fetch_soup(url):
	'''
	Fetches the soup for a given URL. Helper function created 
		in order to use threading/pooling. 
	'''
	html = pm.urlopen(url=url, method='GET').data
	soup = bs4.BeautifulSoup(html, "html.parser")
	return soup


##########################################################################
############################ UNUSED FUNCTIONS ############################
#
#		Wrote these and had been using them but it was easier to 
#		obtain most of this information through the Yelp API. 
#
##########################################################################
##########################################################################

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

