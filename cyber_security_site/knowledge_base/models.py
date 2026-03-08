from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

class Article(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
