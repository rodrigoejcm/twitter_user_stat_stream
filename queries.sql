S

SELECT screen_name_usuario, count(*)
from tweet
where 
tweet_type = "ORIGINAL"
group by screen_name_usuario, name_usuario




select tweet_type, count(tweet_type) from tweet group by tweet_type;



SELECT * 
FROM ( 
SELECT screen_name_usuario , name_usuario, count(*) as "Tweets"
from tweet where  tweet_type = "ORIGINAL" group by screen_name_usuario, name_usuario ) AS a

join
(
select retweet_from_screen_name , count(*) as "Retweets" 
from tweet where tweet_type = "RETWEET" group by retweet_from_screen_name ) AS b

on  a.screen_name_usuario = b.retweet_from_screen_name

join 

(select in_reply_to_screen_name  , count(*) as "Replies" 
from tweet where tweet_type = "REPLY" group by in_reply_to_screen_name ) as c   

on c.in_reply_to_screen_name = a.screen_name_usuario
order by 7,3,5 desc




SELECT TIMEDIFF(
    (SELECT created_at FROM tweet ORDER BY created_at DESC LIMIT 1),
    (SELECT created_at FROM tweet ORDER BY created_at LIMIT 1)) as "duracao";



SELECT name_usuario, total_followers, total_following, total_posts, location from user;




SELECT * FROM 
( SELECT screen_name_usuario , name_usuario, count(*) as "Tweets"from tweet where  tweet_type = "ORIGINAL" group by screen_name_usuario, name_usuario ) AS a 
join 
( select retweet_from_screen_name , count(*) as "Retweets" from tweet where tweet_type = "RETWEET" group by retweet_from_screen_name ) AS b 
on  a.screen_name_usuario = b.retweet_from_screen_name 
join 
(select in_reply_to_screen_name  , count(*) as "Replies" from tweet where tweet_type = "REPLY" group by in_reply_to_screen_name ) as c  on c.in_reply_to_screen_name = a.screen_name_usuario 
join
(SELECT name_usuario, total_followers, total_following, total_posts, location from user) as d
on a.name_usuario = d.name_usuario 
order by 7,3,5 desc;


SELECT a.name_usuario, a.Tweets, e.Tweets_RE as "Tweets(RE)", b.Retweets, c.Replies, d.id, d.total_followers, d.total_following, d.total_posts    FROM 
( SELECT screen_name_usuario , name_usuario, count(*) as "Tweets"from tweet where  tweet_type = "ORIGINAL" group by screen_name_usuario, name_usuario ) AS a 
left join 
( SELECT screen_name_usuario , name_usuario, count(*) as "Tweets_RE"from tweet where  tweet_type = "ORIGINAL - RETWEET" group by screen_name_usuario, name_usuario ) AS e
on  a.screen_name_usuario = e.screen_name_usuario 
left join 
( select retweet_from_screen_name , count(*) as "Retweets" from tweet where tweet_type = "RETWEET" group by retweet_from_screen_name ) AS b 
on  a.screen_name_usuario = b.retweet_from_screen_name 
left join 
(select in_reply_to_screen_name  , count(*) as "Replies" from tweet where tweet_type = "REPLY" group by in_reply_to_screen_name ) as c  on c.in_reply_to_screen_name = a.screen_name_usuario 
left join
(SELECT id, name_usuario, total_followers, total_following, total_posts, location from user) as d
on a.name_usuario = d.name_usuario ;













