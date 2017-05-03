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
	final=[]
	sentiment = []
	subj=request.session.get('form')['searchBox']		
		
	context = {
		'subj' : subj,
		'date' : searched_date,
		'lat' : lat,
		'lon' : lon,
		'sentiment' : sentiment,
		'len' : 0
	}
	
	if form.is_valid():
		if not subj:
			return render(request,'tweetView.html',context)

		obj=TwitterObject(subj)
		tweets = obj.fetchTweets()
		
		dbTweets = TweetModel.objects.all().filter(topic = subj, date=str(searched_date))
		tweetId = []
		
		for tweet in dbTweets :
			sentData = {}

			lat.append(tweet.lat)
			lon.append(tweet.lon)
			sentiment.append(tweet.sentiment)
			sentData['latitude'] = tweet.lat
			sentData['longitude'] = tweet.lon
			sentData['sentiment'] = tweet.sentiment
			final.append(sentData)
	
		for tweet in tweets:
			entity = TweetModel(tweetId = tweet.get('id'), 
				topic = subj , 
				text = tweet.get('text') ,
				date = tweet.get('created_at').now().date(),
				lat =  tweet.get('lat'),
				lon = tweet.get('long'),
				sentiment = tweet.get('sentiment'))
			if entity.tweetId not in tweetId:

				sentData={}
				sentData['latitude'] = entity.lat
				sentData['longitude'] = entity.lon
				sentData['sentiment'] = entity.sentiment
				
				final.append(sentData)
		
				lat.append(entity.lat)
				lon.append(entity.lon)
				sentiment.append(entity.sentiment)
				tweetId.append(entity.tweetId)
				entity.save()	
		f = open(os.path.join(settings.BASE_DIR,"templates","data.json"),"w")
		for data in final:
			json.dump(data,f)
			f.write("\n")
			# print r
		f.close()
		print len(lat)
	context = {
		'subj' : subj,
		'date' : searched_date,
		'lat' : lat,
		'lon' : lon,
		'sentiment' : sentiment,
		'len' : len(lat)
	}
	
	return render(request,'ad3.html',context)