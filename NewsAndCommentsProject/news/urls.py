from django.urls import path
from .views import NewsList, NewsDelete, ArticleDelete, PostDetail, create_news,create_article, ArticleList, NewsUpdate, ArticleUpdate


urlpatterns = [
   path('news/', NewsList.as_view(), name = 'news_list'),
   path('articles/', ArticleList.as_view(), name ='article_list'),
   path('news/<int:pk>', PostDetail.as_view(), name = 'news_detail'),
   path('articles/<int:pk>', PostDetail.as_view(), name = 'articles_detail'),
   path('news/create', create_news),
   path('articles/create', create_article),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
]