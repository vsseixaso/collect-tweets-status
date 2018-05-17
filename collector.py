# coding: utf-8
 
import tweepy
import json
import psycopg2
 
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

def write_unavailable_txt(i, j):
	id_tweet = matters[i][j]
	id_matter = matters[i][0]
	file.open('unavailable.txt', 'w')

def read_unavailable_txt():
	id_tweet = matters[i][j]
	id_matter = matters[i][0]
	fi

def read_last_tweet_txt():
	file = open('last_tweet.txt', 'r')
	out = []
	for line in file:
		aux = ''
		for c in line:
			if c != ',':
				aux += c
			else: 
				out.append(int(aux))
				aux = ''
		out.append(int(aux))
	return out

def insert_into_matter(i):
    cur.execute("INSERT INTO matter (id_matter, label) VALUES (%s, %s)", (matters[i][0], matters[i][1]))
    conn.commit()
 
def insert_into_tweet_status(i, j):
    cur.execute("INSERT INTO tweet_status (id_tweet, status, matter) VALUES (%s, %s, %s)", (matters[i][j], json.dumps(api.get_status(matters[i][j])), matters[i][0]))
    conn.commit()
 
##############################################################

matters = []
 
file = open('Twitter.txt', 'r')
for line in file:
    aux = line.split()
    aux[0] = aux[0][4:]
    aux[1] = aux[1][6:]
    matters.append(aux)
file.close()
 
# connecting to DB
conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")
cur = conn.cursor()

# last_matter = control[0]
# start_tweet = control[1] + 1

# for i in xrange(start_tweet, len(matters[last_matter])):
# 	try:
# 		insert_into_tweet_status(last_matter, i)
# 		write_last_tweet_txt(last_matter, i)
# 		print 'Tweet %s adicionado' %matters[last_matter][i]
# 	except tweepy.error.TweepError:
# 		print 'TweepError: Tweet %s indisponível' %matters[last_matter][i]

control = read_last_tweet_txt()
start_matter = control[0]
start_tweet = control[1] + 1
count_unavailable = 0
is_break = False

# for i in xrange(start_matter, len(matters)):
# 	for j in xrange(start_tweet, len(matters[i])):
# 		try:
# 			insert_into_tweet_status(i, j)
# 			write_last_tweet_txt(i, j)
# 			count_unavailable = 0
# 			print 'Tweet %s adicionado' %matters[i][j]
# 		except tweepy.error.TweepError:
# 			count_unavailable += 1
# 			if count_unavailable >= 20: is_break = True
#			write_unavailable_txt(i, j)
# 			print 'TweepError: Tweet %s indisponível' %matters[i][j]
# 			if is_break: break
# 	if is_break: break
# 	else: start_tweet = 2

write_error_txt()

# close DB
cur.close()
conn.close()