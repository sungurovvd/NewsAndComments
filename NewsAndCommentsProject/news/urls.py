from django.urls import path
from .views import Subs, CategoryDetail, NewsList, PostList, NewsDelete, ArticleDelete, PostDetail,CreateNews, CreateArticles , ArticleList, NewsUpdate, ArticleUpdate #create_news,create_article
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('news/', cache_page(60)(NewsList.as_view()), name = 'news_list'),
   path('articles/',cache_page(60)(ArticleList.as_view()), name ='article_list'),
   path('news/<int:pk>',cache_page(5*60)(PostDetail.as_view()), name = 'news_detail'),
   path('articles/<int:pk>', cache_page(5*60)(PostDetail.as_view()), name = 'articles_detail'),
   path('news/create', CreateNews.as_view()),
   path('articles/create', CreateArticles.as_view()),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
   path('search/', PostList.as_view()),
   path('subscribers/', Subs.as_view()),
   # path('subscribers/', CategoryList.as_view()),
   # path('subscribers/<int:pk>', CategoryDetail.as_view()),
   # path('subscribers/<int:pk>/sub', Subs.as_view(), name = 'subs')
]