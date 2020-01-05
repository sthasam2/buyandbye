from django.utils.text import slugify

# recursive function for slug creation because repitition  of same title can happen
def create_slug(instance, new_slug=None):
        # converts title into slug, e.g. Apple Iphone 7-> apple-iphone-7
    slug = slugify()
    if new_slug is not None:
        slug = new_slug
    # checking for multiple instances for same slug using queryset, because sometimes the item id may be same
    qs = Item.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        # for multiple occurence, defining a new slug
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    # defining the slug at given instance to the slugified one
    return slug
