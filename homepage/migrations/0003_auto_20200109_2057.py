# Generated by Django 3.0 on 2020-01-09 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20200107_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='content',
            field=models.TextField(),
        ),
    ]