import nltk

# reviews.sort(key=lambda x:x['date_published'])
# reviews.sort(key=lambda x:len(x['text']))

#


# Getting the text of a single review
# mr = list(filter(lambda r:'Minority Report' in r['title'], reviews))[0]
mr = None # Minority Report
for r in reviews:
    if 'Minority Report' in r['title']:
        print(r)
        mr = r

# Inspecting the review
mr
list(mr.keys()) # see review fields
list(mr.items()) # view key-value pairs

# Inspecting the text with built-in Python functions
mr_text = mr['text']
print(mr_text)
len(mr_text)
mr_text.count('Pre-Cogs')
mr_text.count('Anderton')
mr_text.count('the') # 78 occurrences
print(mr_text.lower())
mr_text.lower().count('the') # but 88 occurrences in lowercased text
print(mr_text.upper())
mr_text.upper().count('THE') # and 88 occurrences in uppercased text

# Inspect paragraphs
print(mr_text)
mr_paras = mr_text.split('\n\n')
len(mr_paras)
mr_paras[0]
mr_paras[-1]
mr_paras.sort(key=lambda p:len(p)) # sort by character length of paragraph
mr_paras[0]
mr_paras[-1]
len(mr_paras[0])
len(mr_paras[-1])

# Inspect sentences
mr_sents = mr_text.split('. ')
mr_sents[:5] # uh oh--newlines are not properly split
mr_sents = mr_text.split('.')
mr_sents[:5] # looks good
mr_sents[-5:] # looks good
mr_sents[18:22] # ellipsis results in error!
mr_text[3000:3200] # the original text
import re
mr_sents = re.split('[\.\!\?]\s', mr_text) # but we lose that punctuation information
mr_sents
mr_sents = re.split('([^\.\!\?]+[\.\!\?]\s+)', mr_text)
mr_sents
mr_sents[44:46] # but what about quotation marks and parentheticals?
mr_sents = [sent for sent in mr_sents if sent] # clear empty strings
len(mr_sents)
mr_sents.sort(key=lambda s:len(s)) # sort by sentence character length
mr_sents[:10] # shortest sentences
mr_sents[-3:] # longest sentences
len(mr_sents[0]) # character length of shortest sentence
len(mr_sents[-1]) # character length of longest sentence
sent_lengths = [len(sent) for sent in mr_sents]
import statistics as stats
stats.mean(sent_lengths) # 132 characters
stats.median(sent_lengths) # 131 characters
stats.stdev(sent_lengths) # 68 characters
# this is setup for computing reading level

# Inspect tokens (words and punctuation)
mr_text.split()
mr_text.split(' ') # error is that punctuation and whitespaces glom to words
# Splitting with regular expressions
# import re
re.split(' ', mr_text)
re.split('\s', mr_text) # splits on whitespace characters
tokens = re.split('(\W)', mr_text) # groups on non-word characters
#tokens = list(filter(lambda token:token not in ['', ' '], tokens)) # filters spaces
tokens = [tok for tok in tokens if tok not in ['', ' ']] # filters spaces
len(tokens)
tokens.sort(key=lambda tok:len(tok)) # sort by token length
tokens[:10] # shortest tokens
tokens[10:] # longest tokens
from collections import Counter
token_counts = Counter(tokens) # get counts of each token
token_counts.most_common() # see most common tokens
token_counts['film']
token_counts['movie']
token_counts['scene']
token_counts['sequence']
token_counts['character']
sorted(tokens) # alphabetical list of all tokens
token_set = set(tokens) # unique tokens
sorted(token_set) # alphabetical list of unique tokens
len(tokens) # count of all tokens
len(token_set) # count of unique tokens
len(token_set) / len(tokens) # lexical diversity
len(tokens) / len(token_set) # average token occurrences
token_lengths = [len(token) for token in tokens]
min(token_lengths)
max(token_lengths)
# import statistics as stats
stats.mean(token_lengths)
stats.median(token_lengths)
stats.mode(token_lengths)
stats.stdev(token_lengths)
sorted(token_lengths)[-20:]


