from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    count_messages = models.IntegerField(default=0)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='chat_message_likes')
    dislikes = models.ManyToManyField(User,
                                      related_name='chat_message_dislikes')
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-pk', )
