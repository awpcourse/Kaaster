from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# Kaaster Models
from kaaster.models import Post, Tag, TagsInPost, Reply, TagsInReplies, UserProfile

# Class-Based Views
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView

# Forms
from kaaster.forms import UserLoginForm, CreatePostForm

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


# Post Views
# class CreatePostView(LoginRequiredMixin):
#     model = Post
#     form_class = CreatePostForm
#     template_name = 'create_post.html'
