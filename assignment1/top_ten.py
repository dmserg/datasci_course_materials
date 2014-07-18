import sys
import json
import operator

def getTextTweet(tweetLine):
    tweet = json.loads(tweetLine)
    assert isinstance(tweet, dict)
    if tweet.has_key('created_at') & tweet.has_key('text'):
        return tweet
    else:
        return None

def getTweetHashTags(tweet):
    if tweet.has_key("entities"):
        entities = tweet["entities"]
        return map(lambda h:h["text"],  entities["hashtags"])
    else:
        return none


def main():
    tweet_file = open(sys.argv[1])
    hashTagsFrequency = dict()
    hashTagsCount = 0.0
    # Read tweets line by line...
    for line in tweet_file:
        tweet = getTextTweet(line)
        if tweet:
            hashTags = getTweetHashTags(tweet)
            if hashTags:
                hashTagsCount += len(hashTags)
                for hashTag in hashTags:
                    counter = hashTagsFrequency.get(hashTag, 0) + 1
                    hashTagsFrequency[hashTag] = counter

    # Sort by frequency
    sortedByFrequency = sorted(hashTagsFrequency.iteritems(), key=operator.itemgetter(1), reverse=True)

    i = 0
    for hashTag, freq in sortedByFrequency:
        encoded_string = hashTag.encode('utf-8')
        print "%s %s" % (encoded_string, str(freq))
        i += 1
        if i == 10:
            break

if __name__ == '__main__':
    main()