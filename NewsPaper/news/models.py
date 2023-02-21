from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_raiting = models.BigIntegerField(default=0, verbose_name='Рэйтинг автора')

    def update_raiting(self):
        postRat = self.post_set.aggregate(postRating=Sum("raitingPost"))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set.aggregate(commentRating=Sum("raitingComment"))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.author_raiting = pRat*3 + cRat
        self.save()

    def __str__(self):
        return self.author_user.username

    class Meta:
        verbose_name = ('Автор')
        verbose_name_plural = ('Авторы')


class Category(models.Model):
    name_category = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")


class Post(models.Model):
    news = 'NW'
    articles = 'AR'
    POSITION = [
        (news, 'Новость'),
        (articles, 'Статья')
    ]

    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, default=news, choices=POSITION)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=128, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    raitingPost = models.SmallIntegerField(default=0, verbose_name='Рэйтинг поста')

    def __str__(self):
        return f"ID: {self.id}, title: {self.title}, Author: {self.author_post.author_user}"

    def preview_text(self):
        return f'{self.text[:20]}...'

    def like(self):
        self.raitingPost += 1
        self.save()

    def dislike(self):
        self.raitingPost -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    class Meta:
        verbose_name = ("Пост")
        verbose_name_plural = ("Посты")


class Comment(models.Model):
    text = models.CharField(max_length=128)
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост комментария')
    date_created = models.DateTimeField(auto_now_add=True)
    raitingComment = models.SmallIntegerField(default=0, verbose_name='Рэйтинг комментария')

    def like(self):
        self.raitingComment += 1
        self.save()

    def dislike(self):
        self.raitingComment -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions')