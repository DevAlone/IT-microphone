from django.forms import ModelForm, Textarea
from django import forms
from .models import Event


class EventAddForm(ModelForm):
    def clean(self):
        cleaned_data = super(EventAddForm, self).clean()
        event_start_time = self.cleaned_data['event_start_time']
        event_end_time = self.cleaned_data['event_end_time']
        if event_start_time >= event_end_time:
            raise forms.ValidationError(
                "Дата начала не может быть больше или равна дате конца события")

    def save(self, commit=True):

        return super(EventAddForm, self).save(commit=commit)

    class Meta:
        model = Event
        fields = ('theme', 'description', 'location', 'event_start_time',
                  'event_end_time', 'need_subscribers')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
            'event_start_time': forms.DateTimeInput(
                attrs={'class': 'datepicker timepicker'},
                format='%Y-%m-%d %H:%M'),
            'event_end_time': forms.DateTimeInput(
                attrs={'class': 'datepicker timepicker'},
                format='%Y-%m-%d %H:%M')
        }
