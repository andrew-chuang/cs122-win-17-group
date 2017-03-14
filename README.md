# Arif-Chuang-Hori-Teehan

A project for CMSC 12200 - Computer Science with Applications II - University of Chicago

Authors: @salman-arif @andrew-chuang @jonathan-hori @rteehas

## Hierarchy
- Project
	- yelp_app
		- algorithms
			- overlap.py
			- text_analysis.py
		- data
			- json_to_sql.py
		- google_api_groupwork
			- g_cal.py
			- g_maps.py
		- scraping
			- scraping.py
		- templates
		- yelp_app
		- yelp_rec_django
		- final_project.py
		- config_secret.json
		- db.sqlite3
		- final_project.py
		- manage.py
	- requirements.txt
- Preliminary
	- Arif-Chuang-Hori-Teehan Proposal.pdf
	- Outline of Yelp API
	- Yelp Restaurant Suggestion Queue.pptx
	- googleapiwork.txt
- .gitignore
- README.md - This file

## Required APIs:
- Google Calendar
- Google Maps
- OAuth
- Yelp

## How to Run:
- Navigate to Project/yelp_app
- Run `python3 manage.py runserver`
- In a browser window, navigate to `127.0.0.1:8000`
- Enter your desired restaurant with location (city, state, zip code, address)
- Select your intended restaurant
- Your recommendation list should appear. At the bottom of the page, you may select a 
	restaurant to view its details.
	
## Yelp Scraper:

Main file: scraping.py. All other files are backups or copies I kept in case certain things broke. 

Scrapes data from Yelp Business page and then from each User's page. Ensures reviews are not double-scraped. Makes use of Yelp API in Business Class. 

Uses two important constants: 
- MAX_BIZ_REV: How many reviews to scrape from business page
- MAX_USER_REV: How many reviews to scrape from each user page

These are currently set to 10 and 15, respectively, in order to keep runtimes on the lower end. We tested up to 30 x 30, but this took several minute even when running in native macOS. 

Additional constants: 
- THREAD_SIZE: How many parallel requests to send for multiprocessing (set to 3 to avoid getting blocked)
- HEADER: Header used fur HTTP requests
- DEBUG: True causes the program to run in 'verbose' mode, printing out each step as it occurs to the terminal. We are leaving this on False for our submission, but it is very useful to ensure that things are occurring because it can take several minutes for recommendations to load. 

## Converting Data:

To manage the data scraped form Yelp, we import all data into a SQLITE3 database. This 
database has several tables:
- business
	- business_id
- biz_reviews
	- business_id
	- stars
	- text
	- user_id
- user_reviews
	- business_id
	- stars
	- text
	- user_id

## Algorithms Overview:

There are 3 algorithms used in this section. There is a simple algorithm that 
determines how many times a restaurant appears in the user reviews, which are 
all highly reviewed. It then normalizes this number. 

We also have an algorithm that returns an average similarity score using Latent 
Semantic Indexing. The algorithm takes reviews from the input restaurants as 
training data and then compares each review in the user reviews, grouped into 
blocks of text by restaurant, for similarity. This yields a list of similarity 
scores, which we then average. 

Finally, there is a sentiment scoring algorithm. We first determine the average 
sentiment score of the reviews from the input restaurants to use as a baseline.
We want to give extra emphasis to restaurants whose reviews in user_reviews are 
more positive than the reviews for the input restaurants. We then determine the
sentiment score of the reviews in the user reviews, grouped as in the sentiment 
scoring and subtract the baseline score to get the sentiment score. 

These are then weighted to give more emphasis to similarity scoring than 
sentiment scoring, and more emphasis to their sum than to the overlap score.

overlap.py:

Counts the number of times that a review appears in the user reviews dataframe

text_analysis.py:

Contains all the functions for sentiment analysis and LSI


## Google API Overview:

Three files:
    g_maps.py: This file contains all functions directly calling on the 
        Google Maps, Directions, Static Maps and Places APIs. 
    g_calendar.py: This file contains all functions calling on the
        Google Calendars API. This file also utilizes the Google OAuth API
        that allows the project to 
    client_secrets.json: This file contains a JSON collection of private
        details that holds the API key and Client Keys. 

This project utilized three main Google APIs: Maps, Calendars and Places. Within
both main files, we also used the OAuth API to connect to the users' accounts and
send editing requests to the Users' Calendars. 

The Google Maps file is the bulk of the functions that utilize Google APIs. 
We utilize Google Directions to provide directions between two locations, 
possibly allowing the user to request directions between 
two recommended restaurants. Google's Static Maps API allows us 
to construct Google URLs that are later put between IMG tags. 
These IMG tags are later used in the Django site to directly
display maps with markers indicating the location of restaurants. 
Other auxiliary functions include a function that parses details from
the Places Object returned from the Places API as well as a
latitude and longitude finder. 

The Google Calendar file was slated to hold credential requests from the
Google OAuth API as well as functions that would interact with the 
calendar of a user. Most of the functions in this file are not 
actually used by the Django site, but they are functional. 
These functions include the OAuth Token Credential initalization, 
adding an additional "Yelp Calendar" to the list of calendars of the user,
as well as an event inserter to the user's calendar. 











