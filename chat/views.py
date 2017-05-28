import sys
from django.shortcuts import get_object_or_404
# from core.models import Event
from django.forms.models import model_to_dict
from .models import Chat, ChatMessage
from django.contrib.auth.models import User
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.csrf import csrf_protect


def getMessages(request, pk):
    offset = int(request.GET.get('offset', 0))
    count = int(request.GET.get('count', 50))
    chat = get_object_or_404(Chat, pk=pk)
    chat_messages = \
        ChatMessage.objects.filter(chat=chat).order_by('pk')[offset:offset+count]

    messages = list(chat_messages.values(
        'pk', 'author', 'text', 'pub_date', 'likes_count', 'dislikes_count'))

    for message in messages:
        message['author'] = model_to_dict(
            get_object_or_404(User, pk=message['author']),
            {'id', 'username', 'first_name'})

    data = {
        'count_messages': chat.count_messages,
        'messages': messages,
    }
    return JsonResponse(data)


@csrf_protect
@transaction.atomic
def messageVote(request, pk, action):
    if not request.user.is_authenticated:
        return JsonResponse({
            'state': False,
            'text': 'authentication is required',
        })
    message = get_object_or_404(ChatMessage, pk=pk)
    state = False
    text = ""
    print(pk)
    print(action)
    print()
    if action == str(1):
        if not message.likes.filter(pk=request.user.pk).exists():
            if message.dislikes.filter(pk=request.user.pk).exists():
                message.dislikes.remove(request.user)
                message.dislikes_count -= 1
            message.likes.add(request.user)
            message.likes_count += 1
            state = True
        else:
            text = 'Ты уже оценил комментарий'
    else:
        if not message.dislikes.filter(pk=request.user.pk).exists():
            if message.likes.filter(pk=request.user.pk).exists():
                message.likes.remove(request.user)
                message.likes_count -= 1
            message.dislikes.add(request.user)
            message.dislikes_count += 1
            state = True
        else:
            text = 'Ты уже оценил комментарий'

    message.save()
    data = {
        'state': state,
        'text': text,
        'likes_count': message.likes_count,
        'dislikes_count': message.dislikes_count,
    }

    return JsonResponse(data)


@csrf_protect
@transaction.atomic
def addMessage(request, pk):
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({
            'state': False,
            'text': 'необходима авторизация',
        })
    text = request.POST.get('text')
    if len(text) > 10000 or sys.getsizeof(text) > 40000:
        return JsonResponse({
            'state': False,
            'text': 'много букаф',
        })


    chat = get_object_or_404(Chat, pk=pk)
    message = ChatMessage(chat=chat, author=request.user, text=text)
    message.save()

    return JsonResponse({
        'state': True,
        'text': 'спасибо за комментарий',
        'chatMessage': {
            'chatId': chat.pk,
            'authorId': request.user.pk,
            'text': message.text,
            'pub_date': message.pub_date,
            'likes_count': message.likes_count,
            'dislikes_count': message.dislikes_count,
        }
    })
