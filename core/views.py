from django.shortcuts import render, get_object_or_404

from .models import Event


def index(request):
    events = Event.objects.all().order_by('-event_start_time')

    return render(request, 'core/index.html', {
        'events': events
    })


def eventDetail(request, pk=None):
    event = get_object_or_404(Event, pk=pk)

    return render(request, 'core/event_detail.html', {
        'event': event
    })


def test(request):
    user = request.user

    return render(request, 'core/test.html', {
        'user': user
    })
