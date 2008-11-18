from bacaberita.news.models import Feed, Article, Category
from django.contrib import admin

class FeedAdmin(admin.ModelAdmin):
	fields = ['feed_url', 'category']
	list_display = ('title', 'url', 'feed_url')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Article)
admin.site.register(Category)

