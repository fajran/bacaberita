from django.http import HttpResponse
from bacaberita.news.models import Feed, Article

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
			content = entry.get('summary', None)

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