# Finale: compute reading level / text complexity
# https://en.wikipedia.org/wiki/Readability
# Most use word lists and syllable counts
# Ours: "The Code4Lib Readability Index"

words = [tok for tok in re.split('(\W)', mr_text) if tok.isalpha()]
sents = re.split('[\.\!\?]\s', mr_text)
tokenized_sents = []
for sent in sents:
    sent_tokens = [tok for tok in re.split('(\W)', sent) if tok.isalpha()]
    tokenized_sents.append(sent_tokens)

tokenized_sents[0]
tokenized_sents[1]

avg_sent_length = stats.mean([len(sent) for sent in tokenized_sents]) # 23 words
avg_word_length = stats.mean([len(word) for word in words]) # 4.6 characters

def leveler(avg_word_length, avg_sent_length):
    reading_level = -5 + 2*avg_word_length + 0.25*avg_sent_length
    return reading_level

leveler(5, 30) # 12.5
leveler(4, 30) # 10.5
leveler(4,20) # 8.0
leveler(3,20) # 6.0
leveler(3,10) # 3.5
leveler(avg_word_length, avg_sent_length) # 9.95

def leveler(text):
    words = [tok for tok in re.split('(\W)', text) if tok.isalpha()]
    sents = re.split('[\.\!\?]\s', text)
    tokenized_sents = []
    for sent in sents:
        sent_tokens = [tok for tok in re.split('(\W)', sent) if tok.isalpha()]
        tokenized_sents.append(sent_tokens)
    avg_sent_length = stats.mean([len(sent) for sent in tokenized_sents]) # 23 words
    avg_word_length = stats.mean([len(word) for word in words]) # 4.6 characters
    reading_level = -5 + 2*avg_word_length + 0.25*avg_sent_length
    return reading_level

leveler(mr_text)
reviews.sort(key=lambda r:leveler(r['text']))
print(reviews[0]['text']) # short sentences with simple language
reviews[0]
print(reviews[1]['text']) # repartee dialogue
reviews[1]
print(reviews[-1]['text']) # erroneous commas at the end of each paragraph
reviews[-1] # visit http://www.rogerebert.com/reviews/switch-1991
print(reviews[-2]['text']) # long, complex sentences
reviews[-2]





# .lower()
# .isalpha()
# .endswith('ing')
# .beginswith('dis')


# Introducing NLTK
import nltk
from collections import Counter
# from nltk imoprt sent_tokenize
# from nltk import word_tokenize

# use reviews[0] and reviews[-1] ?

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


# Corpus level analysis with set of reviews

# import os
# nltk.corpus.reader.plaintext import PlaintextCorpusReader
# corpusdir = 'review_text/'
# newcropus = PlaintextCorpusReader(corpusdir, '.*')


len(reviews) # 7734 star-rated reviews
reviews.sort(key=lambda x:len(x['text']))
reviews[0] # shortest
reviews[-1] # longest
# reviews.sort(key=lambda x:x['running_time'])
# date_published
# running_time
# star_rating
# mpaa_rating
# genre

# show plots and other statistics
# concatenate by date_published
# analyze concatenated corpus using NLTK techniques seen above (and more)
# possibly run some processes against each individual review text
#   e.g. compare review_wrapper._collocations across texts



# collocations
# or
# noun chunks
# or
# tf-idf
# or
# tf-idf for noun chunks
#for r in reviews:
#    tokens = nltk.word_tokenize(r['text'])
#    text_wrapper = nltk.Text(tokens)
#    text_wrapper.collocations(50)
#    collos = text_wrapper._collocations
#    r['collocations'] = collos


grammar = r"""
NP: {<JJ>*<NNS?>+}
    {<NNPS?>+}
"""
chunk_parser = nltk.RegexpParser(grammar)

def parse_review(r, parser):
    try:
        print(r['title'])
        r['sentences'] = nltk.sent_tokenize(r['text'])
        r['tokens'] = nltk.word_tokenize(r['text'])
        r['pos_tags'] = nltk.pos_tag(r['tokens'])
        text_wrapper = nltk.Text(r['tokens'])
        text_wrapper.collocations(50) # prints collocations
        r['collocations'] = text_wrapper._collocations
        r['noun_chunks'] = [
            str(c) for c in parser.parse(r['pos_tags'])
            if type(c)==nltk.tree.Tree
        ]
        print(len(r['noun_chunks']))
        print('')
    except Exception as error:
        print(error)
        print('')

