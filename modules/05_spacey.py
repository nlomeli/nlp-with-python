import os
import sys
import json
from collections import Counter

try:
    directory = sys.args[1]
except:
    directory = '../review_json/'

def load_reviews(directory):
    file_names = os.listdir(directory)
    reviews = [json.loads(open(directory+fn, 'r').read()) for fn in file_names]
    reviews.sort(key=lambda r:len(r['text'])) # sort by length of review
    reviews = reviews[5:] # get rid of 5 shortest reviews
    for r in reviews:
        r.pop('by') # remove 'by' field in each review
    return reviews

reviews = load_reviews(directory)
reviews.sort(key=lambda r:r['release_year']) # sort by release_year
titles = {r['title']:r for r in reviews} # dict of reviews by title

####

import spacy
nlp = spacy.load('en') # takes time

mr = titles['Minority Report (2002)']
mr_text = mr['text']
mr_doc = nlp(mr_text)
list(mr_doc)[:30]

mr_doc = nlp.tokenizer(mr_text) # parses into spacy.tokens.token.Token objects
nlp.tagger(mr_doc) # pos tagger
nlp.parser(mr_doc) # dependency parser
nlp.entity(mr_doc) # entity recongizer

# doc1.similarity(doc2)

# list((w.text, w.pos_) for w in mr_doc)
