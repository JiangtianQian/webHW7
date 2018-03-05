from django import forms

from django.contrib.auth.models import *

from django.forms import ModelForm

from socialnetwork.models import *
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
	username = forms.CharField(max_length = 20,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
	first_name = forms.CharField(max_length = 20,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
	last_name = forms.CharField(max_length = 20,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
	email = forms.EmailField(max_length = 30,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
	password = forms.CharField(max_length = 20,
		widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
	confirm = forms.CharField(max_length = 20,
		widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}))
	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		confirm = cleaned_data.get('confirm')
		if User.objects.filter(username = username):
			raise forms.ValidationError("User already exist.")
		if password and password and password != confirm:
			raise forms.ValidationError("Passwords did not match.")
		return cleaned_data

class Postform(forms.Form):
        text = forms.CharField(max_length = 100, 
                     widget = forms.TextInput(attrs={'class': 'bubble', 'placeholder': 'Say something', 'cols': "200", 'rows':"5"}))

        def clean(self):
            cleaned_data = super(Postform, self).clean()
            post = cleaned_data.get('post')
            return cleaned_data


class Commentform(forms.Form):
        text = forms.CharField(max_length = 42, 
                     label='Comment', 
                     widget = forms.Textarea(attrs={'class': 'comment','placeholder': 'Comment' }))
        postID = forms.IntegerField()
       

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['follow','user','itemPost']
		widgets = {'picture' : forms.FileInput(),
		'short_bio' : forms.Textarea(attrs={'placeholder': 'Short Bio'}),
		'first_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
		'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
		'email':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})}
		def clean(self):
			cleaned_data = super(ProfileForm, self).clean()
			return cleaned_data
