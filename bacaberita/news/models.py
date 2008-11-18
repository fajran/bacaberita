from django.db import models

class Article(models.Model):
	author = models.CharField(max_length=255, null=True, blank=True)
	url = models.URLField()
	date = models.DateTimeField()
	title = models.CharField(max_length=255)
	content = models.TextField(null=True)
	article_id = models.CharField(max_length=255)

	feed = models.ForeignKey('Feed')

	time_read = models.DateTimeField(null=True, default=None)
	clipped = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

class Feed(models.Model):
	title = models.CharField(max_length=255)
	url = models.URLField()
	feed_url = models.URLField()

	category = models.ForeignKey('Category', null=True)

	def __unicode__(self):
		if self.title:
			return self.title
		else:
			return self.feed_url

class Category(models.Model):
	parent = models.ForeignKey("self", null=True, blank=True)
	
	title = models.CharField(max_length=255)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Categories'

