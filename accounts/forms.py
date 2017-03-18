from django import forms
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    middle_name = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('middle_name', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            width, height = get_image_dimensions(avatar)

            max_width = max_height = 500
            if width > max_width or height > max_height:
                raise forms.ValidationError(
                    'Слишком много пикселей. '
                    'Надо не больше %sx%s' % (max_width, max_height)
                )

            print(avatar.__dict__)
            main, sub = avatar.content_type.split('/')
            avatar._name = 'avatar.' + sub
            if not (main == 'image' and sub in ['jpeg', 'jpg', 'gif', 'png']):
                raise forms.ValidationError(
                    'Разрешённые файлы: .jpeg, .jpg, .png, .gif')

            if len(avatar) > (10 * 1024):
                raise forms.ValidationError(
                    'Слишком много байтов')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar
