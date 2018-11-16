from decimal import Decimal
from datetime import date
from datetime import datetime


import json

from pony.orm.core import *

db = Database()



class User(db.Entity):
    id = PrimaryKey(int,size=64)
    screen_name_usuario = Optional(str,nullable=True)
    name_usuario = Optional(str,nullable=True)
    total_followers = Optional(int)
    total_posts = Optional(int)
    total_following = Optional(int)
    location = Optional(str,nullable=True )
    


class Tweet(db.Entity):
    id = PrimaryKey(int, size=64)
    id_str = Required(str)
    id_usuario = Required(int, size=64)
    id_str_usuario = Required(str)
    screen_name_usuario = Optional(str,nullable=True)
    name_usuario = Optional(str,nullable=True)
    
    in_reply_to_user_id = Optional(int, size=64)
    in_reply_to_status_id = Optional(int, size=64)
    in_reply_to_screen_name = Optional(str, nullable=True)
    retweet_from_tweet_id = Optional(int, size=64)
    retweet_from_screen_name = Optional(str, nullable=True)
    retweet_from_user_id = Optional(int, size=64)

    created_at = Optional(datetime)

    text = Required(LongUnicode)
    text_full = Optional(LongUnicode, nullable=True)

    source = Optional(str, nullable=True)
    tweet_type = Optional(str, nullable=True)
    

    

sql_debug(True)  # Output all SQL queries to stdout



params = dict(
    #sqlite=dict(provider='sqlite', filename='university1.sqlite', create_db=True),
    mysql=dict(provider='mysql', host="localhost", user="twitter_user", passwd="twitter_pass", db="user_comp_3")
    #postgres=dict(provider='postgres', user='pony', password='twitter_user', host='localhost', database='twitter'),
    #oracle=dict(provider='oracle', user='c##pony', password='pony', dsn='localhost/orcl')
)

db.bind(**params['mysql'], charset='utf8mb4', use_unicode=True)


if __name__ == '__main__':
    print("GERANDO TABELAS....")
    db.generate_mapping(create_tables=True)
    with db_session:
        db.execute("SET NAMES utf8mb4;")
    #    db.execute("ALTER DATABASE twitter CHARACTER SET = utf8mb4;")
  
    
else:
    db.generate_mapping(create_tables=False)
    with db_session:
        db.execute("SET NAMES utf8mb4;")
