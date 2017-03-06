import os
import sys
import json

import nltk
from nltk.stem.porter import *
from collections import Counter, defaultdict
import random

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

mr = titles['Minority Report (2002)'] # the Minority Report review
mr
mr_text = mr['text']

# nltk is a language processing toolkit
# nltk?
# nltk.[TAB]... to explore the package

# let's analyze sentences
mr_sents = nltk.sent_tokenize(mr_text) # segment into sentences
# sort and display sentences by length
mr_sents.sort(key=lambda x:len(x)) # shortest to longest
mr_sents[:10]
mr_sents[-5:]
# note we can no longer recover the original order

nltk.word_tokenize(mr_sents[0]) # ['The', 'year', 'is', '2054', '.']
mr_tokens = nltk.word_tokenize(mr['text']) # not organized into sentences
mr_tokens

mr_sent_tokens = []
for sent in nltk.sent_tokenize(mr_text):
    sent_tokens = nltk.word_tokenize(sent)
    mr_sent_tokens.append(sent_tokens)

mr_sent_tokens[0]
mr_sent_tokens[-1]

# let's look at the nltk Text class, which wrappers a set of tokens
# nltk.Text?
""""
A wrapper around a sequence of simple (string) tokens, which is
intended to support initial exploration of texts (via the
interactive console).  Its methods perform a variety of analyses
on the text's contexts (e.g., counting, concordancing, collocation
discovery), and display the results.  If you wish to write a
program which makes use of these analyses, then you should bypass
the ``Text`` class, and use the appropriate analysis function or
class directly instead.
"""
mr_wrapper = nltk.Text(mr_tokens)
mr_wrapper.tokens

mr_wrapper.count('action') # counts tokens
mr_text.count('he') # if we don't have tokens, number of 'he' pronouns incorrect
mr_wrapper.count('he') # correct 'he' count
mr_text.count(' he ') # would miss "he's" and '--he' and 'he,' ... so not trivial

mr_vocab = mr_wrapper.vocab() # unique tokens with their counts
mr_vocab
mr_vocab.most_common(50)

mr_fdist = nltk.FreqDist(mr_wrapper)
mr_fdist.most_common(50) # same as mr_vocab.most_common(50)
mr_fdist.plot() # power law--some tokens vert common but most appear once

# ngrams are patterns of tokens with a window size of "n"
mr_bigrams = list(nltk.ngrams(mr_tokens, 2))
mr_bigrams
Counter(mr_bigrams).most_common(30) # most common adjacent token pairs
Counter(list(nltk.ngrams(mr_tokens, 3))).most_common(20) # trigrams less interesting here
Counter(list(nltk.ngrams(mr_tokens, 4))).most_common(20) # nor are quadgrams
# Google Books Ngram Viewer: https://books.google.com/ngrams
# try: "true love"

# Collocation
# A sequence of words or terms which co-occur more often than would be expected by chance.
# 'Crystal clear', 'middle management', 'nuclear family', and 'cosmetic surgery' are examples of collocated pairs of words"
mr_wrapper.collocations(num=20, window_size=2)
# concordance is a list of all the occurrences of a token with context
mr_wrapper.concordance('future')
mr_wrapper.concordance('action')
mr_wrapper.collocations(num=20, window_size=5)
mr_wrapper.concordance('term', width=200) # using the term "pre-crime"
mr_wrapper.concordance('spiders', width=200) # "spiders that can search"
# note that this is a very small sample of text on which to analyze collocations

# stemming: normalizing text
# stemming is good for finding the stem / base / root of a word form
# a series of if-then transformation rules are applied, typically
# from nltk.stem.porter import *
stemmer = PorterStemmer()
stemmer.stem('happens')
stemmer.stem('happened')
stemmer.stem('happening')
stemmer.stem('happenings')
stemmer.stem('happen') # can't be simplified
stemmer.stem('runnings') # works on made up words
stemmer.stem('lemmings') # 'lem' is an error--stemmer has no word knowledge
stemmer.stem('plead')
stemmer.stem('pled') # doesn't know this is same as 'plead'

sorted(set(mr_tokens)) # 553 unique tokens like 'year' and 'years'
# let's find the tokens that are altered by stemming:
stemmed = set([(tok, stemmer.stem(tok)) for tok in mr_tokens if stemmer.stem(tok) != tok]) # actually around 495 unique word stems
stemmed # 'worked', 'working', and 'works' become 'work'

# lemmatization with a vocabulary: WordNet
# lemmatization use a dictionary to reduce tokens to their base forms
lemmer = nltk.WordNetLemmatizer()
lemmatized = set([(tok, lemmer.lemmatize(tok)) for tok in mr_tokens if lemmer.lemmatize(tok) != tok])
lemmatized # tries -> try requires a dictionary

