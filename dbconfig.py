from pymongo.errors import ConnectionFailure
from pymongo import MongoClient

if __name__=='__main__':


    from tweetconfiguration import GetTwitterObject

    client = None;
    db = None;
    collection = None;
    try:
        client = MongoClient(port=27017);
        db = client['twitter'];
        collection = db['ecosystem'];
        isConnected = True;
    except ConnectionFailure as e:
        print "Connection Failure #####"

    tw_object = GetTwitterObject()

    tw_object.createTwitterObject()
    tweets = tw_object.getTweetFromUserTimeLine('GoverSmart',10,16)

    print tweets
    for tweet in tweets:
        saveTweet = {
                'id':tweet['id'],
                'text':tweet['text'],
                'retweet_count':tweet['retweet_count'],
                'created_at':tweet['created_at'],
                'status':'pending',
                'coordinates':'NA'
                };
        collection.insert_one(saveTweet).inserted_id
