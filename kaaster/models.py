from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        )
    first_name = models.TextField(max_length=500)
    last_name = models.TextField(max_length=500)
    birthday = models.DateField()
    gender = models.CharField(max_length=1, 
        choices=(('M', 'Male'), ('F', 'Female')), default='M')
    avatar = models.ImageField(upload_to='avatars/',
        default='images/avatars/no_avatar.jpg')

    def __unicode__(self):
        return u'{} @ {}'.format(self.first_name, self.last_name)