import json
from homepage.models import Category

with open('category.json') as f:
    template = json.load(f)

    for newCategory in template:
        newCategory = Category(
            name=newCategory['name'], slug=newCategory['slug'])
        newCategory.save()
