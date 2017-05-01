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
		request.session['form']=request.POST
		return HttpResponseRedirect('tweetView')
	return render(request,'base.html',context)

def tweetView(request):
	form=SearchBox(request.session.get('form'))
	final=[]
	context = {
		'data' : final
	}

	if form.is_valid():
		subj=request.session.get('form')['searchBox']		
		if not subj:
			return render(request,'tweetView.html',context)

		obj=TwitterObject(subj)
		tweets = obj.fetchTweets()
		
		dbTweets = TweetModel.objects.all().filter(topic = subj)


		for tweet in dbTweets :
			sentData = {}
			sentData['lat'] = tweet.lat
			sentData['lon'] = tweet.lon
			sentData['sentiment'] = tweet.sentiment
			final.append(dbTweets)
				 

		for tweet in tweets:
			entity = TweetModel(tweetId = tweet['id'], 
				topic = subj , 
				text = tweet['text'] ,
				date = tweet['created_at'],
				lat =  tweet['lat'],
				lon = tweet['long'],
				sentiment = tweet['sentiment'])
			if entity not in dbTweets:
				sentData = {}
				sentData['lat'] = entity.lat
				sentData['lon'] = entity.lon
				sentData['sentiment'] = entity.sentiment
				final.append(dbTweets)
				entity.save()

	context = {
		'data' : final
	}
	
	return render(request,'tweetView.html',context)

	# form = get_object_or_404(str, pk=city_id)
	# deals = Deal.objects.filter(city=city)