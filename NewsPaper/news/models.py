from django.db import models
from django.contrib.auth.models import User

# Create your models here.

POST_TYPES = [
    ('AR', 'Статья'),
    ('NE', 'Новость')
]


class CommonLike:
    rate = 0

    def like(self):
        self.rate += 0.1

    def dislike(self):
        self.rate -= 0.1


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.FloatField(null=False)

    def update_rating(self):
        all_author_articles = Post.objects.filter(author__user=self.user).values('author__user__username', 'title', 'rate')
        all_author_comments = Comment.objects.filter(user=self.user).values('post__title', 'user__username', 'comment', 'rate')
        all_comments_under_author_posts = Comment.objects.filter(post__author__user=self.user).values('post__title', 'user__username', 'comment', 'rate')
        print(all_author_articles)
        print(all_author_comments)
        print(all_comments_under_author_posts)


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)


class Post(models.Model, CommonLike):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=POST_TYPES, default='NE')
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rate = models.FloatField(null=False, default=0.0)

    def preview(self):
        return f'{self.title}\n{self.content[:125]}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model, CommonLike):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField(null=False, default=0.0)
