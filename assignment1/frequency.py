import sys
import re
import json
import traceback

word_match = re.compile(r"^[a-zA-Z]+$")

def getTweetWords(tweetLine):
    try:
        tweet = json.loads(tweetLine)
        assert isinstance(tweet, dict)
        if tweet.has_key('created_at') & tweet.has_key('text'):
            # This is a valid text twit
            text = str(tweet['text'])
            words = text.split(' ')
            return map(lambda w: w.strip().lower(), words)
        else:
            return None
    except UnicodeEncodeError:
        return None
    except Exception as err:
        print tweetLine
        tb = traceback.format_exc()
        raise ValueError('Can\'t decode line: %s\n%s' % (str(err), tb))

def getWordsFromTweet(line):
    words = getTweetWords(line)


def main():
    wordsCount = dict()
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        words = getTweetWords(line)
        if words:
            for word in words:
                if word_match.match(word):
                    count = wordsCount.get(word, 0)
                    wordsCount[word] = count + 1

    # Output result
    for (word, count) in wordsCount.iteritems():
        print "%s %s" % (word, float(count)/float(len(wordsCount)))

if __name__ == '__main__':
    main()