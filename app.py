
import shutil

import pandas as pd
from flask import Flask, render_template
from pony.orm import *
import db_init
import matplotlib.pyplot as plt
import io
import base64
from data_vars import dict_paises, query_user

app = Flask(__name__)

@app.route('/')
@db_session
def index():
    total_space, used_space, free_space = shutil.disk_usage(__file__)
    total_tweets = count_tweets()
    last_tweet = find_last_tweets()
    log_size()
    #retweet_tweets = find_most_retweet_tweets()
    #reply_tweets = find_most_reply_tweets()
    user_stats = find_user_stats()
    #user_info = get_user_info()
    runtime = find_total_time()

    
    graph = get_total_tweets_hour()
    #print(reply_tweets)
    return render_template('index.html',
        last_tweet=last_tweet,
        user_stats = user_stats,
        #user_info = user_info,
        runtime = runtime,
        dict_paises = dict_paises,
        #reply_tweets=reply_tweets, 
        #retweet_tweets=retweet_tweets,
        total=total_tweets,
        graph = graph, 
        space = total_space/10 **9,
        used = used_space/10**9,
        free = free_space/10**9 )


def find_last_tweets():
    return db_init.Tweet.select().order_by(desc(db_init.Tweet.created_at))[:1]

def find_user_stats():
        #return pd.read_sql(query, db_init.db.get_connection())
        df = pd.read_sql(query_user, db_init.db.get_connection())

        df['local'] = df['id'].map(dict_paises)
        
        df.fillna(0, inplace=True)

        df['Engag_Rep_m'] = df['Replies']/df['Tweets']
        df['Engag_Tweet'] = (df['Retweets'] + df['Replies'])/df['Tweets']
        df['Engag_User'] = (df['Retweets'] + df['Replies'])/df['total_followers']
        
        return df


def find_total_time():
        query = 'SELECT TIMEDIFF( (NOW()), (SELECT created_at FROM tweet ORDER BY created_at LIMIT 1)) as "duracao";'        
        return pd.read_sql(query, db_init.db.get_connection())


def log_size():
        query = 'INSERT INTO size_status (table_name, size_mb, date) \
                 SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "size_mb", NOW() AS date  FROM information_schema.TABLES WHERE table_schema = "user_comp_2" ORDER BY (data_length + index_length) DESC;'        
        db_init.db.execute(query)
#def find_most_reply_tweets():
#    return select((t.in_reply_to_status_id, count()) for t in db_init.Tweet if t.in_reply_to_status_id != None).order_by(desc(2))[:5]

   
#def find_most_retweet_tweets():
#    return select((t.retweet_from_tweet_id, count()) for t in db_init.Tweet if t.retweet_from_tweet_id != None).order_by(desc(2))[:5]

def count_tweets():
    return select((count(t)) for t in db_init.Tweet)[:1]

def get_total_tweets_hour():
        t = db_init.db.execute('SELECT DATE_FORMAT(created_at, "%Y-%m-%d %H") as date , count(*) from tweet group by DATE_FORMAT(created_at, "%Y-%m-%d %H") order by 1;')
        x = []
        y = []
        for p in t.fetchall():
                x.append(p[0])
                y.append(p[1])
        img = io.BytesIO()

        plt.rcParams.update({'font.size': 8})
        plt.figure(figsize=(11,6))

        plt.plot(x, y)
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.25)
        #for a,b in zip(x, y): 
        #        plt.text(a, b, str(b))
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        return 'data:image/png;base64,{}'.format(graph_url)


if __name__ == '__main__':
    app.run(port=443, host='0.0.0.0')
    #app.run()




