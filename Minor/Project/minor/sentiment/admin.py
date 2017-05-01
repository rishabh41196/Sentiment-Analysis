from django.contrib import admin
from .models import TweetModel
# Register your models here.

class TweetModelAdmin(admin.ModelAdmin):
	pass
admin.site.register(TweetModel, TweetModelAdmin)