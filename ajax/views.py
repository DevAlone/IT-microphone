from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.db import transaction
from core.models import Event


@transaction.atomic
def eventSetSubscribeState(request, pk, state):
    if not request.user.is_authenticated():
        return HttpResponse("Необходима авторизация")

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        if state:
            event.subscribers.add(request.user)
            # event.subscribers_count += 1
        else:
            event.subscribers.remove(request.user)
            # event.subscribers_count -= 1

        event.save()
        return HttpResponse("OK")
    else:
        raise Http404()

    return HttpResponse("something bad happened")


def eventSubscribe(request, pk):
    return eventSetSubscribeState(request, pk, True)


def eventUnsubscribe(request, pk=None):
    return eventSetSubscribeState(request, pk, False)
