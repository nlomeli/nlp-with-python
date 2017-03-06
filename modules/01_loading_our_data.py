import os
import sys
import json
import random

try:
    directory = sys.args[1]
except:
    directory = '../review_json/'

file_names = os.listdir(directory)
reviews = [json.loads(open(directory+fn, 'r').read()) for fn in file_names]
reviews.sort(key=lambda r:len(r['text'])) # sort by length of review
reviews = reviews[5:] # get rid of 5 shortest reviews
for r in reviews:
    r.pop('by') # remove 'by' field in each review

reviews.sort(key=lambda r:r['release_year']) # sort by release_year

def display(r):
    print("""
    Review: %s
    ------------------------------
    Title: %s
    Release year: %s
    Running time: %s
    MPAA rating: %s
    Genres: %s
    Star rating: %s
    Date Published: %s
    Review URL: %s
    """ % (
    r['text'],r['title'],r['release_year'],r['running_time'],r['mpaa_rating'],
    ', '.join(r['genres']) if r['genres'] else 'N/A',
    r['star_rating'],r['date_published'],r['url']
    ))

####

type(reviews) # list
reviews[:5]
reviews[-5:]
len(reviews) # 7734
type(reviews[0]) # dict
reviews[0] # oldest movie by release year
reviews[-1] # newest movie by release year
random.choice(reviews)
r = random.choice(reviews)
sorted(r) # alphabetical list of review fields
r # review object
r['title']
print(r['text'])
display(r) # custom printed view
display(random.choice(reviews)) # repeat to view random reviews

# read some excerpts
# visit a couple links

# let's write our own movie search function
def search(q, reviews):
    matches = {}
    for r in reviews:
        title = r['title']
        if q.lower() in title.lower():
            matches[title] = r
    return matches

love_movies = search('love', reviews)
sorted(love_movies) # alphabetical list of titles
war_movies = search('war', reviews)
sorted(results)
results['The Fog of War (2004)']

# let's organize our data into a dictionary for easier access
titles = {r['title']:r for r in reviews} # dictionary of reviews by title
type(titles)
sorted(titles)
titles['Chinatown'] # >>> titles['My Movi... [TAB] for autocompletion
titles['The Big Lebowski (1998)']
len(titles) # yup, 7734 of them
mr = titles['Minority Report (2002)'] # titles['Minor[TAB]...
display(mr)
