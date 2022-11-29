from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import BaseRegisterForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):

    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required # кнопка хочу быть автором
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/') # после нажатия 'хочу быть автором' преходит в.....