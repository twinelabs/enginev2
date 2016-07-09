from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ClientForm


def index(request):

    context = {}

    return render(request, 'welcome/index.html', context)


def register(request):
    # From: http://www.tangowithdjango.com/book17/chapters/login.html

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        client_form = ClientForm(data=request.POST)

        if user_form.is_valid() and client_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            registered = True

        else:
            print user_form.errors, client_form.errors

    else:
        user_form = UserForm()
        client_form = ClientForm()

    context = {'user_form': user_form, 'client_form': client_form, 'registered': registered}

    return render(request, 'welcome/register.html', context)


def user_login(request):
    # From: http://www.tangowithdjango.com/book17/chapters/login.html

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/welcome/')
        else:
            print "Username and password not found."
            return HttpResponse("Invalid login.")

    else:
        return render(request, 'welcome/login.html', {})


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/welcome/login/')
