import sys
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
            for word in words:
                key = word.strip().lower()
                if scoreDict.has_key(key):
                    sentimentScore += int(scoreDict[key])

            return sentimentScore
        else:
            return None
    except UnicodeEncodeError:
        return 0
    except Exception as err:
        print tweetLine
        tb = traceback.format_exc()
        raise ValueError('Can\'t decode line: %s\n%s' % (str(err), tb))

def main():
    tweet_file = open(sys.argv[2])
    sentimentsDict = tweetCommon.getSentimentScoreDict(sys.argv[1])
    # Read tweets line by line...
    for line in tweet_file:
        score = getSentimentScore(line, sentimentsDict)
        if score:
            print str(score)

if __name__ == '__main__':
    main()
