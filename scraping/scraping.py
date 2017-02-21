import bs4
import urllib3
import json
pm = urllib3.PoolManager()

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

# read API keys
with open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)

client = Client(auth)



url = 'https://www.yelp.com/biz/au-cheval-chicago'

html = pm.urlopen(url=url, method="GET").data

soup = bs4.BeautifulSoup(html, "html.parser")

soup = soup.find_all('script', type="application/ld+json")

js = json.loads(soup[0].text)

with open('JSData.json', 'w') as f:
     json.dump(js, f)