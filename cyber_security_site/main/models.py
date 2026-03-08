from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
