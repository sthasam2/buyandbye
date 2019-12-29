from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # one user one profile
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=150)
    country = CountryField()
    address = models.TextField()
    bio = models.TextField(max_length=200)
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics')  # setting image

    def __str__(self):
        return f'{self.user.username} Profile'

    # resize the images to 300x300 pixels
    def save(self):
        super().save()  # accessing parent class save function

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)  # overriding previous image
