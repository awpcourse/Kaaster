# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-16 10:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(max_length=500)),
                ('media', models.ImageField(blank=True, null=True, upload_to=b'images/media')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=500)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='kaaster.Post')),
            ],
            options={
                'ordering': ['date_added'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('popularity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TagsInPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaaster.Tag')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaaster.Post')),
            ],
        ),
        migrations.CreateModel(
            name='TagsInReplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaaster.Reply')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kaaster.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=500)),
                ('last_name', models.TextField(max_length=500)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1)),
                ('avatar', models.ImageField(default=b'images/avatars/no_avatar.jpg', upload_to=b'images/avatars/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
