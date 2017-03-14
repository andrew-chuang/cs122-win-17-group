# Arif-Chuang-Hori-Teehan

A project for CMSC 12200 - Computer Science with Applications II - University of Chicago

Authors: @salman-arif @andrew-chuang @jonathan-hori @rteehas

Hierarchy
- Project
	- algorithms
		- overlap.py
		- text_analysis.py
	- data - Jon
		- json_to_sql.py
	- django-workshop/mysite
	- google_api_groupwork
	- scraping
		- scraping.py
	- yelp_rec_django
	- final_project.py - MASTER FILE
	- requirements.txt - List of required libraries
- Preliminary
	- Arif-Chuang-Hori-Teehan Proposal.pdf
	- Outline of Yelp API
	- Yelp Restaurant Suggestion Queue.pptx
	- googleapiwork.txt
- .gitignore
- README.md - This file

Required APIs:
- Google Calendar
- Google Maps
- OAuth


Algorithms Overview:

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


