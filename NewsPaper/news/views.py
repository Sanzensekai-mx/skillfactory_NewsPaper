from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib.auth.models import Group, User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post, Author, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm, UserUpdateForm


class ListPosts(ListView):
    model = Post
    template_name = 'post_news.html'
    context_object_name = 'post_news'
    queryset = Post.objects.order_by('-create_time')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class DetailPosts(DetailView):
    model = Post
    template_name = 'post_new_detail.html'
    context_object_name = 'post_new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('pk'))
        categories_id = list(PostCategory.objects.filter(post=post).values('category'))
        context['categories'] = [Category.objects.get(id=obj['category']).category for obj in categories_id]
        return context


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


class CreatePostView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    # model = Post
    template_name = 'add_new.html'
    form_class = PostForm
    initial = {
        'author': None
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    # def post(self, request, *args, **kwargs):
    #     context = super().post(request, **kwargs)
    #     author = Author.objects.get(user=request.user)
    #     self.form_class.author = author
    #     self.form_class.save(commit=False)
    #     # self.initial['author'] = author.id
    #     print(request.user)
    #     print(author.user.username)
    #     return context

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


class UpdatePostView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'add_new.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        get = super().get(self, request, *args, **kwargs)
        item = Post.objects.get(pk=self.kwargs.get('pk'))
        author = Author.objects.get(user=request.user)
        if not author == item.author and not author.user.is_superuser:
            return HttpResponseForbidden(f'?????? ?????????????? ?????? ???????????????????????????? ???????????? ???????????? {item.author.user.username}')
        return get

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class DeletePostView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'delete_new.html'
    context_object_name = 'post_to_del'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get(self, request, *args, **kwargs):
        get = super().get(self, request, *args, **kwargs)
        item = Post.objects.get(pk=self.kwargs.get('pk'))
        author = Author.objects.get(user=request.user)
        if not author == item.author and not author.user.is_superuser:
            return HttpResponseForbidden(f'?????? ?????????????? ?????? ???????????????? ???????????? ???????????? {item.author.user.username}')
        return get


class UpdateUserProfileView(UpdateView, LoginRequiredMixin):
    template_name = 'update_user_profile.html'
    form_class = UserUpdateForm

    def get_object(self, **kwargs):
        user = self.request.user
        return User.objects.get(pk=user.id)


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        Author.objects.create(user=user)
        author_group.user_set.add(user)
    return redirect('/news/')
