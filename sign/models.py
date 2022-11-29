from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import User, Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

    def save(self, commit=True):
        user = super(BaseRegisterForm, self).save()
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print('Custom group2 works!!!!')
        return user