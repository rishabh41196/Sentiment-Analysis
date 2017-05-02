from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from .forms import SearchBox
from .models import TweetModel
from .fetch import TwitterObject
from datetime import datetime
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
	print request.session
	# searched_date=SearchBox(request.session.get('date'))
	lat=[]
	lon = []
	final=[]
	sentiment = []
	context = {
		'lat' : lat,
		'lon' : lon,
		'sentiment' : sentiment,
	}
	# print searched_date

	# if form.is_valid():
	# 	subj=request.session.get('form')['searchBox']		
	# 	if not subj:
	# 		return render(request,'tweetView.html',context)

	# 	obj=TwitterObject(subj)
	# 	tweets = obj.fetchTweets()
		
	# 	dbTweets = TweetModel.objects.all().filter(topic = subj, date=str(searched_date))
	# 	tweetId = []
		
	# 	for tweet in dbTweets :
	# 		sentData = {}

	# 		lat.append(str(tweet.lat))
	# 		lon.append(str(tweet.lon))
	# 		sentiment.append(tweet.sentiment)
	# 		sentData['lat'] = str(tweet.lat)
	# 		sentData['lon'] = str(tweet.lon)
	# 		sentData['sentiment'] = tweet.sentiment
	# 		final.append(dbTweets)
	
	# 	for tweet in tweets:
	# 		entity = TweetModel(tweetId = tweet.get('id'), 
	# 			topic = subj , 
	# 			text = tweet.get('text') ,
	# 			date = tweet.get('created_at').now().date(),
	# 			lat =  tweet.get('lat'),
	# 			lon = tweet.get('long'),
	# 			sentiment = tweet.get('sentiment'))
	# 		if entity.tweetId not in tweetId:
	# 			lat.append(str(entity.lat))
	# 			lon.append(str(entity.lon))
	# 			sentiment.append(entity.sentiment)
	# 			tweetId.append(entity.tweetId)
	# 			entity.save()	

	# print lat
	# print lon
	# print sentiment
	# context = {
	# 	'data' : final,
	# 	'lat' : lat,
	# 	'lon' : lon,
	# 	'sentiment' : sentiment,
	# }
	
	return render(request,'tweetView.html',context)