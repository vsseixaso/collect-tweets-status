# coding: utf-8
 
import tweepy
import json
import psycopg2
from time import sleep

# authentications
consumer_key = 'ZwU4lUEzjUIrCIN481bmd82KA'
consumer_secret = '8vQvWZEqPAOn23TYru6fbdsR4OkfBP9XIql0zjq2FBKUwEltof'
access_token = '967147201871929345-g4bPJJYIh0hteM8GU1Tq2OryNtpLfPE'
access_token_secret = 'o6vHoBczBW4n54d6eJX3EUtDnMovXXnPFJfd9AjjTM5HF'
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
 
def write_last_tweet_txt(i, j):
    file = open('last_tweet.txt', 'w')
    tweet = [str(i), ',', str(j)]
    file.writelines(tweet)
    file.close()

def write_error_txt():
	file = open('error.txt', 'w')
	file.writelines("error")
	file.close()

def write_unavailable_txt(tweet, matter):
	file = open('unavailable.txt', 'a')
	file.write(tweet + ' ' + matter + '\n')
	file.close()

def read_twitter_txt():
	out = []
	file = open('Twitter.txt', 'r')
	for line in file:
		aux = line.split()
		aux[0] = aux[0][4:]
		aux[1] = aux[1][6:]
		out.append(aux)
	file.close()
	return out

def read_unavailable_txt():
	out = []
	file = open('unavailable.txt', 'r')
	for line in file:
		aux = line.split()
		out.append(aux)
	file.close()
	return out

def read_last_tweet_txt():
	out = []
	file = open('last_tweet.txt', 'r')
	for line in file:
		aux = ''
		for c in line:
			if c != ',':
				aux += c
			else: 
				out.append(int(aux))
				aux = ''
		out.append(int(aux))
	file.close()
	return out

def tweet_not_added(id_tweet):
	cur.execute("SELECT * FROM tweet_status WHERE id_tweet = %s", (id_tweet,))
	tweet = cur.fetchall()
	if len(tweet) == 0: return True
	else: return False

def insert_into_matter(i):
    cur.execute("INSERT INTO matter (id_matter, label) VALUES (%s, %s)", (matters[i][0], matters[i][1]))
    conn.commit()

def insert_into_tweet_status(tweet, matter):
	cur.execute("INSERT INTO tweet_status (id_tweet, status, matter) VALUES (%s, %s, %s)", (tweet, json.dumps(api.get_status(tweet)), matter))
	conn.commit()

def added_the_unavailable_again():
	tweets = read_unavailable_txt()
	for i in xrange(len(tweets)):
		tweet = tweets[i][0]
		matter = tweets[i][1]
		if (tweet_not_added(tweet)):
			try: 
				insert_into_tweet_status(tweet, matter)
				print 'Tweet %s adicionado.               ID MAtter: %S' %(tweet, matter)
			except:
				print 'TweepError: Tweet %s indisponível. ID Matter: %s' %(tweet, matter)
 
# connecting to DB
conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
cur = conn.cursor()

# collect of data
matters = read_twitter_txt()
control = read_last_tweet_txt()
start_matter = control[0]
start_tweet = control[1] + 1
count_unavailables = 0

for i in xrange(start_matter, len(matters)):
	for j in xrange(start_tweet, len(matters[i])):
		if count_unavailables == 10:
			count_unavailables = 0
			print 'Sleep: 120 segundos'
			sleep(180)
		tweet = matters[i][j]
		matter = matters[i][0]
		try:
			if (tweet_not_added(tweet)):
				insert_into_tweet_status(tweet, matter)
				print 'Tweet %s adicionado.               ID Matter: %s' %(tweet, matter)
			else:
				print 'Tweet %s já foi adicionado.        ID Matter: %s' %(tweet, matter)
			count_unavailables = 0
		except tweepy.error.TweepError:
			write_unavailable_txt(tweet, matter)
			count_unavailables += 1
			print 'TweepError: Tweet %s indisponível. ID Matter: %s' %(tweet, matter)
		write_last_tweet_txt(i, j)
	start_tweet = 2

added_the_unavailable_again()

# close DB
cur.close()
conn.close()