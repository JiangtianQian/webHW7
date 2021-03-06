# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 18:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=42)),
                ('mypostTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=42)),
                ('postTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=42)),
                ('last_name', models.CharField(max_length=42)),
                ('email', models.EmailField(max_length=42)),
                ('picture', models.ImageField(blank=True, upload_to='addr-photos/')),
                ('follow', models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL)),
                ('itemPost', models.ManyToManyField(related_name='post', to='socialnetwork.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentpost',
            name='commentWhichPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='socialnetwork.Post'),
        ),
        migrations.AddField(
            model_name='commentpost',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
