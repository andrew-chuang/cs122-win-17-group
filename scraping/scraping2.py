# Imports
import string
from lxml import html
import requests
# Yelp unique url endings for each restaurant
RESTAURANTS = ['aquavit-new-york',
               'atera-new-york',
               'blanca-brooklyn',
               'daniel-new-york']
start_urls = [ 'http://www.yelp.com/biz/%s' % s for s in RESTAURANTS]
num_reviews = 2000 # Number of reviews you want
page_order = range(0, (num_reviews+1), 40)
review_dict = {}
for ur in start_urls:
    for o in page_order:
        page = requests.get(ur + ("?start=%s" % o))
        tree = html.fromstring(page.text)
        # This will extract the name of the business
        title = tree.xpath('//h1[@itemprop="name"]/text()')
        title = title[0].strip()
        # This will create a list of reviews
        reviews = tree.xpath('//p[@itemprop="description"]/text()')
        mod_reviews = []
        for rev in reviews:
            mod_rev = filter(lambda x: x in string.printable, rev)
            mod_reviews.append(mod_rev)

        # This will add the reviews to a dictionary
        if title in review_dict:
            review_dict[title] += mod_reviews
        else:
            review_dict[title] = mod_reviews