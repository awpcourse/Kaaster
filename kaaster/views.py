from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError

# Kaaster Models
from kaaster.models import Post, Tag, TagsInPosts, Reply, TagsInReplies, UserProfile

# Class-Based Views
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView

# Forms
from kaaster.forms import UserLoginForm, CreatePostForm, UserPostForm, UserRegisterForm, \
            EditProfileForm

# Mixins
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

def index(request):
    context = {"user": ""}
    print(request.user)
    if(request.user.is_authenticated()):
        print "Logged In"
        context["user"] = request.user
        context["loggedin"] = True

        if request.method == 'GET':
            posts = Post.objects.all()
            print 'am luat un cacat'
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


# class PostDetailsView(LoginRequiredMixin, DetailView):
#     model = UserPost
#     template_name = 'post_details.html'
#     form_class = UserPostCommentForm

#     def get_context_data(self, **kwargs):
#         context = super(PostDetailsView, self).get_context_data(**kwargs)
#         context['form'] = self.form_class()
#         return context

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             text = form.cleaned_data['text']
#             user_comment = UserPostComment(text=text, author=request.user, post=self.get_object())
#             user_comment.save()
#         return redirect('post_details', pk=self.get_object().pk)

