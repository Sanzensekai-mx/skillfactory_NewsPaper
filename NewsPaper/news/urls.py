from django.urls import path
from .views import ListPosts, DetailPosts, post_search

urlpatterns = [
    path('', ListPosts.as_view()),
    path('<int:pk>', DetailPosts.as_view()),
    path('search', post_search)
]
