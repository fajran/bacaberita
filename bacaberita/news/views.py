from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils import simplejson

from bacaberita.news.models import Feed, Article, Category

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

def read(req, type=None, id=None):
	articles = get_articles(type, id)

	template = get_template('news_read.html')
	html = template.render(Context({
		'articles': articles
	}))

	return HttpResponse(html)

def json(req, type=None, id=None):
	articles = get_articles(type, id)

	json = simplejson.dumps(articles)

	return HttpResponse(json, content_type="text/x-json")

def index(req):
	categories = get_categories()

	template = get_template('news_index.html')
	html = template.render(Context({
		'categories': categories[0],
	}))

	return HttpResponse(html)

def get_categories():
	categories = Category.objects.all().order_by('id', 'parent__id', 'title')

	res = {}
	res[0] = {
		'id': 0,
		'title': 'root',
		'children': []
	}

	for category in categories:
		if category.parent == None:
			parent_id = 0
		else:
			parent_id = category.parent.id

		item = {
			'id': category.id,
			'title': category.title,
			'children': [],
			'feeds': []
		}

		feeds = Feed.objects.filter(category__id=category.id)
		for feed in feeds:
			item['feeds'].append({
				'id': feed.id,
				'title': feed.title
			})

		res[category.id] = item

		parent = res[parent_id]
		parent['children'].append(item)


	print repr(res)
	return res

def get_articles(type=None, id=None):

	try:
		id = int(id)
	except ValueError:
		id = -1
	except TypeError:
		id = -1
	
	time_read_limit = datetime.datetime.today() - datetime.timedelta(minutes=1130)
	articles = Article.objects.exclude(time_read__lt=time_read_limit).order_by('-date').order_by('feed__title', 'clipped')

	if type == 'cat':
		articles = articles.filter(feed__category__id=id)
	elif type == 'feed':
		articles = articles.filter(feed__id=id)

	html = ''
	last_feed = None

	feed = {}
	res = []

	time_read = datetime.datetime.today()

	for entry in articles:
		if last_feed != entry.feed:
			if last_feed != None:
				res.append(feed)

			feed = {}
			feed['url'] = entry.feed.url
			feed['title'] = entry.feed.title
			feed['entries'] = []

		feed['entries'].append({
			'url': entry.url,
			'title': entry.title,
			'content': entry.content,
			'clipped': entry.clipped
		})

		last_feed = entry.feed

		if not entry.time_read:
			entry.time_read = time_read
			entry.save()

	res.append(feed)
	
	return res
		
	




