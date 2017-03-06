import os
import sys
import json

import re
import statistics as stats
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

reviews = load_reviews(directory)
reviews.sort(key=lambda r:r['release_year']) # sort by release_year
titles = {r['title']:r for r in reviews} # dict of reviews by title

####

mr = titles['Minority Report (2002)'] # the Minority Report review
mr
display(mr)
list(mr.keys()) # see review fields
list(mr.items()) # view key-value pairs

# Inspecting the text with built-in Python functions
mr_text = mr['text']
print(mr_text)
len(mr_text) # character count
mr_text.count('Pre-Cogs')
mr_text.count('Anderton')
mr_text.count('the') # 78 occurrences
print(mr_text.lower()) # normalize letter casing
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
# import re
mr_sents = re.split('[\.\!\?]\s', mr_text) # but we lose that punctuation information
mr_sents
mr_sents = re.split('([^\.\!\?]+[\.\!\?]\s+)', mr_text) # group sentences
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
# import statistics as stats
stats.mean(sent_lengths) # 132 characters
stats.median(sent_lengths) # 131 characters
stats.stdev(sent_lengths) # 68 characters
# this is setup for computing reading level

# Inspect tokens (words and punctuation)
mr_text.split() # simplest possible approach to English tokenization
mr_text.split(' ') # error is that punctuation and whitespaces glom to words
# Splitting with regular expressions
# import re
re.split(' ', mr_text)
re.split('\s', mr_text) # splits on whitespace characters
tokens = re.split('(\W)', mr_text) # groups on non-word characters
tokens = [tok for tok in tokens if tok.strip()] # filters spaces
len(tokens) # 1391
tokens.sort(key=lambda tok:len(tok)) # sort by token length
tokens[:10] # shortest tokens
tokens[-10:] # longest tokens
# from collections import Counter
token_counts = Counter(tokens) # get counts of each token
token_counts.most_common(50) # see most common tokens
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
len(token_set) / len(tokens) # lexical diversity 0.3989935298346513
len(tokens) / len(token_set) # average token occurrences (2.5) misleading
# import statistics as stats
stats.median(token_counts.values()) # 1 (most tokens appear once)
max(token_counts.values()) # 69 (but some tokens occur very frequently)
token_lengths = [len(token) for token in tokens] # token character lengths
min(token_lengths) # 1
max(token_lengths) # 15
stats.mean(token_lengths) # 4.020848310567937
stats.median(token_lengths) # 3
stats.mode(token_lengths) # 1
stats.stdev(token_lengths) # 2.6701649504450606
sorted(token_lengths)[-20:] # character lengths of 20 longest words


# Finale: compute reading level / text complexity
# https://en.wikipedia.org/wiki/Readability
# Most algorithms use word lists and syllable counts
# Ours: "The Code4Lib Readability Index" uses no extra data
words = [tok for tok in re.split('(\W)', mr_text) if tok.isalpha()]
sents = re.split('[\.\!\?]\s', mr_text)
tokenized_sents = []
# let's created a list of tokenized sentences
for sent in sents:
    sent_tokens = [tok for tok in re.split('(\W)', sent) if tok.isalpha()]
    tokenized_sents.append(sent_tokens)

tokenized_sents[0]
tokenized_sents[1]
tokenized_sents[-1]

avg_sent_length = stats.mean([len(sent) for sent in tokenized_sents]) # 24 words
avg_sent_length
avg_word_length = stats.mean([len(word) for word in words]) # 4.6 characters
avg_word_length

def leveler(avg_word_length, avg_sent_length):
    reading_level = -5 + 2*avg_word_length + 0.25*avg_sent_length
    return reading_level

# let's test our leveler before applying it to our Minority Report text
# big words, long sentences
leveler(5, 30) # 12.5
# smaller words, long sentences
leveler(4, 30) # 10.5
# medium words, medium sentences
leveler(4,20) # 8.0
# short words, medium sentences
leveler(3,20) # 6.0
# short words, short sentences
leveler(3,10) # 3.5
# Minority Report: (4.6, 24)
leveler(avg_word_length, avg_sent_length) # 10.147311027415258

# let's turn this into a function that accepts a text input
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

leveler(mr_text) # yes, 10.147311027415258

# let's sort our reviews by reading level
reviews.sort(key=lambda r:leveler(r['text']))
leveler(reviews[0]['text']) # 4.966795091324202
display(reviews[0]) # short sentences with simple language
display(reviews[1]) # repartee dialogue
leveler(reviews[-1]['text']) # 28.858155204460967
display(reviews[-1]) # erroneous commas at the end of each paragraph
reviews[-1]['url'] # visit http://www.rogerebert.com/reviews/switch-1991
leveler(reviews[-2]['text']) # 18.722480395004354
display(reviews[-2]) # long, complex sentences
