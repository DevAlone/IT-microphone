from django.forms import ModelForm, Textarea
from .models import ChatMessage


class ChatMessageAddForm(ModelForm):

    class Meta:
        model = ChatMessage
        fields = ('text', )
        widgets = {
            'text': Textarea(),
        }
