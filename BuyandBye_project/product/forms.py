from django import forms
from djmoney.forms.fields import MoneyField

from activity.utils import create_action

from .models import Category, Item, SubCategory
from .options import CATEGORY_CHOICES, YEARS


class ItemCreateForm(forms.ModelForm):
    image = forms.ImageField(
        label="Item Image 1", required=True, help_text="Choose images to upload"
    )
    image2 = forms.ImageField(
        label="Item Image 2", required=False, help_text="Choose images to upload"
    )
    image3 = forms.ImageField(
        label="Item Image 3", required=False, help_text="Choose images to upload"
    )
    image4 = forms.ImageField(
        label="Item Image 4", required=False, help_text="Choose images to upload"
    )
    image5 = forms.ImageField(
        label="Item Image 5", required=False, help_text="Choose images to upload"
    )
    image6 = forms.ImageField(
        label="Item Image 6", required=False, help_text="Choose images to upload"
    )

    class Meta:
        model = Item
        fields = [
            "category",
            "sub_category",
            "title",
            "price",
            "price_negotiability",
            "item_available_for",
            "condition",
            "content",
            "image",
            "image2",
            "image3",
            "image4",
            "image5",
            "image6",
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["sub_category"].queryset = SubCategory.objects.none()

            if "category" in self.data:
                try:
                    category_id = int(self.data.get("category"))
                    self.fields["sub_category"].queryset = SubCategory.objects.filter(
                        category_id=category_id
                    ).order_by("subname")
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty SubCat queryset
            elif self.instance.pk:
                self.fields[
                    "sub_category"
                ].queryset = self.instance.category.sub_category_set.order_by("name")


# class AdvancedSearchForm(forms.Form):
#     title_as = forms.CharField(max_length=200)
#     price_as = MoneyField(decimal_places=2, max_digits=10,
#                           default_currency='NPR',)
#     category_as = forms.CharField(
#         widget=forms.Select(choices=CATEGORY_CHOICES))
#     date_published_as = forms.DateField(
#         widget=forms.SelectDateWidget(years=YEARS))

#     class Meta:
#         # model = Item
#         fields = [
#             'title_as',
#             'price_as',
#             'category_as',
#             'date_published_as'
#         ]