for r in reviews:
    parse_review(r, chunk_parser)


#could also store r['tokens'] = tokens
#or
#r['text_wrapper'] = text_wrapper

for r in reviews:
    all_collos.extend(r['collocations'])


Counter(all_collos).most_common()

for r in reviews:
     ...:     if ('bad', 'guys') in r['collocations']:
     ...:         print(r['title'])

for r in reviews:
     ...:     if ('New', 'Wave') in r['collocations']:
     ...:         print(r['title'])
     ...:
     ...:
Les Biches (1969)
The Firemen's Ball (1969)
Around a Small Mountain (2010)
Elevator to the Gallows (2005)
La Collectionneuse (1967)
Cléo from 5 to 7 (1962)
A Sunday in the Country (1984)
Breathless (1960)
Bob le Flambeur (1955)
The 400 Blows (1959)
The Flower of Evil (2003)
Au revoir les enfants (1987)
Atlantic City (1980)
Inspector Bellamy (2011)
The Beaches of Agnes (2008)
A Tale of Winter (1992)
The Dreamers (2004)
Mon oncle d'Amerique (1980)
The American Friend (1977)


# can generate tags by looking at common vocab not in stopwords list!
from nltk.corpus import stopwords
stopwords.words('english')

for tok in mr_tokens:
     ...:     if tok.lower() not in stopwords.words('english') and tok.isalpha():
     ...:         print(tok)



reviews.sort(key=lambda x:x['date_published'])
review_texts = [r['text'] for r in reviews]
all_text = '\n\n\n\n'.join(review_texts)

# demonstrate stemming on "fall"?
all_text.count('fell in love') # the limitation of stemming! fell !> fall
all_text.count('falling in love')
all_text.count('fall in love')
all_text.count('falls in love')
# all_text.count('fall out of love')

all_tokens = nltk.word_tokenize(all_text)


# formula may differ--could log some of these values
# also n+1 for some of these values?

all_tokens_count = len(all_tokens)
all_counts = Counter(all_tokens)
all_freqs = {tok:all_counts[tok]/all_tokens_count for tok in all_tokens}

mr_token_count = len(mr_tokens)
mr_counts = Counter(mr_tokens)
mr_freqs = {tok:mr_counts[tok]/mr_token_count for tok in mr_tokens}

tf_idf_scores = [(tok, mr_freqs[tok]/all_freqs[tok]) for tok in set(mr_tokens)]
tf_idf_scores.sort(key=lambda s:s[1], reverse=True)
tf_idf_scores

romances = []
trigrams = nltk.ngrams(all_tokens, n=3)
for tri in trigrams:
    if ' '.join([stemmer.stem(tri[0]),tri[1],tri[2]]) == 'fall in love':
        print(tri)
        romances.append(tri)

len(romances)



all_wrapper = nltk.Text(all_tokens)



# Visualizing our data
import matplotlib.pyplot as pyplot

# date_published (histogram)
pub_dates = [int(r['date_published'].split('-')[0]) for r in reviews] # year
pub_date_range = max(pub_dates)+1 - min(pub_dates)
pyplot.hist(pub_dates, bins=pub_date_range)
pyplot.show() # early outlier in 1960
reviews[0] # mistake--Le Petit Soldat (1960) was clearly not reviewed in 1960

# release_year (histogram)
release_dates = [r['release_year'] for r in reviews]
release_date_range = max(release_dates)+1 - min(release_dates)
pyplot.hist(release_dates, bins=pub_date_range)
pyplot.show()

# character count of text (histogram)
char_counts = [len(r['text']) for r in reviews]
char_counts_range = max(char_counts)+1 - min(char_counts)
pyplot.hist(char_counts, bins=int(char_counts_range/10))
pyplot.show()

