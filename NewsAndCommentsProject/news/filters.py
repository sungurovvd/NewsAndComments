from django_filters import FilterSet, BooleanFilter , ModelChoiceFilter, DateFilter
from .models import Post, Author, User, Category, Subscribers
from django import forms
import  datetime

class PostFilter(FilterSet):
    type_of_post = BooleanFilter(
        field_name = 'is_news',
        label = 'Новость',
        )
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(2015, cur_year)])

    category_name = ModelChoiceFilter(
        field_name = 'postcategory__category__name',
        label = 'Категория',
        queryset= Category.objects.all(),
        empty_label = 'Все категории'

    )

    time = DateFilter(
        field_name= 'create_time',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        lookup_expr='gt', label='Опубликовано после:'
    )

    class Meta:
        model = Post
        fields = {
            'article': ['icontains'],
        }

# class ChooseCategoryFilter(FilterSet):
#
#     category_name = ModelChoiceFilter(
#         field_name = 'subscribers_category_name',
#         label = 'Категория',
#         queryset= Category.objects.all(),
#         empty_label = 'Все категории'
#
#     )
#     class Meta:
#         model = Author
#         fields={
#             'name': ['icontains'],
#         }