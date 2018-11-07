## Environment Configuration

Install packages using pip and requeirements.txt file

```
pip install -r requirements.txt
```


## Create a new dataase and db user 

MySql Example:

```
CREATE DATABASE "table_name" CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE "user_name"@localhost;
SET PASSWORD FOR "user_name"@localhost = password(' - the password - ');
GRANT ALL PRIVILEGES ON "table_name".* to "user_name"@localhost IDENTIFIED BY " - the password - ";
FLUSH PRIVILEGES;

```
It is assumed that the database server is already installed and configrued.


## Twitter api Access

Create the "pass_tw.py" inside project root folder with twitter api keys, tokens ans secrets

```
CONSUMER_KEY = "Your Consumer Key"
CONSUMER_SECRET = "Your Consumer Secret"
ACCESS_TOKEN  = "Your Token"
ACCESS_TOKEN_SECRET  = "Your token secret"

```

## Database tables creation

Execute the script to create the tables to store the tweets in the database

```
python db_init.py

```

## Define the stream filters and init capturing tweets

inside the file stram_db_init.py, change the parameters(filters) for the client in:

```
# Exemple filter by a group of ids

follow = ['8802752','9317502'] 
resource = client.stream.statuses.filter.post(follow=follow)

```

Execute the script to start capturing tweets

```
python stream_db_twitter.py

```

## Monitor the catured tweets  
Start the flask app and ckeck http://localhost:8080

```
python app.py

```
# twitter_user_stat_stream
