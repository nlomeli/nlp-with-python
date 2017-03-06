import os
import sys
import json
import nltk
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

mr = titles['Minority Report (2002)'] # the Minority Report review
mr

# Analyze sentences
# Tokenize into sentences
mr_sents = nltk.sent_tokenize(mr_text)
# Sort and display sentences by length
mr_sents.sort(key=lambda x:len(x)) # shortest to longest
mr_sents[:10]
mr_sents[-5:]
# Note we can no longer recover the original order

nltk.word_tokenize(mr_sents[0])
mr_tokens = nltk.word_tokenize(mr['text']) # note that we do not get sentences automatically

mr_sent_tokens = []
for sent in nltk.sent_tokenize(mr_text):
    sent_tokens = nltk.word_tokenize(sent)
    mr_sent_tokens.append(sent_tokens)

mr_sent_tokens[0]
mr_sent_tokens[-1]


nltk.Text?
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

mr_vocab = mr_wrapper.vocab()
mr_vocab # unique tokens with their counts
mr_vocab.most_common(50)

mr_fdist = nltk.FreqDist(mr_wrapper)
mr_fdist.most_common(50)
mr_fdist.plot() # power law

mr_bigrams = list(nltk.ngrams(mr_tokens, 2))
Counter(mr_bigrams).most_common(30) # most common adjacent token pairs
Counter(list(nltk.ngrams(mr_tokens, 3))).most_common(20) # trigrams less interesting here
Counter(list(nltk.ngrams(mr_tokens, 4))).most_common(20) # nor are quadgrams
# Google Books Ngram Viewer: https://books.google.com/ngrams
# try: "true love",

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

from nltk.stem.porter import *
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
stemmed = set([(tok, stemmer.stem(tok)) for tok in mr_tokens if stemmer.stem(tok) != tok]) # actually around 495 unique word stems
stemmed # 'worked', 'working', and 'works' become 'work'

# lemmatization with a vocabulary: WordNet
lemmer = nltk.WordNetLemmatizer()
lemmatized = set([(tok, lemmer.lemmatize(tok)) for tok in mr_tokens if lemmer.lemmatize(tok) != tok])
lemmatized # tries -> try requires a dictionary

# dictionaries
# get rid of trivial words with nltk.corpus.stopwords.words('english')
# get rid of general vocabulary with nltk.corpus.words.words()
mr_vocab = set([stemmer.stem(tok.lower()) for tok in mr_tokens if tok.isalpha()])
len(mr_vocab) # 464
stopwords = [stemmer.stem(word) for word in nltk.corpus.stopwords.words('english')]
stopwords
mr_content = [tok for tok in mr_vocab if tok not in stopwords]
len(mr_content) # 390
mr_content # content words
nltk_vocab = nltk.corpus.words.words()
english_vocab = [stemmer.stem(word.lower()) for word in nltk_vocab]
len(english_vocab)
import random
random.sample(english_vocab, 20)
mr_unusual = [word for word in mr_content if word not in english_vocab]
mr_unusual
'glitch' in nltk_vocab
'cartoonish' in nltk_vocab
'filmmaker' in nltk_vocab

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

from collections import defaultdict
tokens_by_pos = defaultdict(set)
for token, pos in mr_pos:
    tokens_by_pos[pos].add(token)

sorted(tokens_by_pos)
sorted(tokens_by_pos.items())

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
#grammar = r"""
#  NP: {<DT|PP\$>?<JJ>*<NN>+}   # chunk determiner/possessive, adjectives and noun
#      {<NNP>+}                # chunk sequences of proper nouns
#"""
grammar = r"""
NP: {<JJ>*<NNS?>+}   # chunk determiner/possessive, adjectives and noun
    {<NNPS?>+}                # chunk sequences of proper nouns
"""
chunk_parser = nltk.RegexpParser(grammar)
mr_parsed = chunk_parser.parse(mr_pos)
print(mr_parsed)
mr_chunks = [chunk for chunk in mr_parsed if type(chunk)==nltk.tree.Tree]
mr_chunks

# next do NER
# then do some different processing across corpus
# then move on to spaCy analysis


# do NER
#sentences = nltk.sent_tokenize(mr_text)
#tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
#tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
#chunked_sentences = [nltk.ne_chunk(sentence, binary=True) for sentence in tagged_sentences]
#nes = [chunk for sentence in chunked_sentences for chunk in sentence if type(chunk)!=tuple]
#sorted(nes)

mr_ne = nltk.ne_chunk(mr_pos, binary=True)
sorted(mr_ne)[:50]

# nouns are things
# nouns tend to be content
# we'll get all the noun phrases
# these are "noun chunks"

# we'll just look for 'N...' but there will be false positives and adjective-noun misses
# mistakes: ['awkward', 'joins'], ['plot', 'centers'], ['strategy', 'prepares']

# Stanford Parser
# http://nlp.stanford.edu:8080/parser/index.jsp
# other Stanford online demos... (NER, sentiment, etc.)
