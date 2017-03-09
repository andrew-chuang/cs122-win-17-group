# CS 122 Win 17 
# Arif-Chuang-Hori-Teehan
# Yelp Recommender Scraping 
#
#
#


import bs4
import urllib3
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from multiprocessing.pool import ThreadPool

MAX_BIZ_REV = 2
MAX_USER_REV = 2
THREAD_SIZE = 3
HEADER = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) \
	#AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

DEBUG = True

# Suppress warning output from urllib3
urllib3.disable_warnings()
# Set number of connections in order to use threading/pooling
pm = urllib3.PoolManager(num_pools=5, maxsize=10)

# read API keys for Yelp
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

#########################################################################
#------------------------------------------------------------------------
#---------------------------- BUSINESS CLASS ----------------------------
#------------------------------------------------------------------------
#########################################################################

class business:
	'''
	Class holds some basic information about a business. Also scrapes the
		attributes of business as listed on Yelp.
	'''

	def __init__(self, business_id, attr=False):
		'''
		Initialization uses the Yelp API to obtain the name, address, review count, 
		rating, url and attributes of a business. 

		Inputs:
		    business_id (string) Yelp specific id for a business
		    attr: indicates whether or not to scrape the attributes. 
		'''
		if DEBUG:
			print('Making business...', business_id)

		biz = client.get_business(business_id).business
		
		self.name = biz.name
		self.business_id = biz.id

		# Sometimes businesses don't have a proper address?
		if biz.location.address:
			self.address = ' '.join((biz.location.address[0], 
				biz.location.city, biz.location.state_code))
		else: 
			self.address = ' '.join((biz.location.city, 
				biz.location.state_code))
		
		self.review_count = biz.review_count
		self.rating = biz.rating
		self.url = biz.url.split('?')[0] + '?'
		self.attributes = {}
		if attr:
			self.scrape_biz_attributes()


	def scrape_biz_attributes(self):
		'''
		Method scrapes restaurant attributes 
		(ex: takes reservations, delivery, parking, etc)
			and adds them to the business instance. 

		No explicit inputs or outputs;
		    Method makes adjustments solely to the
		    class attributes.
		'''
		html = pm.urlopen(url=self.url, method="GET", headers=HEADER).data
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


#########################################################################
#------------------------------------------------------------------------
#------------------------------- FUNCTIONS ------------------------------
#------------------------------------------------------------------------
#########################################################################


def find_intended_restaurant(name, loc):
	'''
	Returns the top 4 results given by the Yelp Search API for the given
		restaurant name and location (neighborhood, city, zip, etc).

	This is used to determine and verify which restaurant(s) the user 
	    intended to input, because we cannot programmatically 
	    convert a name to a business ID. This function is directly used
	    in the Django yelp_app/views.py file. 

	Inputs:
		name: (string) restaurant name inputted by user (medici, harolds, etc)
		loc: some location identifier (city, zip, etc)

	Outputs:
	    results (Yelp object) contains top 4 results given by Yelp Search API
	'''
	name = str(name)
	location = str(loc)
	results = []

	matches = client.search(term=name, location=loc, limit=2).businesses

	for biz in matches:
		addr = ' '.join((biz.location.address[0], 
			biz.location.city, biz.location.state_code))

		business = business(biz)
		results.append((business.name, business.address, business.business_id))

	return results



def scrape_biz_reviews(business_id):
	'''
	Given a business ID, scrapes up to MAX_BIZ_REV reviews for the business. 
	Only scrapes 'positive' reviews - reviews at/above the business's
		average rating. 

	Inputs:
        business_id (string): unique Yelp ID identifier for each business
	Outputs: 
	    (Tuple)
		1: The business ID
		2: List of dictionaries, each dictionary containing information
			for one review. Includes: user ID, date, stars, text. 
		3: Set containing all of the user IDs and their review counts
			corresponding to the scraped reviews, as well as the 
			business ID that led to their review (which is the same as input). 
	Example: reviews = scrape_biz_reviews('medici-on-57th-chicago')
	'''
	if DEBUG:
		print('\n######### NEW BIZ ', business_id, '##########')

	review_list = []
	user_set = set()

	biz = business(business_id)
	threshold = biz.rating // 1
	pages = range(0, biz.review_count, 20)

	for page in pages:
		url = biz.url + 'start={}'.format(page)
		
		html = pm.urlopen(url=url, method="GET", headers=HEADER).data
		soup = bs4.BeautifulSoup(html, "html.parser")

		rev_data = soup.find_all('div', itemprop='review')
		users = soup.find_all('div', class_='review review--with-sidebar')
		user_rev_num = soup.find_all('ul', class_="user-passport-stats")
		
		if DEBUG:
			print('--------SCRAPING BIZ PAGE--------')

		for i in range(0, len(rev_data)):
			review_dict = {}

			stars = float(rev_data[i].find('meta', 
				itemprop='ratingValue')['content'])

			if stars >= threshold:

				review_dict['business_id'] = biz.business_id

				review_dict['text'] = rev_data[i].find('p', \
					itemprop='description').text.strip()

				#review_dict['date'] = rev_data[i].find('meta', \
					#itemprop='datePublished')['content']

				review_dict['stars'] = float(stars)

				user_id = users[i]['data-signup-object'].split(':')[1]
				review_dict['user_id'] = user_id

				user_num = user_rev_num[i].find('li', \
					class_="review-count responsive-small-display-inline-block")
				user_num = int(user_num.text.strip().split(' ')[0])

				user_set.add((user_id, user_num, biz.business_id))

				review_list.append(review_dict)
				
				if DEBUG:
					print('XXXXX SCRAPED REVIEW FROM ', user_id)
				
				if len(review_list) >= MAX_BIZ_REV:
					return biz.business_id, review_list, user_set 
	
	return biz.business_id, review_list, user_set 



