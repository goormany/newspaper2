# Generated by Django 4.1.6 on 2023-02-21 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_postcategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]
