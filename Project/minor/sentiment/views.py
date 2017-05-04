from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.conf import settings
from .forms import SearchBox
from .models import TweetModel
from .fetch import TwitterObject
from datetime import datetime
import json
import os
def home(request):
	form=SearchBox(request.POST or None)
	context = {
		'form': form,
	}
	if form.is_valid():
		request.session['date'] = str(datetime.now().date())
		request.session['form'] = request.POST
		return HttpResponseRedirect('tweetView')
	return render(request,'base.html',context)

def tweetView(request):
	form=SearchBox(request.session.get('form'))
	searched_date=request.session.get('date')
	lat=[]
	lon = []
	lis=[]
	final=[]
	sentiment = []
	subj=request.session.get('form')['searchBox']		

 	if request.POST.get('timestamp') is not None:
 		received_datetime = datetime.strptime(request.POST.get('timestamp'),  '%d-%m-%Y %H:%M:%S')
 		searched_date = received_datetime.date()


	context = {
		'subj' : subj,
		'pos': 0,
		'neg' : 0,
		'neut': 0,
		'date' : searched_date,
		'lat' : lat,
		'lon' : lon,
		'sentiment' : sentiment,
		'len' : 0,
		'lis' : lis
	}
	


	if form.is_valid():
		if not subj:
			return render(request,'tweetView.html',context)
		tweets=[]
		if str(searched_date) == str(datetime.now().date()):
			obj=TwitterObject(subj)
			tweets = obj.fetchTweets()
			
		dbTweets = TweetModel.objects.all().filter(topic = subj, date=str(searched_date))
		tweetId = []
		for tweet in dbTweets :
			if str(tweet.date) == str(searched_date):
				sentData = {}
				lat.append(float(tweet.lat))
				lon.append(float(tweet.lon))
				sentiment.append(tweet.sentiment)
				sentData['latitude'] = tweet.lat
				sentData['longitude'] = tweet.lon
				sentData['sentiment'] = tweet.sentiment
				final.append(sentData)
		
		for tweet in tweets:
			# print tweet.get('location')
			entity = TweetModel(tweetId = tweet.get('id'), 
				topic = subj , 
				text = tweet.get('text') ,
				date = tweet.get('created_at').now().date(),
				lat =  tweet.get('lat'),
				lon = tweet.get('long'),
				sentiment = tweet.get('sentiment'))
			if entity.tweetId not in tweetId:
				if str(entity.date) == str(searched_date):
					sentData={}
					sentData['latitude'] = entity.lat
					sentData['longitude'] = entity.lon
					sentData['sentiment'] = entity.sentiment
					lat.append(float(entity.lat))
					lon.append(float(entity.lon))
					sentiment.append(entity.sentiment)			
					final.append(sentData)
				tweetId.append(entity.tweetId)
				entity.save()	
		ct=0
		l= len(final)

		pos=0
		neg=0
		neut=0

		sentiment = json.dumps(sentiment)
		lon=json.dumps(lon)
		lat=json.dumps(lat)
		
		for tweet in final:
			if(tweet['sentiment']=='positive'):
				pos+=1;
			elif(tweet['sentiment']=='negative'):
				neg+=1;
			else:
				neut+=1;


	context = {
		'subj' : subj,
		'pos': pos,
		'neg' : neg,
		'neut': neut,
		'date' : searched_date,
		'lat' : lat,
		'lon' : lon,
		'sentiment' : sentiment,
		'len' : len(lat),
		'lis' : lis
	}

	return render(request,'ad3.html',context)