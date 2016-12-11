import twitter
import time
import json

class GetTwitterObject:

    def __init__(self):
        self.token = None;
        self.access_token_secret = None;
        self.consumer_key = None;
        self.consumer_secret_key = None;
        self.twitter_object = None;

    def setAccessToken(self,token=None):

        if token is None:
            self.token = "807471303917764608-aUCV0si5k8GFIDiftdSYSMFzb1W1TPW";
        else:
            self.token = token

    def setAccessTokenSecret(self,token_secret=None):

        if token_secret is None:
            self.access_token_secret = "iuXHZvlQ0ivvKy8DA76Aaoayi0wsb9FpNO5wrPCAq9yev";
        else:
            self.access_token_secret = token_secret;

    def setConsumerKey(self,key=None):

        if key is None:
            self.consumer_key = "dtPGQ7KaW9xeHsdZTajEFseoC";
        else:
            self.consumer_key = key;

    def setConsumerSecret(self,cons_sec_key=None):

        if cons_sec_key is None:
            self.consumer_secret_key = "kkUIVRn9KXI218IMoBsHuNP07IsiTc6NeWOR3EGPXlB7J14OKz";
        else:
            self.consumer_secret_key = cons_sec_key;

    def getTweetFromUserTimeLine(self,handle=None,tw_count=None,interval=1):

        userTweetsCollection = list()
        tw_len = 0
        max_ids = [self.twitter_object.statuses.user_timeline(screen_name=handle,count=1,include_retweets=False)[0]['id']]

        for i in range(0,interval):

            tweetsCollection = self.twitter_object.statuses.user_timeline(screen_name=handle,count=tw_count,include_retweets=False,max_id=max_ids[-1])
            for tweet in tweetsCollection:
                max_ids.append(tweet['id'])

            tw_len = tw_len + tw_count;
            userTweetsCollection.append(tweetsCollection)
        return  [tweet for tweets in userTweetsCollection for tweet in tweets]


    def write_to_txt_file(self,tweets):

        with open('tweets.txt','w') as f:
            f.write(json.dumps(tweets))



    def getTwitterObject(self):

        if self.twitter_object is not None : return self.twitter_object


    def createTwitterObject(self):

        self.setAccessToken()
        self.setAccessTokenSecret()
        self.setConsumerKey()
        self.setConsumerSecret()
        self.twitter_object =  twitter.Twitter(auth=twitter.oauth.OAuth(self.token,self.access_token_secret,self.consumer_key,self.consumer_secret_key));



'''
if __name__ == '__main__':

    tw = GetTwitterObject()
    tw.createTwitterObject()
    tweets = tw.getTweetFromUserTimeLine('GoverSmart')
    tw.write_to_txt_file(tweets)
'''









