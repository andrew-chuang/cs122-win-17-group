import bs4
import urllib3
pm = urllib3.PoolManager()


def a():

	url = 'https://www.yelp.com/biz/au-cheval-chicago'

	html = pm.urlopen(url=url, method="GET").data

	soup = bs4.BeautifulSoup(html, "html.parser")

	soup = soup.find_all('script', type="application/ld+json")

	return soup