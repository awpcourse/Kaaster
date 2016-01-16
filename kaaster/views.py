from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
import re

# Kaaster Models
from kaaster.models import Post, Tag, TagsInPosts, Reply, TagsInReplies, UserProfile

# Class-Based Views
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView

# Forms
from kaaster.forms import UserLoginForm, CreatePostForm, UserRegisterForm, \
            EditProfileForm, CreatePostReplyForm

# Mixins
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

# def getProfile(post):

def index(request):
    context = {"user": ""}
    print(request.user)
    if(request.user.is_authenticated()):
        print "Logged In"
        context["user"] = request.user
        context["loggedin"] = True

        if request.method == 'GET':
            posts = Post.objects.all()
            # map(getProfile, posts)
            print 'Posts received'
            print posts
            context = {
                'posts': posts
            }
    else:
        print "Not logged in!"
    return render(request, 'index.html', context)


def loginview(request):
    if request.method == 'GET':
        form = UserLoginForm()
        context = {'form': form}
        print "OMG"
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                'form': form,
                'message': 'Wrong username or password!'
            }
            return render(request, 'login.html', context)
        else:
            login(request, user)
            return redirect('index')


def logoutview(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            user_auth = authenticate(username=username, password=password)
            if user_auth is None:
                return redirect('login')
            else:
                login(request, user_auth)
                profile = UserProfile.objects.create(user=user)
                profile.save()
                return redirect('user_profile', username=username)
        else:
            context = {'form': form}
            return render(request, 'register.html', context)


def user_profile(request, username):
    if request.method == 'GET':
        user = User.objects.filter(username=username)
        profile = UserProfile.objects.filter(user=user).first()
        context = {'profile': profile}
        return render(request, 'user_profile.html', context)


def edit_profile(request, username):
    if request.method == 'GET':
        form = EditProfileForm()
        context = {
            'form': form,
        }
        return render(request, 'edit_profile.html', context)
    elif request.method ==  'POST':
        form = EditProfileForm(request.POST, request.FILES)
        user = User.objects.filter(username=username).first()
        profile = UserProfile.objects.filter(user=user).first()

        if form.is_valid():
            if form.cleaned_data['first_name']:
                profile.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name']:
                profile.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['birthday']:
                profile.birthday = form.cleaned_data['birthday']
            if form.cleaned_data['gender']:
                profile.gender = form.cleaned_data['gender']
            if form['avatar'].value():
                profile.avatar = form['avatar'].value()
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
                user.save()
            profile.save()
        else:
            context = {'form': form}
            return render(request, 'edit_profile.html', context)
        return redirect('user_profile', username=username)

# Post Views
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['message', 'media']
    template_name = 'create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super(CreatePostView, self).form_valid(form)

    def get_success_url(self):
        # return reverse('index', kwargs={'pk': self.get_object().post.pk})
        post = Post.objects.get(pk=self.object.id)
        tags = re.findall(r'#\w+', post.message)
        for tagNameUnformated in tags:
            tagName = tagNameUnformated.replace('#', '')
            tag = Tag.objects.filter(name=tagName).first()
            if not tag:
                tag = Tag.objects.create(name=tagName)
                tag.save()
            
            tagsinpost = TagsInPosts.objects.create(tag=tag, post=post)
            tagsinpost.save()
        return reverse('index')

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['message', 'media']
    template_name = 'edit_post.html'

    def get_success_url(self):
        # return reverse('index', kwargs={'pk': self.get_object().post.pk})
        return reverse('index')

class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail_post.html'
    formPentruReply = CreatePostReplyForm

    def get_context_data(self, **args):
        context = super(DetailPostView, self).get_context_data(**args)
        context['replyForm'] = self.formPentruReply()
        context['replies'] = self.model.replies
        return context

    def post(self, request, *args, **kwargs):
        form = self.formPentruReply(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            user_reply = Reply(message=message, author=request.user, post=self.get_object())
            user_reply.save()
            
        return redirect('detail_post', pk=self.get_object().pk)

