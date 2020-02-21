import json
from homepage.models import Category, SubCategory, Item

with open('.json/category.json') as f:
    template = json.load(f)

for newCategory in template:
    newCategory = Category(
        name=newCategory['name'], slug=newCategory['slug'])
    newCategory.save()

with open('.json/subcat.json') as f:
    template2 = json.load(f)

for new in template2:
    new = SubCategory(parent_category=Category.objects.get(
        name=new['parent_name']), subname=new['subname'])
    new.save()
