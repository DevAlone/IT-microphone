from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event
from .forms import EventAddForm, EventEditForm


def index(request):
    events = Event.objects.all().order_by('-event_start_time')

    subscribers = []
    for event in events:
        event.subscribed = False

    return render(request, 'core/index.html', {
        'events': events,
        'subscribers': subscribers
    })


def eventListView(request, category):
    if category == 'past':
        events = Event.objects.filter(event_end_time__lte=timezone.now())
    elif category == 'future':
        events = Event.objects.filter(event_start_time__gte=timezone.now())
    elif category == 'my':
        if not request.user.is_authenticated():
            raise Http404()
        events = Event.objects.filter(owner=request.user)
    else:
        events = Event.objects.all().order_by('-event_start_time')

    paginator = Paginator(events, 10)
    page = request.GET.get('page')
    try:
        events_list = paginator.page(page)
    except PageNotAnInteger:
        events_list = paginator.page(1)
    except EmptyPage:
        events_list = paginator.page(paginator.num_pages)

    return render(request, 'core/events_list.html', {
        'category': category,
        'events': events_list,
    })


def eventDetail(request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    event.subscribed = True

    return render(request, 'core/event_detail.html', {
        'event': event,
    })


@transaction.atomic
@login_required
def addEvent(request):
    if request.method == 'POST':
        form = EventAddForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)

            event.owner = request.user
            event.save()

            return HttpResponseRedirect(reverse('core:event_detail',
                                                kwargs={'pk': event.pk}))
    else:
        form = EventAddForm()

    return render(request, 'core/add_event.html', {'form': form})


@transaction.atomic
@login_required
def editEvent(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.owner:
        raise Http404()

    if request.method == 'POST':
        form = EventEditForm(request.POST)

        if form.is_valid():
            result = form.cleaned_data
            event.description = result['description']
            event.location = result['location']
            event.event_end_time = result['event_end_time']
            event.need_subscribers = result['need_subscribers']
            event.save()

            return HttpResponseRedirect(reverse('core:event_detail',
                                        kwargs={'pk': event.pk}))
    else:
        form = EventEditForm(initial={
            'theme': event.theme,
            'description': event.description,
            'location': event.location,
            'event_start_time': event.event_start_time,
            'event_end_time': event.event_end_time,
            'need_subscribers': event.need_subscribers,
        })

    return render(request, 'core/edit_event.html', {'form': form})
