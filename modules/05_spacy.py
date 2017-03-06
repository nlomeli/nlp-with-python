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
type(mr_doc) # spacy.tokens.doc.Doc
mr_doc.text
list(mr_doc.sents)
len(list(mr_doc.sents)) # 49
list(mr_doc)
len(mr_doc) # 1376 tokens
list(mr_doc)[:30]
type(mr_doc[0]) # spacy.tokens.token.Token
token = mr_doc[0]
# dependency parser visualization
# https://demos.explosion.ai/displacy/
# enter:
# At a time when movies think they have to choose between action and ideas, Steven Spielberg's "Minority Report" is a triumph--a film that works on our minds and our emotions.

# token.[TAB] to see ways to navigate the grammatical tree of the sentence
token.pos_
token.head # is
list(token.children) # time
token.lemma # 507--a unique identifier for this word in the spaCy English vocab

# explore other sentences in the dependency visualizer

# let's break down nlp() into its component parts
mr_doc = nlp.tokenizer(mr_text) # parses into spacy.tokens.token.Token objects
nlp.tagger(mr_doc) # pos tagger
nlp.parser(mr_doc) # dependency parser
nlp.entity(mr_doc) # entity recongizer

# lots of processing is done with a simple call to nlp()
list((tok.text, tok.pos_) for tok in mr_doc) # tokens with their pos
list(mr_doc.noun_chunks)
for sent in mr_doc.sents:
    print(sent.orth_)
    print(sent.root)
    print('')
mr_doc.ents

# built-in entity types
# https://spacy.io/docs/usage/entity-recognition
entity = mr_doc.ents[0]
entity.orth_ # orthographic representation "Steven Spielberg's"
entity.label_ # 'PERSON'
entities = [e for e in mr_doc.ents]
people = [e for e in entities if e.label_=='PERSON']
artworks = [e for e in entities if e.label_=='WORK_OF_ART']
dates = [e for e in entities if e.label_=='DATE'] # error: 'mid-air'

# Named Entity Recognition (NER) visualization
# https://demos.explosion.ai/displacy-ent/

# let's process multiple docs
# doing all of them will take forever:
#for r in reviews:
#    print(r['title'])
#    docs.append(nlp(r['text']))

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

# let's see everything
mermaid_like = [(mermaid_doc.similarity(r['doc']),r) for r in g_rated]
for sim_score, r in mermaid_like:
    print(sim_score, r['title'])

# semantic similarity visualization
# https://demos.explosion.ai/sense2vec/?word=natural%20language%20processing&sense=auto

# could create matrix of similarities ... would take a long time
# with matrix, could find most similar/disimilar pairs in a bunch
# could collect disaster movies (23) to find these matches

# named entities:
# pull out different types of named entities
# aggregate named entities across reviews
# look at aggregates of different types of named entities across corpus

# knowledge extraction
# extract groups of subject-relation-direct object triples