# word count of text (histogram())
review_tokens = [nltk.word_tokenize(r['text']) for r in reviews]
review_words = [[tok for tok in tokens if tok.isalpha()] for tokens in review_tokens]
word_counts = [len(words) for words in review_words]
word_count_range = max(word_counts)+1 - min(word_counts)
pyplot.hist(word_counts, bins=int(word_count_range/10))
pyplot.show() # bimodal distribution--indicates varying formats
# did Ebert work under 1000-word and 1500-word limits?

# genre (pie chart)
genre_instances = [inst for r in reviews if r['genres'] for inst in r['genres']]
#genre_instances = []
#for r in reviews:
#    tagged_genres = r['genres']
#    if tagged_genres:
#        genre_instances.extend(tagged_genres)
from collections import Counter
genre_counts = Counter(genre_instances)
genre_counts
#genres, counts = zip(*sorted(genre_counts.items()))
genres, counts = zip(*sorted([gc for gc in genre_counts.items() if gc[1]>50], key=lambda gc:gc[1]))
pyplot.pie(counts, labels=genres)
pyplot.show()

# running_time (histogram)
running_times = [r['running_time']/60 for r in reviews if r['running_time']]
running_times_range = max(running_times)+1 - min(running_times)
pyplot.hist(running_times, bins=int(running_times_range*20))
pyplot.show() # mass is between 1 and 2.5 hours with long tail to the right

# mpaa_rating (pie chart)
# from collections import Counter
mpaa_ratings = [r['mpaa_rating'] for r in reviews if r['mpaa_rating']]
rating_counts = Counter(mpaa_ratings)
rating_counts
ratings, counts = zip(*sorted([r for r in rating_counts.items() if r[1]>10], key=lambda r:r[1]))
pyplot.pie(counts, labels=ratings)
pyplot.show() # vast minority R

# star_rating (hist)
star_ratings = [r['star_rating'] for r in reviews]
Counter(star_ratings)
#star_range = max(star_ratings)+1 - min(star_ratings)
pyplot.hist(star_ratings, bins=8)
pyplot.show() # displays funny--how to fix?
# note the dip in 2.5 star ratings--a sign of irrationality?


# means and medians:
# stars on mpaa_rating
# stars on genre

# regression:
# http://stackoverflow.com/questions/3949226/calculating-pearson-correlation-and-significance-in-python
# stars on release year post 1967
# stars on review year
# stars on review length
# stars on running_time



# need numpy, matplotlib
# actors
# Freem, Poitier, Gooding, Glover, Snipes
all_wrapper.dispersion_plot(
    ['Eastwood','Brando','Niro','Schwarzenegger','Hanks','Depp',
    'Pitt','Spacey','DiCaprio','Clooney','Osment','Gosling'])

# consider comparison of female actors / actresses

all_wrapper.concordance('laugh', lines=50)
all_wrapper.concordance('cry', lines=50)
all_wrapper.concordance('fight', lines=50)



all_wrapper.similar('scene') # noun
all_wrapper.similar('actor') # noun
all_wrapper.similar('woman') # noun
all_wrapper.similar('pleasant') # adjective
all_wrapper.similar('hideous') # adjective
all_wrapper.similar('entertaining') # adjective
all_wrapper.similar('foreign') # adjective
all_wrapper.similar('intimately') # adverb
all_wrapper.similar('slay') # verb
all_wrapper.similar('pray') # verb

all_wrapper.common_contexts(['good','bad'])
all_wrapper.common_contexts(['good','evil'])
all_wrapper.common_contexts(['man','woman'])
all_wrapper.common_contexts(['boy','girl'])
all_wrapper.common_contexts(['little','small'])
all_wrapper.common_contexts(['big','huge'])
all_wrapper.common_contexts(['short','long'])
all_wrapper.common_contexts(['true','false'])
all_wrapper.common_contexts(['very','extremely'])
all_wrapper.common_contexts(['emotion','feeling'])

# all_fdist = nltk.FreqDist(all_wrapper)
# all_fdist.most_common(50)

# OPTIONAL: DOCUMENT CLASSIFICATION
# http://www.nltk.org/book/ch06.html#document-classification
# train on mpaa ratng and star rating

# spaCy
