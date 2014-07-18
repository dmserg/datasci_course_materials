import sys
import re
import json
import operator
import math

empty_state = ""

states_coordinates = {
"AK":(61.3850,-152.2683),
"AL":(32.7990,-86.8073),
"AR":(34.9513,-92.3809),
"AS":(14.2417,-170.7197),
"AZ":(33.7712,-111.3877),
"CA":(36.1700,-119.7462),
"CO":(39.0646,-105.3272),
"CT":(41.5834,-72.7622),
"DC":(38.8964,-77.0262),
"DE":(39.3498,-75.5148),
"FL":(27.8333,-81.7170),
"GA":(32.9866,-83.6487),
"HI":(21.1098,-157.5311),
"IA":(42.0046,-93.2140),
"ID":(44.2394,-114.5103),
"IL":(40.3363,-89.0022),
"IN":(39.8647,-86.2604),
"KS":(38.5111,-96.8005),
"KY":(37.6690,-84.6514),
"LA":(31.1801,-91.8749),
"MA":(42.2373,-71.5314),
"MD":(39.0724,-76.7902),
"ME":(44.6074,-69.3977),
"MI":(43.3504,-84.5603),
"MN":(45.7326,-93.9196),
"MO":(38.4623,-92.3020),
"MP":(14.8058,145.5505),
"MS":(32.7673,-89.6812),
"MT":(46.9048,-110.3261),
"NC":(35.6411,-79.8431),
"ND":(47.5362,-99.7930),
"NE":(41.1289,-98.2883),
"NH":(43.4108,-71.5653),
"NJ":(40.3140,-74.5089),
"NM":(34.8375,-106.2371),
"NV":(38.4199,-117.1219),
"NY":(42.1497,-74.9384),
"OH":(40.3736,-82.7755),
"OK":(35.5376,-96.9247),
"OR":(44.5672,-122.1269),
"PA":(40.5773,-77.2640),
"PR":(18.2766,-66.3350),
"RI":(41.6772,-71.5101),
"SC":(33.8191,-80.9066),
"SD":(44.2853,-99.4632),
"TN":(35.7449,-86.7489),
"TX":(31.1060,-97.6475),
"UT":(40.1135,-111.8535),
"VA":(37.7680,-78.2057),
"VI":(18.0001,-64.8199),
"VT":(44.0407,-72.7093),
"WA":(47.3917,-121.5708),
"WI":(44.2563,-89.6385),
"WV":(38.4680,-80.9696),
"WY":(42.7475,-107.2085)}

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

def calculateDistance(sLatitude, sLongitude, eLatitude, eLongitude):
    sLatitudeRadians = sLatitude * (math.pi / 180.0)
    #sLongitudeRadians = sLongitude * (math.pi / 180.0)
    eLatitudeRadians = eLatitude * (math.pi / 180.0)
    #eLongitudeRadians = eLongitude * (math.pi / 180.0)

    #dLongitude = eLongitudeRadians - sLongitudeRadians
    #dLatitude = eLatitudeRadians - sLatitudeRadians
    theta = sLongitude-eLongitude
    rTheta = math.pi * theta / 180.0
    dist = math.sin(sLatitudeRadians) * math.sin(eLatitudeRadians) + math.cos(sLatitudeRadians) * math.cos(eLatitudeRadians) * math.cos(rTheta)
    dist = math.acos(dist)
    dist = dist * 180/math.pi
    dist = dist * 60 * 1.1515 * 1.609344
    return math.fabs(dist)

def findNearestState(latitude, longitude):
    minDistance = sys.maxint
    minState = ""
    for state, (state_lat, state_long) in states_coordinates.iteritems():
        distance = calculateDistance(latitude, longitude, state_lat, state_long)
        if distance < minDistance:
            minState = state
            minDistance = distance
    return minState

def getState(tweet):
    if tweet["coordinates"]: #or tweet["place"]:
        coordinates = tweet["coordinates"]["coordinates"]
        return findNearestState(coordinates[1], coordinates[0])
    return empty_state

def main():
    tweet_file = open(sys.argv[2])
    sentimentsDict = getSentimentScoreDict(sys.argv[1])
    statesScore = dict()
    # Read tweets line by line...
    for line in tweet_file:
        tweet = getTextTweet(line)
        if tweet:
            words = getTweetWords(tweet)
            if words:
                score = getSentimentScore(words, sentimentsDict)
                state = getState(tweet)
                stateScore = statesScore.get(state, 0) + score
                statesScore[state] = stateScore

    # Sort by score
    sortedByScore = sorted(statesScore.iteritems(), key=operator.itemgetter(0), reverse=True)
    for state, score in sortedByScore:
        if state != empty_state:
            print state
            return

if __name__ == '__main__':
    main()