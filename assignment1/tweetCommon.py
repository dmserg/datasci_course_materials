import sys
import re
import json
import traceback

'''
Common functions for tweeter assignments
'''

_word_match = re.compile(r"^[a-zA-Z]+$")

def getTextTweet(tweetLine):
    tweet = json.loads(tweetLine)
    assert isinstance(tweet, dict)
    if tweet.has_key('created_at') & tweet.has_key('text'):
        return tweet
    else:
        return None

def getTweetWords(tweet):
    try:
        text = str(tweet['text'])
        words = text.split(' ')
        return map(lambda w: w.strip().lower(), words)

    except UnicodeEncodeError:
        return None
    except Exception as err:
        tb = traceback.format_exc()
        raise ValueError('Can\'t decode tweet: %s\n%s' % (str(err), tb))

def isPlainWord(word):
    return True if _word_match.match(word) else False

def getSentimentScoreDict(afinnFileName):
    afinnfile = open(afinnFileName)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    return scores

def getSentimentScore(words, scoreDict):
    sentimentScore = 0
    for word in words:
        key = word.strip().lower()
        if scoreDict.has_key(key):
            sentimentScore += int(scoreDict[key])

    return sentimentScore