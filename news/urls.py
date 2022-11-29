from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, AuthorList, post_create, \
   PostUpdate, PostDelete, PostsSearch, NewsCreate, ArticlesCreate, Userlist, UserUpdateView, CategoryDetail


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('authorlist/', AuthorList.as_view(), name='author_list'),
   #path('authorlist/', AuthorList.as_view(template_name="index.html")), можно как атрибут напрямую указывать template_name
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
#   path('create/', post_create, name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostsSearch.as_view(), name='post_search'),
   path('user/', Userlist.as_view(), name='user_list'),
   path('user_update/', UserUpdateView.as_view(), name='user_update'),
   path('category/', CategoryDetail.as_view(), name='category_detail'),
]
