from django.shortcuts import render, get_object_or_404
from core.models import Event
from django.forms.models import model_to_dict
from .models import Chat
from django.contrib.auth.models import User
from django.http import JsonResponse


def getMessages(request, pk):
    chat = get_object_or_404(Chat, pk=pk)
    messages = list(chat.chatmessage_set.values(
        'author', 'text', 'pub_date', 'likes_count', 'dislikes_count'))

    for message in messages:
        message['author'] = model_to_dict(
            get_object_or_404(User, pk=message['author']),
            {'id', 'username', 'first_name'})

    data = {
        'count_messages': chat.count_messages,
        'messages': messages,
    }
    return JsonResponse(data)
