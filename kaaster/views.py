from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# FORMS
from kaaster.forms import UserLoginForm, UserRegisterForm, CreatePostForm
# Kaaster Models
from kaaster.models import Post, Tag, TagsInPost, Reply, TagsInReplies, UserProfile

# Class-Based Views
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView

# Mixins
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)

def index(request):
    context = {"user": "", "loggedin": False}
    print(request.user)
    if(request.user.is_authenticated()):
        print "Logged In"
        context["user"] = request.user
        context["loggedin"] = True
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
            User.objects.create(username=username, password=password, email=email)
            return redirect('index')
        else:
            context = {
                'form': form,
                'message': 'Something went wrong!'
            }
            return render(request, 'register.html', context)


# Post Views
# class CreatePostView(LoginRequiredMixin):
#     model = Post
#     form_class = CreatePostForm
#     template_name = 'create_post.html'
