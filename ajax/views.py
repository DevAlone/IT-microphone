from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from core.models import Event


def eventSubscribe(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        if not request.session.has_key('anonim_subscribed' + pk) or\
                not request.session['anonim_subscribed' + pk]:
            request.session['anonim_subscribed' + pk] = False
            event.anonymous_subscribers += 1
            event.save()

            request.session['anonim_subscribed' + pk] = True
            return HttpResponse("OK")



    return HttpResponse("NEOK")
    raise Http404()


def eventUnsubscribe(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'GET':
        if request.session.has_key('anonim_subscribed' + pk) and\
                request.session['anonim_subscribed' + pk]:
            if event.anonymous_subscribers > 1:
                event.anonymous_subscribers -= 1
            event.save()

            request.session['anonim_subscribed' + pk] = False
            return HttpResponse("OK")



    return HttpResponse("NEOK")
    raise Http404()
