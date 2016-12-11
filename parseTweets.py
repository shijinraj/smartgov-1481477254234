from bson import json_util
from pymongo import MongoClient
import json
import spellchecker
import re
import random
import nltk
import pandas as pd


class Tweets:

    def __init__(self,db = None):
        self.db = db

    def fetchPlaces(self):
        places = []
        with open('places.txt','r') as f:
            places = f.readlines()
        places = map(lambda x:x.rstrip(),places)
        return places

    def parseTweets(self):
        dbPlaces = self.fetchPlaces()

        phoneNo = None
        Name    = None
        BloodType = None
        Place = None
        hospital = None
        units = None

        client = MongoClient(port=27017);
        db = client['twitter'];
        collection = db['ecosystem'];

        tweets = collection.find()

        regex_str = [
                 r'<[^>]+>', # HTML tags
                 r'(?:@[\w_]+)', # @-mentions
                 r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
                 r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',#URLs
                 r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
                 r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
                 r'(?:[\w_]+)', # other words
                 r'(?:\S)', # anything else
                 r'(?:AB|A|B|O)[-+]ve'
              ]
        status = ['pending','WIP','completed']
        tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

        dump = MongoClient(port=27017)
        db = dump['parsedTwitter']
        collection = db['ecosystem']

        for tweet in tweets:
            tokens = map(lambda x:x.lower(),self.tokenize(tweet['text'].encode('utf-8'),tokens_re))

            '''
            if 'call' in tokens:
                phoneNumber = [
                        r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}',
                        r'\d{9}'
                            ]
                result = [token for token in tokens if re.search(r'('+'|'.join(phoneNumber)+')',token)]

                if len(result) > 0 :
                     phoneNo =  ' '.join(result) if len(result) > 1 else result[-1]

            if 'hospital' in tokens:
                hospital = tokens[tokens.index('hospital') - 1]

            if  'units' in tokens:
                units = tokens[tokens.index('units') - 1]

            if len(set(tokens).intersection(set(['ve']))) == 1:
                index = tokens.index('ve')
                BloodType = tokens[index-2]+tokens[index-1]+tokens[index]

            if BloodType == None:

                find_blood_gram = [gram for gram in  nltk.ngrams(tweet['text'].encode('utf-8').split(),3)]

                for (x,y,z) in find_blood_gram:
                    if re.search(r'blood',y):
                        BloodType = x+'-ve'
                    if re.search(r'blood',z):
                        BloodType = y+'+ve'

            if len(BloodType.split('-')) > 0:
                BloodType = spellchecker.correction(BloodType.split('-')[0])
            elif len(BloodType.split('+')) > 0:
                BloodType = spellchecker.correction(BloodType.split('+')[0])
            else:
                BloodType = 'a-ve'
            '''

            places = []

            for token in tokens:
                if re.search('^#',token):
                    token = token.split('#')[1]
                    places.append(token)

            if places is None or len(places) == 0:
                places.append('Not Avaliable')
            time = tweet['created_at'].split(' ')
            collection.insert_one({
                'place':places[0],
                'text':tweet['text'],
                'status':status[random.randint(0,2)],
                'created_at':str(random.randint(0,31))+'/'+time[1]+'/'+time[5],
                'retweet_count':tweet['retweet_count']+1,
                'coordinates':'NA',
                'category':'waste management'
                }).inserted_id;
            #print 'Units Required:{0},hospital:{1},Phone:{2},Place:{3}'.format(units,hospital,phoneNo,' '.join(places))

    def tokenize(self,tweet,tokens_re):
        return tokens_re.findall(tweet)



if __name__=='__main__':

    tw = Tweets();
    tw.parseTweets()






