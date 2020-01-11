from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone

from djmoney.models.fields import MoneyField
from markdownx.models import MarkdownxField
from PIL import Image

from . utils import create_slug
from . options import CATEGORY_CHOICES, SUB_CATEGORY_CHOICES, CONDITION_CHOICES


# category class
class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = models.SlugField(max_length=100)
    # parent = models.ForeignKey(self, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # def slugify_function(self, content):
    #     return content. replace('_', '-').lower()

    def __str__(self):
        return self.name


# sub - category class
class SubCategory(models.Model):
    subname = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES)
    slug = models.SlugField(max_length=100)
    parent_category = models.ForeignKey(
        Category, on_delete=django.db.models.deletion.CASCADE)

    class Meta:
        ordering = ('subname',)
        verbose_name = 'Sub_Category'
        verbose_name_plural = 'Sub_Categories'

    def __str__(self):
        return self.subname


# item class
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    price = MoneyField(decimal_places=2, max_digits=10,
                     default_currency='NPR')
    content = MarkdownxField()
    image = models.ImageField(upload_to='item_pics/')  # setting image
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES)

    slug=models.SlugField(max_length=100)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted=models.DateTimeField(default=timezone.now)

    if image:
        def save(self, *args, **kwargs):
            # accessing parent class save function
            super(Item, self).save(*args, **kwargs)

            img=Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size=(300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)  # overriding previous image

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})
