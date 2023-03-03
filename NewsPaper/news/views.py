from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post
from .filters import PostFilter


class ListPosts(ListView):
    model = Post
    template_name = 'post_news.html'
    context_object_name = 'post_news'
    queryset = Post.objects.order_by('-create_time')
    paginate_by = 10


class DetailPosts(DetailView):
    model = Post
    template_name = 'post_new_detail.html'
    context_object_name = 'post_new'


# class PostsSearch(ListView):
#     model = Post
#     template_name = 'news_search.html'
#     context_object_name = 'filter_post_news'
#     queryset = Post.objects.order_by('-create_time')
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
#         # filter_post = PostFilter(self.request.GET, queryset=self.get_queryset())
#         # context['filter'] = filter_post
#         # context['filter_values'] =
#         return context


# class PostsSearch(View):
#     def get(self, request):
#         posts_queryset = Post.objects.order_by('-create_time')
#         p = Paginator(posts_queryset, 10)
#         posts = p.get_page(request.GET.get('page', 1))
#         context = {
#             'filter_values'
#         }
#         return render(request, 'filter_post_news', context)
#
#     def post(self):

def post_search(request):
    post_list = Post.objects.order_by('-create_time')
    posts_filter = PostFilter(request.GET, queryset=post_list)
    post_list = posts_filter.qs

    paginator = Paginator(post_list, 10)
    # print(request.GET)
    # page_get = request.GET.dict()
    page = request.GET.get('page', 1)
    print(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'paginator': paginator,
        'filter': posts_filter,
        'filtered_posts': posts,
    }
    return render(request, 'news_search.html', context)
