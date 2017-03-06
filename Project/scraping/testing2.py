from multiprocessing.pool import ThreadPool
import urllib3
import bs4

MAX_USER_REV = 15

pm = urllib3.PoolManager(num_pools=5, maxsize=10)
urllib3.disable_warnings()

########################################################################
########################################################################
#																	   
#			USED FOR TESTING THREADING OUTSIDE OF SCRAPING.PY
#		ALL OF THIS CODE IS IMPLEMENTED IN THE SCRAPING.PY FILE
#
########################################################################
########################################################################

def fetch_soup(url):
	'''
	Fetches the soup for a given URL. Helper function created 
		in order to use threading/pooling. 
	'''
	html = pm.urlopen(url=url, method='GET').data
	soup = bs4.BeautifulSoup(html, "html.parser")
	return soup


def scrape_user_reviews(user_id, count):

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