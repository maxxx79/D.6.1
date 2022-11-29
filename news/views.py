from django.shortcuts import render
from datetime import datetime
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from .models import Post, Author, Comment, Category, PostCategory, UserCategory, User
from pprint import pprint
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required # чтобы разрешить доступ к странице,
# которая доступна только для зарегистрированных пользователей
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView


@method_decorator(login_required, name='dispatch') # для примера, а так LoginRequiredMixin
class ProtectedView(TemplateView):
    template_name = 'prodected_page.html'


class AuthorList(LoginRequiredMixin, ListView):
    model = Author
    context_object_name = "Authors" # Переименовываем object_list в Authors
    #queryset = Author.objects.all() - тоже самое что и model = Author
    template_name = "news/authors.html"


class PostsList(LoginRequiredMixin, ListView):
    #queryset = Post.objects.filter(
    #    rating__lt=10
    #)
    #queryset = Post.objects.filter(
    #    rating__gt=10
    #).order_by(
    #   '-rating'
    #    )
    # Указываем модель, объекты которой мы будем выводить
    model = Post # MultipleObjectMixin
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation' # MultipleObjectMixin
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html' # TemplateResponseMixin
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'post_list' # MultipleObjectMixin
    paginate_by = 10 # количество записей на странице

    def get_queryset(self): # Переопределяем функцию получения списка товаров
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        #context['time_now'] = datetime.utcnow() # старое время
        # Добавим ещё одну пустую переменную,чтобы на её примере рассмотреть работу ещё одного фильтра.
        #context['next_sale'] = 'Проверка' # None
        #pprint(context)
        context['filterset'] = self.filterset
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post # SingleObjectMixin
    # Используем другой шаблон — product.html
    template_name = 'post.html' # TemplateResponseMixin
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post' # SingleObjectMixin
    # pk_url_kwarg = 'id'


#class Myform(FormView):
#    form_class = myform
#    success_url = '/success/'
#    def form_valid(self, form):
#        return super().form_valid(form)


#class PostCreate(CreateView):
#    model = Post
#    fields = "__all__"
#    success_url = '/'
#    template_name = 'post_edit.html'


class NewsCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.add_post',) # разрешение от group authors

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)


def post_create(request): # не активна
    form = PostForm()

    if request.method == "POST": # Проверка на запрос ( GET или POST )
        form = PostForm(request.POST) # инициализация формы
        if form.is_valid(): # Проверка на правильность заполнения формы

            form.save() # сохраняем
            return HttpResponseRedirect('/') # Направляем на страницу "/"

    return render(request, 'post_edit.html', {'form': form})


# Добавляем представление для изменения товара.
class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)


# Представление удаляющее товар.
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostsSearch(LoginRequiredMixin, ListView):
    model = Post # MultipleObjectMixin
    ordering = '-dateCreation' # MultipleObjectMixin
    template_name = 'post_search.html' # TemplateResponseMixin
    context_object_name = 'post_list' # MultipleObjectMixin
    paginate_by = 10 # количество записей на странице

    def get_queryset(self): # Переопределяем функцию получения списка товаров
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user_update.html'
    form_class = UserForm
    success_url = '/post/'

    def get_object(self, **kwargs):
        return self.request.user


class Userlist(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'uzer'
    template_name = 'user_list.html'


class CategoryDetail(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'postCategory'


class AddProduct(PermissionRequiredMixin, CreateView): # пример
    permission_required = ('shop.add_product', )
#    // customize form view