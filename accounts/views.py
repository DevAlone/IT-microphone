from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index(request):

    return render(request, 'accounts/index.html')


def profile(request):

    return render(request, 'accounts/profile.html')


@login_required
def editProfile(request):
    if request.method == 'GET':
        user = request.user
        return render(request, 'accounts/editProfile.html', {
            'user': user
        })

    raise Http404()


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts.logout'))
        return render(request, 'accounts/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active():
            auth.login(request, user)
            return HttpResponseRedirect(reverse('core.index'))
        return HttpResponseRedirect(reverse('accounts.login'))

    raise Http404()


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('core.index'))
