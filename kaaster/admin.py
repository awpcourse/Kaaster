from django.contrib import admin
from kaaster import models

admin.site.register(models.Post)
admin.site.register(models.UserProfile)
admin.site.register(models.Tag)
admin.site.register(models.TagsInPosts)
admin.site.register(models.Reply)
