from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

from . models import Item, Category, SubCategory


# / Item slug generator
@receiver(pre_save, sender=Item)
# since method is pre_save it constantly keeps on occuoring for every signal sent by item or something like that
def item_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)  # converts title into slug, e.g. Apple Iphone 7-> apple-iphone-7
    # checking for multiple instances for same slug using queryset, because sometimes the item id may be same
    exists = Item.objects.filter(slug=slug).exists()
    if exists:
        # for multiple occurence, defining a new slug
        slug = "%s-%s" % (slug, instance.id)
    # defining the slug at given instance to the slugified one
    instance.slug = slug


pre_save.connect(item_receiver, sender=Item)
# / Item slug generator


# Category slug generator
@receiver(pre_save, sender=Category)
def item_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    exists = Category.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" % (slug, instance.id)
    instance.slug = slug


pre_save.connect(item_receiver, sender=Category)
# / Category slug generator


# # SubCategory slug generator
@receiver(pre_save, sender=SubCategory)
def item_receiver(sender, instance, *args, **kwargs):
    slug = slugify(instance.subname)
    exists = SubCategory.objects.filter(slug=slug).exists()
    if exists:
        slug = "%s-%s" % (slug, instance.id)
    instance.slug = slug


pre_save.connect(item_receiver, sender=SubCategory)
# # / SubCategory slug generator
