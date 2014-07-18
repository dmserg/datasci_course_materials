import sys
import re
import json
import traceback
import tweetCommon

def getSentimentScore(tweetLine, scoreDict):
    try:
        assert isinstance(scoreDict, dict)
        tweet = json.loads(tweetLine)
        assert isinstance(tweet, dict)
        if tweet.has_key('created_at') & tweet.has_key('text'):
            sentimentScore = 0
            # This is a valid text twit
            text = str(tweet['text'])
            words = text.split(' ')
            newWords = []
            for word in words:
                key = word.strip().lower()
                if scoreDict.has_key(key):
                    sentimentScore += int(scoreDict[key])
                else:
                    if tweetCommon.isPlainWord(key):
                        newWords.append(key)
            return sentimentScore, newWords
        else:
            return "N/A", None
    except UnicodeEncodeError:
        return 0, None
    except Exception as err:
        print tweetLine
        tb = traceback.format_exc()
        raise ValueError('Can\'t decode line: %s\n%s' % (str(err), tb))

def calculateNewWordSentiment(tweetSentiment, wordSentiment, wordsNumber):
    newSentiment = tweetSentiment + wordSentiment/wordsNumber
    return newSentiment

def main():
    sentimentsDict = tweetCommon.getSentimentScoreDict(sys.argv[1])
    newSentimentsDict = dict()
    tweet_file = open(sys.argv[2])
    for line in tweet_file:
        (score, newWords) = getSentimentScore(line, sentimentsDict)
        if score != "N/A" and newWords and len(newWords) > 0:
            for newWord in newWords:
                newWordSentiment = newSentimentsDict.get(newWord, 0)
                newSentimentsDict[newWord] = calculateNewWordSentiment(score, newWordSentiment, len(newWords))

    # Output new words with related score
    for word, score in newSentimentsDict.iteritems():
        print "%s %s" % (word, str(int(min(5, max(-5, score)))))

if __name__ == '__main__':
    main()
