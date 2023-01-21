from django.urls import path
from .views import NewsList, PostList, NewsDelete, ArticleDelete, PostDetail,CreateNews, CreateArticles , ArticleList, NewsUpdate, ArticleUpdate #create_news,create_article


urlpatterns = [
   path('news/', NewsList.as_view(), name = 'news_list'),
   path('articles/', ArticleList.as_view(), name ='article_list'),
   path('news/<int:pk>', PostDetail.as_view(), name = 'news_detail'),
   path('articles/<int:pk>', PostDetail.as_view(), name = 'articles_detail'),
   path('news/create', CreateNews.as_view()),
   path('articles/create', CreateArticles.as_view()),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
   path('search/', PostList.as_view())
]