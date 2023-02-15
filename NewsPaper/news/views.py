from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Post


class ListPosts(ListView):
    model = Post
    template_name = 'post_news.html'
    context_object_name = 'post_news'


class DetailPosts(DetailView):
    model = Post
    template_name = 'post_new_detail.html'
    context_object_name = 'post_new'
