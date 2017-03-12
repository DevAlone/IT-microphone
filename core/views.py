import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Event
from .forms import EventAddForm


def index(request):
    events = Event.objects.all().order_by('-event_start_time')

    subscribers = []
    for event in events:
        event.subscribed = request.session['anonim_subscribed' + \
            str(event.pk)] if 'anonim_subscribed' + str(event.pk) in \
            request.session else False

    return render(request, 'core/index.html', {
        'events': events,
        'subscribers': subscribers
    })


def eventListView(request, category):
    if category == 'past':
        events = Event.objects.filter(event_end_time__lte=timezone.now())
    elif category == 'future':
        events = Event.objects.filter(event_start_time__gte=timezone.now())
    else:
        events = Event.objects.all().order_by('-event_start_time')

    return render(request, 'core/events_list.html', {
        'category': category,
        'events': events,
    })


def eventDetail(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    event.subscribed = request.session['anonim_subscribed' + \
        str(event.pk)] if 'anonim_subscribed' + str(event.pk) in \
        request.session else False

    return render(request, 'core/event_detail.html', {
        'event': event,
    })


@login_required
def addEvent(request):
    if request.method == 'POST':
        form = EventAddForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)

            event.owner = request.user
            event.save()

            return HttpResponseRedirect(reverse('core:event_detail',
                                                kwargs={'pk':event.pk}))
    else:
        form = EventAddForm()

    return render(request, 'core/add_event.html', {'form': form})


def test(request):
    user = request.user
#    request.session['voted'] = True

    voted = request.session['voted'] = True

    return render(request, 'core/test.html', {
        'user': user,
        'voted': voted,
    })
