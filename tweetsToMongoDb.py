from dbconfig import DbConfig
from tweetconfiguration import GetTwitterObject

if __name__=='__main__':

    db = DbConfig();

    tw_object = GetTwitterObject()

    tw_object.createTwitterObject()
    tweets = tw_object.getTweetFromUserTimeLine('GoverSmart',10,16)

    db.deleteAllOrOneDocument()

    for tweet in tweets:
        saveTweet = {
                'id':tweet['id'],
                'user':tweet['user'],
                'text':tweet['text'],
                'lang':tweet['lang'],
                'place':tweet['place'],
                'retweet_count':tweet['retweet_count'],
                'created_at':tweet['created_at'],
                'entities':tweet['entities']
                };
        db.insertDocument(saveTweet)