def scrape_user_reviews(user_id, count, biz_ref = None):
	'''
	Given a user ID, scrapes up to MAX_USER_REV of the user's reviews. 
	Only scrapes reviews with 4 or 5 stars. Uses multiprocessing to save time.

	Inputs:
		user_id: string, unique to each Yelp user
		count: how many reviews that user has made. This is found in
			scrape_biz_reviews. 
		biz_ref: the business ID from which this user ID was kept. Found
			in scrape_biz_reviews

	Returns: List of dictionaries, each dictionary containing information 
		for one review. Includes: user ID, business ID, stars, text. 

	Example: usr_rev = scrape_user_reviews('29buG-NLQkLHwz8B2Newcw', 338)
	'''
	review_list = []
	url = 'https://www.yelp.com/user_details_reviews_self?'\
	'userid={}&review_sort=rating&rec_pagestart={}'


	pages = range(0, count, 10)

	# Create a list of lists of 5 URLs to use for multiprocessing. 
	urls = [url.format(user_id, i) for i in pages]
	urls = [urls[i:i+THREAD_SIZE] for i in range(0, len(urls), THREAD_SIZE)]

	for url_set in urls:
		soups = ThreadPool(5).imap(fetch_soup, url_set)

		for soup in soups:
			rev_data = soup.find_all('div', class_='review-content')
			
			if DEBUG:
				print('\n========== SCRAPING USER ', user_id, ' ##########')

			for i in range(1, len(rev_data), 2):
				review_dict = {}

				stars = float(rev_data[i].find_all('div', 
					class_='i-stars')[0]['title'].split(' ')[0])

				if stars > 3.0:
					text = rev_data[i].find_all('p', 
							lang='en')
					business_id = soup.find_all('a', 
						class_='biz-name')[(i-1)//2]['href'].split('/')[2]

					if text and biz_ref != business_id:
						review_dict['text'] = text[0].text

						review_dict['user_id'] = user_id

						review_dict['business_id'] = business_id

						review_dict['stars'] = stars
						
						review_list.append(review_dict)
						
						if DEBUG:
							print(review_dict['business_id'], review_dict['stars'])
					
						if len(review_list) >= MAX_USER_REV:
							return review_list
	return review_list


def fetch_soup(url):
	'''
	Fetches the soup for a given URL. Helper function created 
		in order to use threading/pooling. 
	'''
	html = pm.urlopen(url=url, method='GET', headers=HEADER).data
	soup = bs4.BeautifulSoup(html, "html.parser")
	return soup



##########################################################################
#---------------------------- UNUSED FUNCTIONS ---------------------------
#
#		Wrote these and had been using them but it was easier to 
#		obtain most of this information through the Yelp API. 
#
##########################################################################

def scrape_biz_basics(business_id):
	'''
	Given a business ID, scrapes basic information. 

	Inputs: 
	    business_id (string): unique identifier for each Yelp Business

	Outputs:
	    address
	    review_count
	    agg_rating
	'''
	biz_url = make_url(business_id = business_id)

	html = pm.urlopen(url=biz_url, method="GET", headers=HEADER).data
	soup = bs4.BeautifulSoup(html, "html.parser")

	address = soup.find_all('address')[1].text.strip()

	aggregate_info = soup.find_all('div', itemprop='aggregateRating')[0]

	review_count = int(aggregate_info.text.strip())
	
	agg_rating = aggregate_info.find('meta')['content']
	agg_rating = float(agg_rating)

	return (address, review_count, agg_rating)


def make_url(business_id=None, user_id=None):
	'''
	Constructs the URL for either a business page or a user's page
	through string formatting. Yelp URLs are highly standardized, 
	which allows URL construction through concatenation. 

	Inputs:
		EITHER business_id or user_id, strings

	Output:
        url (string) url of either business or user, depending
        on the input to the function. 
	'''
	if business_id:
		url = 'https://www.yelp.com/biz/{}?'.format(business_id)

	elif user_id:
		url = 'https://www.yelp.com/user_details_reviews_self?'\
		'userid={}&rec_pagestart=0'.format(user_id)

	return url

