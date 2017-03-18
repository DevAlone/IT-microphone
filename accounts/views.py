from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import UserForm, ProfileForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.views import Event


def index(request):
    return render(request, 'accounts/index.html')


def profile(request, username):
    # user = User.objects.get(username=username)
    user = get_object_or_404(User, username=username)
    events = Event.objects.filter(owner=user)

    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    events_list.paginator.low_bound = events_list.number - 5
    events_list.paginator.middle_bound = events_list.number + 5
    events_list.paginator.high_bound = events_list.paginator.num_pages - 2

    return render(request, 'accounts/profile.html', {
        'user': user,
        'events': events_list,
    })


@transaction.atomic
@login_required
def editProfile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES,
                                   instance=request.user.profile)
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
    if request.method == 'POST':
        username = request.POST['username']
        if username == 'admin' or username == 'moderator' or \
           username == 'administrator':
            return redirect(reverse('core:fakeAdmin'))

    return auth.views.login(request, template_name='accounts/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('core.index'))
