# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from socialnetwork.models import *
from socialnetwork.forms import *

from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.db import transaction

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

# Create your views here.

@login_required
def home(request):
	context = {}
	context['form'] = Postform()
	context['formOfComment'] = Commentform()
	return render(request, 'socialnetwork/home.html', context)

@login_required
def myProfile(request):
	try:
		print(request.POST)

		print(request.user)

		print("enter myProfile")


		for p in Profile.objects.all():
			print("a")
			print(p.user)


		context = {}
		bio = get_object_or_404(Profile, user = request.user)

		print("enter myProfile3")


		item = Post.objects.filter(user = request.user).order_by('postTime').reverse()

		print("enter myProfile2")

		context = {'username': request.user,\
		'firstname': bio.first_name,\
		'lastname': bio.last_name,\
		'email': bio.email,\
		'items':item,\
		'bio': bio,\
		'userid': request.user.id}

		print("enter myProfile4")

		print(context)

		return render(request, 'socialnetwork/myProfile.html',context)
	except:
		return redirect('/home')



@login_required
def otherProfile(request, userid):
	context = {}
	try:

		print("here")

		myId = get_object_or_404(User, username = request.user)

		print("here1")

		mine = get_object_or_404(Profile, user = myId)
		otherId = User.objects.get(username = userid)
		otherProfile = get_object_or_404(Profile, user = otherId)
		otherItemSet = Post.objects.filter(user = otherId).order_by('postTime').reverse()

		otherUser = otherId
		bio = otherProfile

		print("here2")

		context = {'username': otherUser.username,\
		'firstname': otherUser.first_name,\
		'lastname': otherUser.last_name,\
		'email': otherUser.email,\
		'items': otherItemSet,\
		'userid': otherUser.id,\
		'bio':bio}

		print("here3")


		if myId.username == otherId.username:
			#context['other'] = True
			return redirect("/myProfile")

		if otherId in mine.follow.all():
			print("true")
			context["flag"] = "False"
		else:
			context["flag"] = "True"

		print("here2")

		return render(request, 'socialnetwork/otherProfile.html',context)
	except:
		return redirect('/home')
		#return render(request, 'socialnetwork/otherProfile.html',context)



def register(request):

	print("jinlai register")
	context = {}
	form = RegisterForm(request.POST)
	context['form'] = form
	try:
		if request.method == 'GET':
			context['form'] = RegisterForm()
			return render(request, 'socialnetwork/register.html', context)
		if not form.is_valid():
			return render(request, 'socialnetwork/register.html', context)
		username = form.cleaned_data.get('username')
		password1 = form.cleaned_data.get('password1')
		email = form.cleaned_data.get('email')
		first_name = form.cleaned_data.get('first_name')
		last_name = form.cleaned_data.get('last_name')
		new_user = User.objects.create_user(username=username,\
											password=password1,\
											email=email,\
											first_name=first_name, \
											last_name=last_name,\
											is_active=False)
		print("token2")

		new_user.save()


		new_Profile = Profile(first_name=first_name, \
			last_name=last_name, \
			user = new_user,\
			email = email)
		new_Profile.save()


		token = default_token_generator.make_token(new_user)

		print("token3")
		email_body = """Please click the link below to verify your email address and complete the registration of your account:
		http://{host}{path}""".format(host=request.get_host(), 
           path=reverse('confirm', args=(new_user.username, token)))

		print("token5")

		print(new_user.email)

		send_mail(subject="Verify your email address",
              message= email_body,
              from_email = "jiangtiq@andrew.cmu.edu",
              recipient_list=[new_user.email])

		print("token4")

		context['emailconfirm'] = email

		print("token1")

		return render(request, 'socialnetwork/emailConfirm.html', context)
	except:
		return redirect('/login')	


@login_required
def updateProfile(request):
	edited_profile = Profile.objects.select_for_update().get(user = request.user)
	try:
		if request.method == "get":
			form = ProfileForm()
			context['form'] = ProfileForm()
			return render(request,'socialnetwork/updateProfile.html',context)
		
		form = ProfileForm(request.POST, request.FILES, instance = edited_profile)
		context = {'form':form}	
		if not form.is_valid():
			return render(request,'socialnetwork/updateProfile.html',context)
		form.save()
		return render(request, 'socialnetwork/updateProfile.html',context)
	except:
		return redirect('/home')

@login_required
def get_photo(request, userid):
	userId = User.objects.get(id = userid)
	profile = get_object_or_404(Profile, user = userId)
	if not profile.picture:
		raise Http404
	content_type = guess_type(profile.picture.name)
	return HttpResponse(profile.picture, content_type= content_type)


@login_required
@transaction.atomic
def follow(request, username):
	print("follow")
	context = {}
	userId = get_object_or_404(User, username = request.user)
	follow = get_object_or_404(User, username = username)
	profile = get_object_or_404(Profile, user = userId)
	profile.follow.add(follow)
	profile.save()
	url = follow.username
	print("hahah")
	print(url)
	return redirect('/otherProfile/' + str(url))



@login_required
@transaction.atomic
def unFollow(request, username):
	context = {}
	userId = get_object_or_404(User, username = request.user)
	follow = get_object_or_404(User, username = username)
	profile = get_object_or_404(Profile, user = userId)
	profile.follow.remove(follow)
	profile.save()
	url = follow.username
	return redirect('/otherProfile/'+str(url))

