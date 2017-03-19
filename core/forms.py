from django.forms import ModelForm, Textarea
from django import forms
from .models import Event


class EventForm(ModelForm):
    def clean(self):
        # cleaned_data =
        super(EventForm, self).clean()
        event_start_time = self.cleaned_data['event_start_time']
        event_end_time = self.cleaned_data['event_end_time']
        if event_start_time >= event_end_time:
            raise forms.ValidationError(
                "Дата начала не может быть больше или равна дате конца события")

    def save(self, commit=True):

        return super(EventForm, self).save(commit=commit)

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


class EventAddForm(EventForm):
    class Meta(EventForm.Meta):
        model = Event
        fields = ('theme', 'description', 'location', 'event_start_time',
                  'event_end_time', 'need_subscribers')


class EventEditForm(EventForm):
    class Meta(EventForm.Meta):
        model = Event
        # fields = ('theme', 'description', 'location', 'event_end_time',
        #          'need_subscribers'),
        widgets = {
            'theme': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
            'event_start_time': forms.DateTimeInput(
                attrs={'readonly': 'readonly'},
                format='%Y-%m-%d %H:%M'),
            'event_end_time': forms.DateTimeInput(
                attrs={'class': 'datepicker timepicker'},
                format='%Y-%m-%d %H:%M')
        }


