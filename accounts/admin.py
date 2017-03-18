from django.contrib import admin
from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileModelForm
    fieldset = [
        (None, {'fields': ['middle_name', 'avatar', ]}),
    ]

admin.site.register(Profile, ProfileAdmin)
