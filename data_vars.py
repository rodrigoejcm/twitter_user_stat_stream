dict_paises = {790680:'Brasil',
2174537102:'Brasil',
54341363:'Brasil',
65473559:'Brasil',
17715048:'Brasil',
14594698:'Brasil',
8802752:'Brasil',
14594813:'Brasil',
9317502:'Brasil',
16632084:'Brasil',
29913589:'Brasil',
21207962:'Brasil',
142393421:'Brasil',
23941036:'Brasil',
14311308:'Brasil',
8110402:'Brasil',
124139163:'Portugal',
2561091:'Portugal',
8665852:'Portugal',
15391813:'Portugal',
15391813:'Portugal',
1690412382:'Portugal',
15392221:'Portugal',
17163446:'Portugal',
14842285:'Portugal',
21783395:'Portugal',
16451028:'Portugal',
25535042:'Portugal',
612473:'Reino Unido ',
87818409:'Reino Unido ',
16973333:'Reino Unido ',
111556423:'Reino Unido ',
271413771:'Reino Unido ',
16343974:'Reino Unido ',
7587032:'Reino Unido ',
16887175:'Reino Unido ',
6107422:'Reino Unido ',
138749160:'Reino Unido ',
17895820:'Reino Unido ',
34655603:'Reino Unido ',
21866939:'Reino Unido ',
759251:'EUA',
428333:'EUA',
807095:'EUA',
14293310:'EUA',
2467791:'EUA',
7309052:'EUA',
1020058453:'EUA/UK',
1367531:'EUA',
14511951:'EUA',
14173315:'EUA',
28785486:'EUA',
15754281:'EUA',
15012486:'EUA',
95431448:'EUA',
3108351:'EUA',
3108351:'EUA',
1652541:'GLOBAL',
51241574:'GLOBAL'}



query_user = ' SELECT a.name_usuario, a.Tweets, e.Tweets_RE as "Tweets(RE)", b.Retweets, c.Replies, d.id, d.total_followers, d.total_following, d.total_posts    \
FROM \
( SELECT screen_name_usuario , name_usuario, count(*) as "Tweets"from tweet where  tweet_type = "ORIGINAL" group by screen_name_usuario, name_usuario ) AS a \
left join \
( SELECT screen_name_usuario , name_usuario, count(*) as "Tweets_RE"from tweet where  tweet_type = "ORIGINAL - RETWEET" group by screen_name_usuario, name_usuario ) AS e \
on  a.screen_name_usuario = e.screen_name_usuario \
left join \
( select retweet_from_screen_name , count(*) as "Retweets" from tweet where tweet_type = "RETWEET" group by retweet_from_screen_name ) AS b \
on  a.screen_name_usuario = b.retweet_from_screen_name \
left join \
(select in_reply_to_screen_name  , count(*) as "Replies" from tweet where tweet_type = "REPLY" group by in_reply_to_screen_name ) as c  on c.in_reply_to_screen_name = a.screen_name_usuario left join \
(SELECT id, name_usuario, total_followers, total_following, total_posts, location from user) as d \
on a.name_usuario = d.name_usuario ; '

