from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from users.models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name","email","profile_picture")


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs.update({'class':'form-control'})
























# from django import forms
# from users.models import CustomUser
#
#
# class UserCreateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("username", "first_name", "last_name", "email", "password")
#
#     def save(self, commit=True):
#         user = super().save(commit=commit)
#         user.set_password(self.cleaned_data['password'])
#         user.save()
#
#         return user
