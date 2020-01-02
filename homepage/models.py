from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# class Category(models.Model):
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'
#
#     def __str__(self):
#         return self.title


class Item(models.Model):
    #category = models.ForeignKey(Category)
    title = models.CharField(max_length=100)
    # slug = models.SlugField(max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
