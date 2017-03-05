import os
import sys
import json

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

####

# inspect data
# look at breakdown of corpus
# quantity of movies by mpaa_rating, star_rating, etc.
# read some text excerpts
# visit a couple links
# write a function to search for a movie review by title:
#   search_string.lower() in review['title']



def search(q, reviews):
    matches = {}
    for r in reviews:
        title = r['title']
        if q.lower() in title.lower():
            matches[title] = r
    return matches

results = search('war', reviews)
sorted(results)
results['The Fog of War (2004)']

titles = {r['title']:r for r in reviews}
# >>> titles['Minor[TAB] for autocompletion
titles['Minority Report (2002)']