@login_required
def followStream(request):
	context = {}
	if request.method == "get":
		context['form'] = ProfileForm()
		return render(request, 'socialnetwork/follow.html',context)
	try:
		profile = get_object_or_404(Profile, user = request.user)

		profile_all = Profile.objects.all()
		
		follower = profile.follow.all()
		
		result = []
		tmp = []
		tmp_id = []
		print("========================================")
		result = Post.objects.filter(user__in = profile.follow.all()).order_by('postTime').reverse()
		print("000000000000000000")

		for r in result:
			if r.user not in tmp_id:
				tmp.append(r)
				tmp_id.append(r.user)

		context['follower'] = tmp

		context['items'] = result
		context['followStatue'] = "True"
		context['comment'] = CommentPost.objects.all()
		for item in CommentPost.objects.all():
			print(item.postID)

		return render(request, 'socialnetwork/follow.html',context)
	except:
		return render(request, 'socialnetwork/follow.html',context)

@login_required
def get_items(request, time="2018-01-01T00:00+00:00"):
	if time == "undefined" :
		time="2018-01-01T00:00+00:00"
	max_time = Post.get_max_time()
	items = Post.get_items(time)
	context = {"max_time":max_time, "items":items}

	print("enter get items now")

	return render(request, 'socialnetwork/items.json', context, content_type='application/json')

@login_required
def postform(request):
	context = {}
	form = Postform(request.POST)
	context['form'] = form
	if not form.is_valid():
		raise Http404
	text = form.cleaned_data.get('text')
	new_item = Post(text = text, user = request.user)
	new_item.save()
	return HttpResponse("")

@login_required
def commentform(request):
	context = {}
	if request.POST['text'] == ' ' or request.POST['text'] == '':
		raise Http404
	if request.POST['postID'] == ' ':
		raise Http404

	print(request.POST)

	postid = int(request.POST['postID'])
	postID = Post.objects.get(id = int(postid))
	new_item = CommentPost(text=request.POST['text'], user = request.user,commentWhichPost = postID)
	new_item.save()
	max_time = CommentPost.get_max_time(postID)
	context = {"max_time":max_time, "postid":postID.id} 
	return render(request, 'socialnetwork/comment.json', context, content_type='application/json')


@login_required
def get_changes(request, time="2018-01-01T00:00+00:00"):
	try:
		if time == "undefined" :
			time="2018-01-01T00:00+00:00"
		max_time = Post.get_max_time()
		items = Post.get_changes(time)
		context = {"max_time":max_time, "items":items}
		return render(request, 'socialnetwork/items.json', context, content_type='application/json')
	except:
		return redirect('/home')


@login_required
def get_commentchanges(request,item_id, time="2018-01-01T00:00+00:00"):
    postID = Post.objects.get(id = int(item_id))
    max_time = CommentPost.get_max_time(postID)
    items = CommentPost.get_changes(postID,time)
    context = {"max_time":max_time, "items":items} 
    return render(request, 'socialnetwork/items.json', context, content_type='application/json')

@login_required
def get_commentall(request,item_id):
	max_time = CommentPost.get_max_time(item_id)
	items = CommentPost.get_items(item_id)
	context = {"max_time":max_time, "items":items}
	return render(request, 'socialnetwork/items.json', context, content_type='application/json')

def visitor(request):
	context = {}
	context['items'] = Item.objects.all().order_by('postTime').reverse()
	context['form'] = ItemForm()
	return render(request, 'socialnetwork/logout.html',context)

@login_required
def get_changeFollow(request, username, time):
    if time == "undefined" or time ==None:
        time="2018-01-01T00:00+00:00"
    max_time = Post.get_max_timeFollow(username)
    user = User.objects.get(username = username)
    items = Post.get_changesFollow(user, time)
    context = {"max_time":max_time, "items":items}
    return render(request, 'socialnetwork/items.json', context, content_type='application/json')


@login_required
def get_follow(request, username):

	print("enter get_follow")

	user = User.objects.get(username = username)


	max_time = Post.get_max_timeFollow(user)

	
	profile = get_object_or_404(Profile, user = request.user)

	profile_all = Profile.objects.all()
	
	follower = profile.follow.all()
		
	result = []

	print("========================================")
	result = Post.objects.filter(user__in = profile.follow.all()).order_by('postTime').reverse()
	print("000000000000000000")

	items = result

	#items = Post.get_itemsFollow(user)


	for i in items:
		print(i.user)

	context = {"max_time":max_time, "items":items}
	return render(request, 'socialnetwork/items.json', context, content_type='application/json')



def confirm(request, username, token):

	print("what are you talking about")
	
	try:
		print("1")
		user = User.objects.get(username = username)
	except:
		raise Http404
	try:
		print("2")
		if not default_token_generator.check_token(user,token):
			print("raise token")
			raise redirect('/login')

		print("oyt of token")
		user.is_active = True
		user.save()

		print(" out of token2")


		#login in 
		new_user = authenticate(username=username,\
								password=user.password)
		login(request,user)

		print("4")
		return redirect('/home')
	except:
		return redirect('/login')




