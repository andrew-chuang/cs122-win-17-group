import bs4
import urllib3
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

pm = urllib3.PoolManager()


# read API keys
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

client = Client(auth)

# restaurants as a list
#page_order = range(0, (num_reviews+1), 40)

class business:

	def __init__(self, biz_id):

		addr, count, rating = scrape_biz_basics(biz_id)
		self.biz_id = biz_id
		self.address = addr
		self.review_count = count
		self.rating = rating 


def find_intended_restaurant(name, loc):
	'''
	Returns the top 5 results given by the Yelp Search API for the given
		restaurant name and location (neighborhood, city, zip, etc).
	'''
	name = str(name)
	location = str(location)

	results = client.search(term=name, location=loc, limit=4)


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









'''
soup = soup.find_all('script', type="application/ld+json")

js = json.loads(soup[0].text)

with open('JSData.json', 'w') as f:
     json.dump(js, f)
'''