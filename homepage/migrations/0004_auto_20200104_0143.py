# Generated by Django 3.0 on 2020-01-03 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20200104_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Real Estate', 'Real Estate'), ('Automobiles', 'Automobiles'), ('Furnitures', 'Furnitures'), ('Jobs', 'Jobs'), ('Computers', 'Computers'), ('Mobiles', 'Mobiles'), ('Books', 'Books'), ('Electronics', 'Electronics'), ('Cameras', 'Cameras'), ('Music Instruments', 'Music Instruments'), ('Pets', 'Pets'), ('Sports and Fitness', 'Sports and Fitness'), ('Services', 'Services'), ('Clothing', 'Clothing')], max_length=100),
        ),
    ]
