from django.http import HttpResponse
from bacaberita.news.models import Feed, Article

import datetime
import feedparser
import time

__all__ = ['update']

def update(request):
	feeds = Feed.objects.all()

	html = ""
	html += "<p>%d feeds updated.</p>" % len(feeds)
	html += "<ul>"

	for feed in feeds:
		
		data = feedparser.parse(feed.feed_url)
		
		feed.title = data.feed.title
		feed.url = data.feed.link
		feed.save()

		html += "<li><a href='%s'>%s</a>" % (feed.url, feed.title)
		cnt = 0

		for entry in data.entries:
			article_id = entry.id
			title = entry.title
			url = entry.link
			date = entry.date_parsed

			author = entry.get('author', None)

			try:
				content = entry.get('summary', None)
				if not content:
					content = entry.content[0].value
			except:
				pass

			if not Article.objects.filter(article_id=article_id, feed=feed):
				article = Article(
					feed=feed,
					author=author,
					url=url,
					date=time.strftime("%Y-%m-%d %H:%M:%S", date),
					title=title,
					content=content,
					article_id=article_id)
				article.save()

				cnt += 1

		html += " (new: %d)</li>" % cnt

	html += "</ul>"

	return HttpResponse(html)

def index(req):

	time_read_limit = datetime.datetime.today() - datetime.timedelta(minutes=30)
	articles = Article.objects.exclude(time_read__lt=time_read_limit).order_by('-date').order_by('feed__title', 'clipped')

	html = ''
	last_feed = None

	for entry in articles:
		if last_feed != entry.feed:
			if last_feed != None:
				html += '</ul>'

			html += '<h2><a href="%s">%s</a></h2>' % (entry.feed.url, entry.feed)
			html += '<ul>'

		html += '<li><div><h3><a href="%s">%s</a></a></h3></div>' % (entry.url, entry.title)

		if entry.content:
			cls = ""
			if entry.clipped:
				cls = "clipped"

			html += '<div%s>%s</div>' % (cls, entry.content)

		html += '</li>'

		last_feed = entry.feed
	
	html += '</ul>'

	time_read = datetime.datetime.today()
	for entry in articles:
		if not entry.time_read:
			entry.time_read = time_read
			entry.save()

	return HttpResponse(html)
		
		
	




