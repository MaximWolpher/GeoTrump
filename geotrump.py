from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import Tweet_predict
from googletrans import Translator

access_token = "898452779332665344-HB9wHjpsyyoATpplA5Cc8WBYi3jssiV"
access_token_secret = "m2Z8cbAjOufeXpgYEk30KzhmtGv4P64Jy2M5dGqE63u9E"
consumer_key = "5L1eudRenQ0HnTT030v5MA3SO"
consumer_secret = "euoRR1J2PqWxmAGptJ4FHbQzKkRZKg6VLZQvYZ7iehZg76OIT9"
trans = Translator()
sent = Tweet_predict.Sentiment()

def remove_symb(text):
    try:
        # Wide UCS-4 build
        symb_c = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+',
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        symb_c = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+',
            re.UNICODE)
    return symb_c.sub(r'',text)


class StdOutListener(StreamListener):

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            if json_data.get('place') and json_data['place']:
                if json_data.get('extended_tweet'):
                    in_text = json_data['extended_tweet']['full_text']

                else:
                    in_text = json_data['text']
                try:
                    trans_text = trans.translate(in_text,dest='en').text
                except ValueError as e:
                    clean = remove_symb(in_text)
                    try:
                        trans_text = trans.translate(clean,dest='en').text
                    except ValueError as e:
                        return True
                coords = find_coords(json_data['place']['bounding_box']['coordinates'][0])
                score = sent.sentiment(trans_text)

                # Will now print positive score instead of True/False
                print {'coordinates':coords,'positive':score}

            return True
        except KeyError as e:
            print e
            return True

    def on_error(self, status_code):
        # TODO Need to figure out how to reconnect when failed
        print status_code
        return True

if __name__ == '__main__':

    def find_coords(bbox):
        x1,y1,x2,y2 = bbox[0][0],bbox[0][1],bbox[2][0],bbox[2][1]
        return [(x1+abs(x1-x2)/2.0), (y1+abs(y1-y2)/2.0)]

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['Donald','Trump','DonaldTrump','realDonaldTrump','Donald Trump','#Trump','#Donald'])

