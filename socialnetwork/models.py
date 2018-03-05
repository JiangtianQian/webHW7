from __future__ import unicode_literals


from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from django.db.models import Max
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

# Create your models here.
class Post(models.Model):
	text = models.CharField(max_length=42)
	user = models.ForeignKey(User)
	postTime = models.DateTimeField(auto_now_add=True, blank=True)
	def html(self):
		context= {}
		context['user'] = self.user
		context['text'] = self.text
		context['postTime'] = self.postTime
		context['username'] = self.user
		context['id'] = self.id
		return render_to_string("socialnetwork/postTemplate.html",context).replace('\n','')

	@staticmethod
	def get_max_time():
		if Post.objects.all().aggregate(Max('postTime'))['postTime__max']:
			return Post.objects.all().aggregate(Max('postTime'))['postTime__max'] 
		else:
			return "2017-01-01T00:00+00:00"
	
	@staticmethod
	def get_changes(time="2018-01-01T00:00+00:00"):
		return Post.objects.filter(postTime__gt=time).distinct()

	@staticmethod
	def get_items(time="2018-01-01T00:00+00:00"):
		return Post.objects.filter(postTime__gt=time).distinct().order_by('postTime').reverse()

	# return items in follower list
	@staticmethod
	def get_max_timeFollow(user):
		follow = get_object_or_404(User, username = user)
		item = Post.objects.filter(user = follow)
		if item.aggregate(Max('postTime'))['postTime__max']:
			return item.aggregate(Max('postTime'))['postTime__max']
		else:
			return "2018-01-01T00:00+00:00"


	@staticmethod
	def get_changesFollow(user,time):
		if time == "undefined" or time == None:
			time ="2018-01-01T00:00+00:00"
		item = Post.objects.filter(user = user)
		if len(item) > 0:
			return item.filter(postTime__gt=time).distinct()
		else:
			return item


class Profile(models.Model):
	user = models.OneToOneField(User,primary_key = True)
	first_name = models.CharField(max_length=42)
	last_name = models.CharField(max_length=42)
	email = models.EmailField(max_length=42)
	follow = models.ManyToManyField(User, related_name = 'follows')
	picture = models.ImageField(upload_to = "addr-photos/", blank = True)
	itemPost = models.ManyToManyField(Post, related_name = 'post')


class CommentPost(models.Model):
	user = models.ForeignKey(User)
	commentWhichPost = models.ForeignKey(Post)
	text = models.CharField(max_length=42)
	mypostTime = models.DateTimeField(auto_now_add=True, blank=True)

	def html(self):
		context = {}
		context['username'] = self.user.username
		context['text'] = self.text
		context['postTime'] = self.mypostTime
		context['id'] = self.id
		context['user'] = self.user
		return render_to_string("socialnetwork/commentTemplate.html",context).replace('\n','')

	@staticmethod
	def get_items(item):
		comment = CommentPost.objects.filter(commentWhichPost = item)
		if len(comment) > 0:
			return comment.distinct().order_by('mypostTime')
			
		else:
			return comment
			
	@staticmethod
	def get_max_time(item):
		comment = CommentPost.objects.filter(commentWhichPost = item)
		return comment.aggregate(Max('mypostTime'))['mypostTime__max'] or "2018-01-01T00:00+00:00"
	
	@staticmethod
	def get_changes(item,time="2018-01-01T00:00+00:00"):
		comment = CommentPost.objects.filter(commentWhichPost = item)
		if len(comment) > 0:
			max_time = CommentPost.objects.filter(commentWhichPost = item).latest('mypostTime').mypostTime
			print(max_time)
			return comment.filter(mypostTime=max_time).distinct()
		else:
			return comment
			








