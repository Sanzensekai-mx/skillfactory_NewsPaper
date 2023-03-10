from django.urls import path
from .views import ListPosts, DetailPosts, post_search, CreatePostView, UpdatePostView, DeletePostView, become_author

urlpatterns = [
    path('', ListPosts.as_view()),
    path('<int:pk>', DetailPosts.as_view()),
    path('search', post_search),
    path('add', CreatePostView.as_view(), name='add_post'),
    path('<int:pk>/edit', UpdatePostView.as_view(), name='update_post'),
    path('<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('be_author', become_author, name='be_author')
]
