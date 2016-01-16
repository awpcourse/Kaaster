from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

# FORMS
from kaaster.forms import UserLoginForm, UserRegisterForm

def index(request):
    context = {}
    return render(request, 'index.html', context)


def login(request):
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


def logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)





