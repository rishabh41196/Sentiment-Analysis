from django.contrib import admin

from .models import TweetModel
# Register your models here.

class TweetModelAdmin(admin.ModelAdmin):
	list_display = ('tweetId','topic','text','sentiment','date')
admin.site.register(TweetModel, TweetModelAdmin)