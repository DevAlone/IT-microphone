from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event


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
    #if not request.session['anonim_subscribed']:
    #    request.session['anonim_subscribed'] = True
    #    event.anonymous_subscribers += 1
    #    event.save() # здесь неплохо бы транзакцию сделать

    #subscribed = request.session['anonim_subscribed' + pk] if \
    #    'anonim_subscribed' + pk in request.session else False
    event.subscribed = request.session['anonim_subscribed' + \
        str(event.pk)] if 'anonim_subscribed' + str(event.pk) in \
        request.session else False

    return render(request, 'core/event_detail.html', {
        'event': event,
    })

@login_required
def addEvent(request):

    return render(request, 'core/add_event.html')


def test(request):
    user = request.user
#    request.session['voted'] = True

    voted = request.session['voted'] = True

    return render(request, 'core/test.html', {
        'user': user,
        'voted': voted,
    })
