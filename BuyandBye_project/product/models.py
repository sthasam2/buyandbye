"""MODEL for the Products including Category and Subcategory"""
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField
from hitcount.models import HitCount
from PIL import Image

from .options import (
    CATEGORY_CHOICES,
    CONDITION_CHOICES,
    ITEM_CONTRACT_CHOICES,
    SUB_CATEGORY_CHOICES,
)


class Category(models.Model):
    """ Item Category Class"""

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from=["name"])
    image = models.ImageField(blank=True, null=True)
    illustration = models.ImageField(blank=True, null=True)
    icon = models.ImageField(blank=True, null=True)

    class Meta:
        """additional properties class"""

        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.get_name_display()

    def get_absolute_url(self):
        return reverse("category-detail", kwargs={"slug": self.slug})


class SubCategory(models.Model):
    """ SubCategory class"""

    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subname = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from=["subname"])
    image = models.ImageField(blank=True, null=True)
    illustration = models.ImageField(blank=True, null=True)
    icon = models.ImageField(blank=True, null=True)

    class Meta:
        """additional properties class"""

        # ordering = ('subname',)
        verbose_name = "Sub_Category"
        verbose_name_plural = "Sub_Categories"

    def __str__(self):
        # return self.subname returns the non human readable tuple
        return self.get_subname_display()  # returns human readable tuple


class Item(models.Model):
    """ Item class"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = MoneyField(decimal_places=2, max_digits=10, default_currency="NPR")
    content = models.TextField()
    image = models.ImageField(
        upload_to="item_pics/", blank=False, null=False
    )  # setting image
    image2 = models.ImageField(
        upload_to="item_pics/", blank=True, null=True
    )  # setting image
    image3 = models.ImageField(
        upload_to="item_pics/", blank=True, null=True
    )  # setting image
    image4 = models.ImageField(
        upload_to="item_pics/", blank=True, null=True
    )  # setting image
    image5 = models.ImageField(
        upload_to="item_pics/", blank=True, null=True
    )  # setting image
    image6 = models.ImageField(
        upload_to="item_pics/", blank=True, null=True
    )  # setting image
    condition = models.CharField(
        max_length=100, null=True, blank=True, choices=CONDITION_CHOICES
    )
    price_negotiability = models.BooleanField(default=False, blank=False)
    item_available_for = models.CharField(
        max_length=100, default="Sale", choices=ITEM_CONTRACT_CHOICES
    )
    sold = models.BooleanField(default=False)

    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field="object_pk",
        related_query_name="hit_count_generic_relation",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    slug = AutoSlugField(populate_from=["title"])

    # if image:
    #     def save(self, *args, **kwargs):
    #         # accessing parent class save function
    #         super(Item, self).save(*args, **kwargs)
    #         img = Image.open(self.image.path)
    #         if img.height > 3000 or img.width > 3000:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.image.path)  # overriding previous image

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={"slug": self.slug})
