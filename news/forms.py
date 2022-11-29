from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):
    # title = forms.CharField(min_length=20) - взамен проверки длинны названия

    class Meta:
        model = Post
        fields = [
           'author',
           #'categoryType',
           'postCategory',
           'title',
           'text',
           'rating',
       ]

    def clean_title(self): # clean_+ название поля, по которому проверяется
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return title

    def clean(self):
        cleaned_data = super().clean() # вызов метода clean() из родительского класса и сохранение в переменной
        title = cleaned_data.get("title")
        if title is not None and len(title) < 20:
            raise ValidationError({
                "title": "Заглавие не может быть менее 20 символов."
            })

        text = cleaned_data.get("text")
        if text == title:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


class UserForm(forms.ModelForm):
    """форма User BasicSignupForm типа"""
    username = forms.CharField(label='Юзиер')
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Почта")

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'date_joined',
            'is_staff'
        ]

    def save(self, commit=True):
        user = super(UserForm, self).save()
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print('Custom group works!!!!')
        return user


