import re
import datetime
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from django.conf import settings
import sys
import json
from Analysis.code import combine,extractDataset,sentiment
import get_coordinates
import codecs


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
 
	def get_tweets(self, query, count = 5):
		tweets = []
		#testing_tweets = []
 
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
				parsed_tweet['user_id']=tweet.user.id
				loc = tweet.user.location
				#if parsed_tweet['location'] == None:
				#    print "cjxdic"
				#    parsed_tweet['location'] = "Antarctica"
				loc_list = []
				loc_list = loc.split('.')
				f=0
		  #      parsed_tweet['latitude'] = get_coordinates(parsed_tweet['location'])           
				result_loc={}
				for i in loc_list:
					result_loc={}
					result_loc=self.geo.getLongLat(i)
					if 'lat'in result_loc.keys() and 'long' in result_loc.keys():
						f=1
						break

				if f==0:
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
	def __init__(self,subj):
		self.api=TwitterClient()
		self.subj=subj;
		self.tweets=[]

	def fetchTweets(self):
		self.tweets = self.api.get_tweets(self.subj, count = 20)

		# f=open(os.path.join(BASE_DIR,"sentiment","Analysis","dataset","fetched_tweets.txt"),"w")
		# for tweet in self.tweets:
		# 	z=tweet['created_at']
		# 	f.write(str(tweet))
		# 	f.write("\n")
		# f.close()

		f=open(os.path.join(BASE_DIR,"sentiment","Analysis","dataset","Testing.txt"),"w")
		for tweet in self.tweets:
			dataset_tweet={}
			dataset_tweet['id']=tweet['id']
			dataset_tweet['user_id']=tweet['user_id']
			dataset_tweet['sentiment']=tweet['sentiment']
			dataset_tweet['text']=tweet['text']
			#print dataset_tweet.values[0]
			#z=tweet['created_at']
			# # print z.datetime
			#print dataset_tweet['id']
			f.write(str(dataset_tweet['id'])+"\t")
			f.write(str(dataset_tweet['user_id'])+"\t")
			f.write(str(dataset_tweet['sentiment'])+"\t")
			f.write(self.api.clean_tweet(dataset_tweet['text']))
			f.write("\n")
		f.close()
		


		extractDataset.extract()
		
		os.system(os.path.join(BASE_DIR,"sentiment","Analysis","ark-tweet-nlp","runTagger.sh")
			+ " " 
			+ os.path.join(BASE_DIR,"sentiment","Analysis","dataset","example_tweets.txt")
			+ " > " 
			+ os.path.join(BASE_DIR,"sentiment","Analysis","dataset","testingTokenised.txt")) 
		combine.combine()
		sentiment.classify()

		f=open(os.path.join(BASE_DIR,"sentiment","Analysis","code","taskB.pred"),"r")
		
		i=0
		for sent in f:
			self.tweets[i]['sentiment']=str(sent)
			i+=1

		return self.tweets
		# self.ptweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'positive']
		# self.ntweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'negative']
		# self.neutral=[tweet for tweet in self.tweets if tweet['sentiment']=='neutral']
# obj=TwitterObject("ipl")
# obj.fetchTweets()
