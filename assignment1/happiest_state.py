import sys
import tweetCommon
import operator

def main():
    tweet_file = open(sys.argv[2])
    sentimentsDict = tweetCommon.getSentimentScoreDict(sys.argv[1])
    tweetScores = dict()
    # Read tweets line by line...
    for line in tweet_file:
        tweet = tweetCommon.getTextTweet(line)
        if tweet:
            words = tweetCommon.getTweetWords(tweet)
            if words:
                score = tweetCommon.getSentimentScore(words, sentimentsDict)
                tweetScores[score] = tweet

    # Sort by score
    sortedByScore = sorted(tweetScores.iteritems(), key=operator.itemgetter(0))

if __name__ == '__main__':
    main()