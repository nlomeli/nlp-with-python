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

# dependency parser visualization
# https://demos.explosion.ai/displacy/

# show sentences parsed into trees with verbs as base of trees
# grab those verbs out
# maybe groub out subject-relation-direct object triples

# doc1.similarity(doc2)

# list((w.text, w.pos_) for w in mr_doc)

# Multi-threading with .pipe()
# https://spacy.io/docs/usage/processing-text#multithreading
texts = [r['text'] for r in reviews]
for i, doc in enumerate(nlp.pipe(texts, batch_size=10000, n_threads=3)):
    reviews[i]['doc'] = doc



for r in reviews:
    print(r['title'])
    docs.append(nlp(r['text']))

g_rated = [r for r in reviews if r['mpaa_rating']=='G']
len(g_rated)
g_titles = {r['title']:r for r in g_rated}
for r in g_rated:
    print(r['title'])
    r['doc'] = nlp(r['text'])

mermaid_doc = g_titles['The Little Mermaid (1989)']['doc']
g_rated.sort(key=lambda r:r['doc'].similarity(mermaid_doc))
g_rated[-1]['title'] # The Little Mermaid (same)
g_rated[-2]['title'] # Aladdin
g_rated[-3]['title'] # Beauty And The Beast
g_rated[0]['title'] # Stormchasers
g_rated[1]['title'] # Microcosmos
g_rated[2]['title'] # Hubble 3D
# or
mermaid_like = [(mermaid_doc.similarity(r['doc']),r) for r in g_rated]
for sim_score, r in mermaid_like:
    print(sim_score, r['title'])

s = list(mermaid_docs.sents)[3]
s.root
list(s.root.children)

for sent in mermaid_doc.sents:
    print(sent.root)

# semantic similarity visualization
# https://demos.explosion.ai/sense2vec/?word=natural%20language%20processing&sense=auto

# could create matrix of similarities ... would take a long time
# with matrix, could find most similar/disimilar pairs in a bunch
# could collect disaster movies (23) to find these matches

# pull out different types of named entities
# aggregate named entities across reviews
# look at aggregates of different types of named entities across corpus


# NER visualization
# https://demos.explosion.ai/displacy-ent/
