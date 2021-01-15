from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Category, Item, SubCategory
from recommender.utils import calculate_similarity


@receiver(post_save, sender=Item)
def item_receiver(sender, instance, *args, **kwargs):
    print("initiate calclationg cosine similarity")
    calculate_similarity()


"""
# / Item slug generator
@receiver(pre_save, sender=Item)
# since method is pre_save it constantly keeps on occuoring for every signal sent by item or something like that
def item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_item_slug(instance)


# recursive function for slug creation because repitition  of same title can happen
def create_item_slug(instance, new_slug=None):
    # converts title into slug, e.g. Apple Iphone 7-> apple-iphone-7
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    # checking for multiple instances for same slug using queryset, because sometimes the item id may be same
    qs = Item.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()

    if exists:
        # for multiple occurence, defining a new slug
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_item_slug(instance, new_slug=new_slug)
    # defining the slug at given instance to the slugified one
    return slug


pre_save.connect(item_receiver, sender=Item)
# / Item slug generator


# Category slug generator
@receiver(pre_save, sender=Category)
def item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_category_slug(instance)


def create_category_slug(instance, new_slug=None):
    slug = slugify(instance.name)

    if new_slug is not None:
        slug = new_slug

    qs = Category.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_category_slug(instance, new_slug=new_slug)

    return slug


pre_save.connect(item_receiver, sender=Category)
# / Category slug generator


# # SubCategory slug generator
@receiver(pre_save, sender=SubCategory)
def item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_subcategory_slug(instance)


def create_subcategory_slug(instance, new_slug=None):
    slug = slugify(instance.subname)

    if new_slug is not None:
        slug = new_slug

    qs = SubCategory.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_subcategory_slug(instance, new_slug=new_slug)

    return slug


pre_save.connect(item_receiver, sender=SubCategory)
# # / SubCategory slug generator


def create_slug(instance, new_slug=None):
    # converts title into slug, e.g. Apple Iphone 7-> apple-iphone-7
    # checking instance class since the slug to be made has different variable
    if instance.__name__ == 'Item':
        slug = slugify(instance.title)
        qs = Item.objects.filter(slug=slug).order_by("-id")

    elif instance.__name__ == 'Category':
        slug = slugify(instance.name)
        qs = Category.objects.filter(slug=slug).order_by("-id")

    elif instance.__name__ == 'SubCategory':
        slug = slugify(instance.subname)
        qs = SubCategory.objects.filter(slug=slug).order_by("-id")

    if new_slug is not None:
        slug = new_slug
    # checking for multiple instances for same slug using queryset, because sometimes the item id may be same

    exists = qs.exists()

    if exists:
        # for multiple occurence, defining a new slug
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    # defining the slug at given instance to the slugified one
    return slug
"""
