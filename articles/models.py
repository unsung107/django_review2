from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.conf import settings

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    # article.user
    # user.articles
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')

    # article.liked_user.all()
    # user.liked_articles.all()
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')

    class Meta:
        ordering = ('-pk', )


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ('-pk', )

