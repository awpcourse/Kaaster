from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

class Post(models.Model):
	author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = 'posts',
        )

	date_added = models.DateTimeField(auto_now_add=True)
	message = models.TextField(max_length=500)
	media = models.ImageField(upload_to='images/media')
	tags_ids = [] 

	def __unicode__(self):
        return u'{} @ {}'.format(self.author, self.date_added)

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    first_name = models.TextField(max_length=500)
    last_name = models.TextField(max_length=500)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, 
        choices=(('M', 'Male'), ('F', 'Female')), default='M')
    avatar = models.ImageField(upload_to='images/avatars/',
        default='images/avatars/no_avatar.jpg')

    class Meta:
        ordering = ['date_added']

    def __unicode__(self):
        return u'{} @ {}'.format(self.first_name, self.last_name)

class Tag(models.Model):
	name = models.TextField(max_length=50)
	popularity = models.IntegerField()

class TagsIntPosts(models.Model):
	tag = models.ForeignKey(
		Post,
		on_delete = models.CASCADE,
		)

	post = models.ForeignKey(
		Tag,
		on_delete = models.CASCADE,
		)


class Reply(models.Model):
    message = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='replies',)

    class Meta:
        ordering = ['date_added']

    def __unicode__(self):
        return u'{} @ {}'.format(self.author, self.date_added)


class TagsInReplies(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE,)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

