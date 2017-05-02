from __future__ import unicode_literals

from django.db import models

class TweetModel(models.Model):
	tweetId  = models.IntegerField( primary_key=True )
	topic = models.CharField(max_length = 100)
	text = models.CharField(max_length = 100 )
	date = models.DateField()
	lat = models.FloatField()
	lon = models.FloatField()
	sentiment  = models.CharField(max_length  = 100)
	

	def __unicode__(self):
		return self.topic