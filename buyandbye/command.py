import json
from product.models import Category, SubCategory, Item
# from djnago.contrib.auth.models import User

with open('.json/category.json') as f:
    template = json.load(f)

for newCategory in template:
    newCategory = Category(name=newCategory['name'])
    newCategory.save()

with open('.json/subcat.json') as f:
    template2 = json.load(f)

for new in template2:
    new = SubCategory(parent_category=Category.objects.get(
        name=new['parent_name']), subname=new['subname'])
    new.save()


# NOTE: error opening 
# with open('.json/items.json') as f:
#     template3 = json.load(f)

# for new in template3:
#     new = Item(category=Category.objects.get(
#         name=new['category']), sub_category=SubCategory.objects.get(subname=new['sub_category']), title=new['title'], price=new['price'], content=new['content'], image=new['image'], condition=new['condition'], item_available_for=new['item_available_for'], author=new['author'], date_posted=new['date_posted'])
#     new.save()
