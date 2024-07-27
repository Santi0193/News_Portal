from django.urls import path
from .views import (
    NewsCreateView, NewsUpdateView, NewsDeleteView,
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView,
    NewsListView, NewsDetailView, NewsSearchListView, SubscribeView
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsListView.as_view()), name='news_list'),
    path('<int:pk>/', cache_page(60 * 5)(NewsDetailView.as_view()), name='news_detail'),
    path('search/', NewsSearchListView.as_view(), name='news_search'),

    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),

    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),

    path('news/category/<int:category_id>/subscribe/', SubscribeView.as_view(), name='subscribe_to_category'),
]