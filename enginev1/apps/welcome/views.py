from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView

from .forms import UserForm, ClientForm
from .models import Client


# TODO: require login before client update

class ClientUpdate(UpdateView):
    """ Page to update client data attributes.
    """
    model = Client
    fields = ['company_name', 'first_name', 'last_name', 'logo']
    template_name = 'welcome/settings.html'
    success_url = '/welcome/home'


def register(request):
    """ Registers new client (user object one-to-one with client object).
    """

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        client_form = ClientForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and client_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            login(request, user)

        else:
            print user_form.errors, client_form.errors

        return HttpResponseRedirect('/welcome/home')

    else:
        user_form = UserForm()
        client_form = ClientForm()

    context = {
        'user_form': user_form,
        'client_form': client_form
    }

    return render(request, 'welcome/register.html', context)


def user_login(request):
    """ Client login page.
    """

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/welcome/home')
        else:
            print "Username and password not found."
            return HttpResponse("Invalid login.")

    else:
        return render(request, 'welcome/login.html', {})


@login_required
def home(request):
    """ Home page.
    """

    c = request.user.client
    data_tables = c.datatable_set.all()
    matches = c.match_set.all()

    context = {
        'c': c,
        'data_tables': data_tables,
        'matches': matches
    }

    return render(request, 'welcome/home.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/welcome/login/')
