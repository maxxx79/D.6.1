from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum # Для: postRat = self.post_set.aggregate(postRating=Sum('rating'))
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE) # , verbose_name='Имя автора'
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self): # для вывода читаемой инфы
        return f'имя : {self.authorUser.username.title()}'

    def update_rating(self): # реализация через aggregate
        postRat = self.posts.aggregate(postRating=Sum('rating')) # Post связана через поле author, у нее поле rating
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribe = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'категория:{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class UserCategory(models.Model):
    """ Промежуточная модель для связи «многие ко многим» User и Category"""
    userThrough = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{user}: {category}'.format(user=self.userThrough, category=self.categoryThrough)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f' ЗАГОЛОК: {self.title};   ' \
               f' ДАТА ПУБЛИКАЦИИ: {self.dateCreation.strftime("%d-%m-%Y")}; '\
               f' ТЕКСТ: {self.text};  '\
               f' АВТОР: {self.author.authorUser};  '  \
               f' СТАТЬЯ/НОВОСТЬ: {self.categoryType}; ' \
               f' Категория: {self.postCategory.all().values("name")}; ' \
               f' Рейтинг: {self.rating}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)]) # возвращение на адрес 'post_detail' после ззполнения формы

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-dateCreation']

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        #return self.text[0:123] + '...'
        return f'Заголовок: {self.title} \n Статья: {self.text[:63]} ...'


class PostCategory(models.Model):
    """ Промежуточная модель для связи «многие ко многим» Post и Category """
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост в категории')
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
       # return f' {self.category_line}, Новость: {self.post_line}'
        return f'{self.categoryThrough.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f' Как отреагировали: {self.text.title()}, Кто написал: {self.commentUser.username}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Кометарий'
        verbose_name_plural = 'Коментарии'

