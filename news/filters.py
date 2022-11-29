from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter,\
        DateTimeFromToRangeFilter, CharFilter, DateTimeFilter
from .models import Post, Category
from django_filters.widgets import DateRangeWidget, RangeWidget
from django.forms import DateTimeInput

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    category = ModelChoiceFilter( # фильтрация статей по категориям
        field_name="postcategory__categoryThrough",
        queryset=Category.objects.all(),
        label='Категории',
        empty_label='любая категория'
    )
    dateCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Период написания до:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
#    dateCreation = DateTimeFromToRangeFilter(# lookup_expr=('lt'),
#        widget=RangeWidget(attrs={'type': 'datetime-local'}),
#        label='Период написания',
#                                         )

    title = CharFilter(
        field_name='title',
        label='Заголовок содержит',
        lookup_expr='icontains'
    )

#    class PostFilter(FilterSet):
#        category = ModelMultipleChoiceFilter(  # фильтрация статей по категориям "или или"
#            field_name="postcategory__categoryThrough",
#            queryset=Category.objects.all(),
#            label='Категории',
#                    )

#class PostFilter(FilterSet):
#    category = ModelMultipleChoiceFilter(  # фильтрация статей по категориям оба критерия должны присутствовать
#        field_name="postcategory__categoryThrough",
#        queryset=Category.objects.all(),
#        label='Категории',
#        conjoined=True,
#        )

    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = {
           "author": ['exact'],
           # поиск по названию
#           'title': ['icontains'],
           # количество товаров должно быть больше или равно
#            'dateCreation': [
#                'gt',
#            ]

#            'rating': [
#                'lt',  # цена должна быть меньше или равна указанной
#                'gt',  # цена должна быть больше или равна указанной
#            ],
       }