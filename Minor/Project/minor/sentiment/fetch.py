import re
import datetime
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from django.conf import settings
import sys
import json
from Analysis.code import combine,extractDataset
import get_coordinates


BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TwitterClient(object):
	'''Twitter class for senti analysis.'''
	def __init__(self):
		CONSUMER_KEY = 'U0xGDJZFfpZamK9awid8Fu5j0'
		CONSUMER_SECRET = 'GnAAVyQCCZnMClGYNs5dEvuRNxVdn2AvuSrsRrk8hzonL9HwEz'
		ACCESS_TOKEN = '583456685-GeqhFLNky6XTYYSKuo6SGq3LWzR5uqOtyA2bEbGr'
		ACCESS_TOKEN_SECRET = 'AzvIobGpbBmuJj3PyTRJP9adTQuVv1OwXu0dmA0854BO5'
	
		self.geo=get_coordinates.Geocoding()

		# consumer_key = settings.CONSUMER_KEY
		# consumer_secret = settings.CONSUMER_SECRET
		# access_token = settings.ACCESS_TOKEN
		# access_token_secret = settings.ACCESS_TOKEN_SECRET
 
		try:
			self.auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication failed")
 
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
	def get_tweet_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))    
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'
 
	def get_tweets(self, query, count = 50):
		tweets = []
 
		try:
			fetched_tweets = self.api.search(q = query, count = count)
			#print fetched_tweets
			for tweet in fetched_tweets:
				
				parsed_tweet = {}
				non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
				parsed_tweet['text'] = tweet.text.translate(non_bmp_map)
				parsed_tweet['created_at']=tweet.created_at
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
				parsed_tweet['id'] = tweet.id
				parsed_tweet['location'] = tweet.user.location
				#if parsed_tweet['location'] == None:
				#    print "cjxdic"
				#    parsed_tweet['location'] = "Antarctica"
				loc_list = []
				loc_list = parsed_tweet['location'].split('.')
				f=0
		  #      parsed_tweet['latitude'] = get_coordinates(parsed_tweet['location'])           
				result_loc={}
				for i in loc_list:
					result_loc={}
					result_loc=self.geo.getLongLat(i)
					if 'lat'in result_loc.keys() and 'long' in result_loc.keys():
						parsed_tweet['location'] = i
						f=1
						break

				if f==0:
					parsed_tweet['location'] = "Antartica"
					result_loc={}
					result_loc=self.geo.getLongLat("Antartica")

				parsed_tweet['lat']=result_loc['lat']
				parsed_tweet['long']=result_loc['long']
				
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
 
			return tweets
 
		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))
class TwitterObject(object):
	def __init__(self):
		self.api=TwitterClient()
		self.subj='';
		self.ptweets=[]
		self.tweets=[]
		self.ntweets=[]
		self.neutral=[]

	def fetchTweets(self):
		self.tweets = self.api.get_tweets(self.subj, count = 200)

		f=open(os.path.join(BASE_DIR,"sentiment","Analysis","dataset","fetched_tweets.txt"),"w")
		for tweet in self.tweets:
			z=tweet['created_at']
			# print z.datetime
			f.write(str(tweet))
			f.write("\n")
		f.close()
		extractDataset.extract()
		os.system(os.path.join(BASE_DIR,"sentiment","Analysis","ark-tweet-nlp","runTagger.sh")
			+ " " 
			+ os.path.join(BASE_DIR,"sentiment","Analysis","dataset","example_tweets.txt")
			+ " > " 
			+ os.path.join(BASE_DIR,"sentiment","Analysis","dataset","testingTokenised.txt")) 
		combine.combine()

		# self.ptweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'positive']
		# self.ntweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'negative']
		# self.neutral=[tweet for tweet in self.tweets if tweet['sentiment']=='neutral']


obj = TwitterObject()
obj.subj="epl"
obj.fetchTweets()