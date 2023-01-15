from django.urls import path
from .views import NewsList, PostDetail, create_news, NotNewsList, NewsUpdate


urlpatterns = [
   path('news/', NewsList.as_view()),
   path('articles/', NotNewsList.as_view()),
   path('news/<int:pk>', PostDetail.as_view(), name = 'post_detail'),
   path('news/create', create_news),
   path('news/<int:pk>/update/', NewsUpdate.as_view())
]