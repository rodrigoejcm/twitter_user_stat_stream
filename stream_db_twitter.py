import json
import db_init
import datetime
from pony.orm import *
from dateutil import parser


from birdy.twitter import StreamClient
import pass_tw ## twitter credentials
import unicodedata
from unidecode import unidecode
from data_vars import follow
import re



client = StreamClient(pass_tw.CONSUMER_KEY,
                    pass_tw.CONSUMER_SECRET,
                    pass_tw.ACCESS_TOKEN,
                    pass_tw.ACCESS_TOKEN_SECRET)

resource = client.stream.statuses.filter.post(follow=follow)


@db_session
def save_data(json_data):

    id = None
    if 'id' in json_data:

        
        id = json_data['id']

        if not db_init.Tweet.exists(id=id): 
            total_words = 0
            id_str = json_data['id_str']
            in_reply_to_user_id = json_data['in_reply_to_user_id'] if 'in_reply_to_user_id' in json_data else None 
            created_at = parser.parse(json_data['created_at'])
            
            #USER
            id_user = json_data['user']['id']
            id_str_user = json_data['user']['id_str'] if 'id_str' in json_data['user'] else None 
            screen_name = json_data['user']['screen_name'] if 'screen_name' in json_data['user'] else None  
            name = json_data['user']['name'] if 'name' in json_data['user'] else None  
            truncated = json_data['truncated']
            
            
            #created_at = parser.parse(json_data['user']['created_at']) if 'created_at' in json_data['user'] else None 
            #is_translator = json_data['user']['is_translator'] if 'is_translator' in json_data['user'] else False 
            #name = json_data['user']['name'] if 'name' in json_data['user'] else None
            text = json_data['text']
            if truncated : 
                text_full =  json_data['extended_tweet']['full_text'] 
            else:
                text_full =  text
            #contributors = json_data['contributors'] if 'contributors' in json_data else None 
            #retweet_count = json_data['retweet_count'] if 'retweet_count' in json_data else None 
            in_reply_to_status_id = json_data['in_reply_to_status_id'] if 'in_reply_to_status_id' in json_data else None 
            #filter_level = json_data['filter_level'] if 'filter_level' in json_data else None 
            #quote_count = json_data['quote_count'] if 'quote_count' in json_data else None 
            #geo = json_data['geo'] if 'geo' in json_data else None 
            source = json_data['source'] if 'source' in json_data else None 
            #possibly_sensitive = json_data['possibly_sensitive'] if 'possibly_sensitive' in json_data else False 
            in_reply_to_screen_name = json_data['in_reply_to_screen_name'] if 'in_reply_to_screen_name' in json_data else None 
            #is_quoted_status = json_data['is_quoted_status'] if 'is_quoted_status' in json_data else False 
            #coordinates = json_data['coordinates'] if 'coordinates' in json_data else None 
            #reply_count = json_data['reply_count'] if 'reply_count' in json_data else None 
            #lang =  json_data['lang'] if 'lang' in json_data else None 
            retweet_from_tweet_id = json_data['retweeted_status']['id'] if 'retweeted_status' in json_data else None 

            
            if(id_str_user in follow ):
                
                location = json_data['user']['location'] if 'location' in json_data['user'] else None
                total_followers = json_data['user']['followers_count'] if 'followers_count' in json_data['user'] else None
                total_following = json_data['user']['friends_count'] if 'friends_count' in json_data['user'] else None
                total_posts = json_data['user']['statuses_count'] if 'statuses_count' in json_data['user'] else None
                #id_user
                # name
                #screen_name
                if not db_init.User.exists(id=id_user): 

                     db_init.User(
                         id = id_user,
                         screen_name_usuario = screen_name,
                         name_usuario = name,
                         total_followers = total_followers,
                         total_following = total_following,
                         total_posts = total_posts,
                         location = location
                     )
                else:
                    user_db = db_init.User[id_user]
                    user_db.set(
                        total_followers = total_followers,
                        total_following = total_following,
                        total_posts = total_posts
                    )


                tweet_type = "ORIGINAL"
                if(retweet_from_tweet_id):
                    tweet_type = "ORIGINAL - RETWEET"
                elif(in_reply_to_status_id or in_reply_to_screen_name or in_reply_to_user_id ):
                    tweet_type = "ORIGINAL - REPLY"
            elif(in_reply_to_status_id or in_reply_to_screen_name or in_reply_to_user_id ):
                tweet_type = "REPLY"
                line = ' '.join(re.sub("([@#][A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text_full).split())
                total_words = len(re.findall(r'\w+', line))
                #print(in_reply_to_status_id," reply ID")
            elif(retweet_from_tweet_id):
                tweet_type ="RETWEET"
            else:
                tweet_type ="OTHER"

            if retweet_from_tweet_id:
                retweet_from_user_id = json_data['retweeted_status']['user']['id'] if 'user' in json_data['retweeted_status'] else None 
                retweet_from_screen_name = json_data['retweeted_status']['user']['screen_name'] if 'user' in json_data['retweeted_status'] else None 
            else:
                retweet_from_user_id = None
                retweet_from_screen_name = None
            

            if (tweet_type == "RETWEET"):
                if retweet_from_tweet_id:
                    tw_id = retweet_from_tweet_id

                    if db_init.Tweet.exists(id=tw_id): 
                        save = True
                    else:
                        print("tweet original nao existe")
                        save = False
                else:
                    print("retweet sem id original")
                    save = False

            elif (tweet_type == "REPLY" ):
                if in_reply_to_status_id:
                    tw_id = in_reply_to_status_id
                    
                    if db_init.Tweet.exists(id=tw_id): 
                        save = True
                    else:
                        print("tweet original nao existe")
                        save = False
                else:
                    print("reply sem id original")
                    save = False
            else:
                save = True


            if save:

                tweet = db_init.Tweet(
                    id_usuario = id_user,
                    id_str_usuario = id_str_user,
                    screen_name_usuario =screen_name,
                    name_usuario = name,
                    
                    id = id,
                    id_str = id_str,
                    
                    created_at = created_at,
                    
                    text_full = text_full,
                    text = text,
                    total_words = total_words,
                    
                    source = source,
                    
                    in_reply_to_user_id = in_reply_to_user_id, 
                    in_reply_to_status_id = in_reply_to_status_id,
                    in_reply_to_screen_name = in_reply_to_screen_name,
                    retweet_from_tweet_id = retweet_from_tweet_id,
                    retweet_from_user_id = retweet_from_user_id,
                    retweet_from_screen_name = retweet_from_screen_name,
                    tweet_type = tweet_type 
                    
                )
            


        

for data in resource.stream():
    save_data(data)
    commit()

