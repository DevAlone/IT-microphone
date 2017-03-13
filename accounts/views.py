from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'accounts/index.html')


def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', {'user': user})


@transaction.atomic
@login_required
def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(
                reverse('accounts:profile',
                        kwargs={'username': request.user.username}))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


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
