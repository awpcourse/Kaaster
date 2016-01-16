"""kaaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from kaaster import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
	url(r'^login/$', views.loginview, name='login'),
	url(r'^logout/$', views.logoutview, name='logout'),
    url(r'^post/create/$', views.CreatePostView.as_view(), name='create_post'),
    url(r'^post/edit/(?P<pk>\d+)/$', views.EditPostView.as_view(), name='edit_post'),
    url(r'^user_profile/(?P<username>[A-Za-z0-9]+)/$', views.user_profile, name='user_profile'),
    url(r'^profile/edit/(?P<username>[A-Za-z0-9]+)/$', views.edit_profile, name='edit_profile'),
    url(r'^post/(?P<pk>\d+)/$', views.DetailPostView.as_view(), name='detail_post'),
    url(r'^register/$', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
