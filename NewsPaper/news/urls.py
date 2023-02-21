from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsCreate, ArticlesCreate, NewsUpdate, ArticlesUpdate, \
    NewsDelete, ArticlesDelete, subscriptions

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('create/', ArticlesCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('subscriptions/', subscriptions, name='subscriptions')
]
