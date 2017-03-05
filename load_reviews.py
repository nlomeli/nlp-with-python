import os
import sys
import json

try:
    directory = sys.args[1]
except:
    directory = 'review_json/'

file_names = os.listdir(directory)

reviews = [json.loads(open(directory+fn, 'r').read()) for fn in file_names]

reviews.sort(key=lambda r:len(r['text'])) # sort by length of review
reviews = reviews[5:] # get rid of 5 shortest reviews

# remove 'by' field
for r in reviews:
    r.pop('by')

# MPAA rating
# ordered_ratings = ['G','PG','PG-13','R','X','NC-17','NR']
# rated_reviews = [r for r in reviews if r['mpaa_rating'] in ordered_ratings]
# rated_reviews.sort(key=lambda r:order_ratings.index(r['mpaa_rating']))

"""
Counter({'Action': 1572,
         'Adventure': 843,
         'Animation': 173,
         'Comedy': 2486,
         'Crime': 724,
         'Disaster': 23,
         'Documentary': 406,
         'Drama': 4008,
         'Eastern': 12,
         'Erotic': 8,
         'Family': 673,
         'Fantasy': 445,
         'Film Noir': 3,
         'Foreign': 1373,
         'History': 224,
         'Holiday': 25,
         'Horror': 393,
         'Indie': 726,
         'Music': 220,
         'Musical': 81,
         'Mystery': 439,
         'Neo-noir': 10,
         'Road Movie': 12,
         'Romance': 1620,
         'Science Fiction': 686,
         'Short': 1,
         'Sport': 36,
         'Sports Film': 107,
         'Suspense': 178,
         'Thriller': 1620,
         'War': 103,
         'Western': 101})
"""
