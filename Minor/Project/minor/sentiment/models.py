from __future__ import unicode_literals

from django.db import models

class TweetModel(models.Model):
	date = models.DateTimeField()
	location = models.CharField(max_length = 100)
	positive = models.IntegerField()
	negative = models.IntegerField()
	neutral = models.IntegerField()
	timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)
	updated=models.DateTimeField(auto_now_add=False,auto_now=True)
	class Meta:
		unique_together = (('date', 'location'),)
	
	def __unicode__(self):
		return self.location