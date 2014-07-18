import sys
import json
import traceback
import tweetCommon

def getWordsFromTweet(line):
    words = tweetCommon.getTweetWords(line)

def main():
    wordsCount = dict()
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        tweet = tweetCommon.getTextTweet(line)
        if tweet:
            words = tweetCommon.getTweetWords(tweet)
            if words:
                for word in words:
                    if tweetCommon.isPlainWord(word):
                        count = wordsCount.get(word, 0)
                        wordsCount[word] = count + 1

    # Output result
    for (word, count) in wordsCount.iteritems():
        print "%s %s" % (word, float(count)/float(len(wordsCount)))

if __name__ == '__main__':
    main()