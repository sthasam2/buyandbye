from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django_extensions.db.fields import AutoSlugField
from django.urls import reverse
from django.utils import timezone
from djmoney.models.fields import MoneyField
from PIL import Image

CATEGORY_CHOICES = (
    ('realestate', 'Real Estate'),
    ('automobiles', 'Automobiles'),
    ('furnitures', 'Furniture'),
    ('jobs', 'Jobs'),
    ('computer', 'Computer'),
    ('mobiles', 'Mobiles'),
    ('books', 'Books'),
    ('electronics', 'Electronics'),
    ('cameras', 'Cameras'),
    ('music Instruments', 'Music Instruments'),
    ('pets', 'Pets'),
    ('sportsandfitness', 'Sports and Fitness'),
    ('services', 'Services'),
    ('clothing', 'Clothing'),
)

# SUB_CATEGORY_CHOICES = (
#      ('Real Estate', 'Real Estate'),
#      ('Automobiles', 'Automobiles'),
#      ('Furniture', 'Furniture'),
#      ('Jobs', 'Jobs'),
#      ('Computer', 'Computer'),
#      ('Mobiles', 'Mobiles'),
#      ('Books', 'Books'),
#      ('Electronics', 'Electronics'),
#      ('Cameras', 'Cameras'),
#      ('Music Instruments', 'Music Instruments'),
#      ('Pets', 'Pets'),
#      ('Sports and Fitness', 'Sports and Fitness'),
#      ('Services', 'Services'),
#      ('Jobs', 'Jobs'),
#      ('Clothing', 'Clothing'),
# )


# category class
class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    slug = AutoSlugField(populate_from='name')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# sub-category class
# class Sub_Category(models.Model):
#     subname = models.CharField(max_length=100, choices=SUB_CATEGORY_CHOICES)
#     slug = AutoSlugField(populate_from='name')
#
#     class Meta:
#         ordering = ('subname',)
#         verbose_name = 'Sub_Category'
#         verbose_name_plural = 'Sub_Categories'
#
#     def __str__(self):
#         return self.name

# item class
class Item(models.Model):
    #category = models.ForeignKey(Category, required=False, on_delete=models.CASCADE, choices=CATEGORY_CHOICES)
    # sub_category= models.ForeignKey(Sub_Category, on_delete=models.CASCADE), choices=SUB_CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, default=None)
    date_posted = models.DateTimeField(default=timezone.now)
    price = MoneyField(decimal_places=2, max_digits=10,
                       default_currency='NPR')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='item_pics/')  # setting image

    def save(self, *args, **kwargs):
         # accessing parent class save function
         super(Item, self).save(*args, **kwargs)

         img = Image.open(self.image.path)
         if img.height > 300 or img.width > 300:
             output_size = (300, 300)
             img.thumbnail(output_size)
             img.save(self.image.path)  # overriding previous image

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})




# # recursive function for slug creation because repitition  of same title can happen
# def create_slug(instance, new_slug=None):
#         # converts title into slug, e.g. Apple Iphone 7-> apple-iphone-7
#     slug = slugify()
#     if new_slug is not None:
#         slug = new_slug
#     # checking for multiple instances for same slug using queryset, because sometimes the item id may be same
#     qs = Item.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         # for multiple occurence, defining a new slug
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     # defining the slug at given instance to the slugified one
#     return slug