# let's find the set of unique stems, disregarding punctuation marks
mr_vocab = set([stemmer.stem(tok.lower()) for tok in mr_tokens if tok.isalpha()])
len(mr_vocab) # 464
# dictionaries
# get rid of trivial words with nltk.corpus.stopwords.words('english')
# get rid of general vocabulary with nltk.corpus.words.words()
stopwords = [stemmer.stem(word) for word in nltk.corpus.stopwords.words('english')]
stopwords
mr_content = [tok for tok in mr_vocab if tok not in stopwords]
len(mr_content) # 390 or 381
mr_content # content word stems
nltk_vocab = nltk.corpus.words.words()
english_vocab = [stemmer.stem(word.lower()) for word in nltk_vocab]
len(english_vocab)
# import random
random.sample(english_vocab, 20) # some setms from the nltk words corpus
mr_unusual = [word for word in mr_content if word not in english_vocab]
mr_unusual
'glitch' in nltk_vocab # False
'cartoonish' in nltk_vocab # False
'filmmaker' in nltk_vocab # False

# Part-Of-Speech (POS) tagging
# also known as grammatical tagging
# e.g. noun, verb, adjective, adverb, preposition
# once done by hand, as in school, now done algorithmically
# done by analyzing token character features and surrounding context:
nltk.help.upenn_tagset() # https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
tag = nltk.pos_tag
tag(['they','bug','him']) # 'bug' is VBP
tag(['a','bug','crawls']) # 'bug' is NN
tag(['bug']) # NN most likely use without context information
tag(['wug']) # NN
tag(['wugs']) # NNS
tag(['it','wugs','well']) # VBZ
tag(['wugged']) # VBD
tag(['wugging']) # VBG

mr_pos = tag(mr_tokens)
sorted(set(mr_pos))

# let's look at our tokens by pos label
# from collections import defaultdict
tokens_by_pos = defaultdict(set)
for token, pos in mr_pos:
    tokens_by_pos[pos].add(token)

sorted(tokens_by_pos) # the labels that appears in the Minority Report tokens
sorted(tokens_by_pos.items()) # the sets of tokens for each pos label

# noun chunks
# NN	noun, singular        'desk'
# NNS	noun plural           'desks'
# NNP	proper noun, singular 'Harrison'
# NNPS	proper noun, plural   'Americans'
noun_chunks = defaultdict(list)
chunk = []
pos_pattern = []
for token, pos in mr_pos:
    if pos.startswith('N'):
        chunk.append(token)
        pos_pattern.append(pos)
    elif chunk:
        noun_chunks[' '.join(pos_pattern)].append(chunk)
        pos_pattern, chunk = [], []

sorted(noun_chunks)
sorted(noun_chunks.items())

# OPTIONAL: can skip to chunk_parser
# noun phrases--a crude attempt to extract them
noun_phrases = defaultdict(list)
phrase = []
pos_pattern = []
flag = False
for token, pos in mr_pos:
    if pos.startswith('N'):
        phrase.append(token)
        pos_pattern.append(pos)
        flag = True
    elif pos.startswith('J') and not flag:
        phrase.append(token)
        pos_pattern.append(pos)
    elif phrase:
        if pos_pattern[-1].startswith('N'):
            noun_phrases[' '.join(pos_pattern)].append(phrase)
        pos_pattern, phrase, flag = [], [], False

sorted(noun_phrases)
sorted(noun_phrases.items())

# Chunking with Regular Expressions
grammar = r"""
NP: {<JJ>*<NNS?>+}   # chunk determiner/possessive, adjectives and noun
    {<NNPS?>+}                # chunk sequences of proper nouns
"""
chunk_parser = nltk.RegexpParser(grammar)
mr_parsed = chunk_parser.parse(mr_pos)
print(mr_parsed)
mr_chunks = [chunk for chunk in mr_parsed if type(chunk)==nltk.tree.Tree]
mr_chunks
mr_chunks.sort(key=len) # to see longest phrases chunked
mr_chunks

# Stanford Parser
# http://nlp.stanford.edu:8080/parser/index.jsp
# see how it tags and organizes text into trees
# use smaller text samples

# named entity recognition (NER)
mr_ne = nltk.ne_chunk(mr_pos, binary=True)
list(mr_ne) # "Tree" objects contain named entities
sorted(mr_ne)[:50]

# OPTIONAL: one last review of key parsing tools
sentences = nltk.sent_tokenize(mr_text)
tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
chunked_sentences = [nltk.ne_chunk(sentence, binary=True) for sentence in tagged_sentences]
entities = [chunk for sentence in chunked_sentences for chunk in sentence if type(chunk)!=tuple]
list(entities)
sorted(entities)

# Stanford Named Entity Tagger
# http://nlp.stanford.edu:8080/ner/process
# paste text from NYTimes to demo
