from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

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


def eventDetail(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    #if not request.session['anonim_subscribed']:
    #    request.session['anonim_subscribed'] = True
    #    event.anonymous_subscribers += 1
    #    event.save() # здесь неплохо бы транзакцию сделать

    #subscribed = request.session['anonim_subscribed' + pk] if \
    #    'anonim_subscribed' + pk in request.session else False
    subscribed = event.isUserSubscribed()

    return HttpResponse(subscribed)
    return render(request, 'core/event_detail.html', {
        'event': event,
        'subscribed': subscribed
    })


def test(request):
    user = request.user
#    request.session['voted'] = True

    voted = request.session['voted'] = True

    return render(request, 'core/test.html', {
        'user': user,
        'voted': voted,
    })
