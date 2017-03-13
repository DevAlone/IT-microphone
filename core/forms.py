from django.forms import ModelForm, Textarea
from django import forms
from .models import Event
import datetime

class EventAddForm(ModelForm):
    event_start_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'datepicker'
    }))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': 'timepicker'
    }))
    event_duration = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M',
                               attrs={'pattern':'[0-9]{1-2}:[0-9]{1-2}',
                                      'value': '00:00'}))

    def save(self, commit=True):

#        event_start_date = self.cleaned_data.get('event_start_date', None,)
#        start_time = self.cleaned_data.get('start_time', None)
#        event_duration = self.cleaned_data.get('event_duration', None)

        self.event_start_time = datetime.datetime.now()
#        self.event_start_time.date =
        #self.event_start_time = event_start_date + start_time
        #self.event_end_time = self.event_start_time + event_duration

        return super(EventAddForm, self).save(commit=commit)

    class Meta:
        model = Event
        fields = ('theme', 'description', 'location', 'event_start_date',
                  'start_time', 'event_duration', 'need_subscribers')
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
