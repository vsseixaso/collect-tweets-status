import tweepy

# authentications
consumer_key = 'ZwU4lUEzjUIrCIN481bmd82KA'
consumer_secret = '8vQvWZEqPAOn23TYru6fbdsR4OkfBP9XIql0zjq2FBKUwEltof'
access_token = '967147201871929345-g4bPJJYIh0hteM8GU1Tq2OryNtpLfPE'
access_token_secret = 'o6vHoBczBW4n54d6eJX3EUtDnMovXXnPFJfd9AjjTM5HF'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# reading Twitter.txt and fill matters
matters = []

file = open('Twitter.txt', 'r')
for line in file:
	aux = line.split()
	aux[0] = aux[0][4:]
	aux[1] = aux[1][6:]
	matters.append(aux)

# collect tweets status
for matter in xrange(len(matters)):
	for tweet_id in xrange(2, len(matters[matter])):
		try:
			print api.get_status(matters[matter][tweet_id]).text
		except tweepy.error.TweepError:
			print "Tweet indisponível"
