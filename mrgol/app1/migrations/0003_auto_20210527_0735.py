# Generated by Django 3.1.5 on 2021-05-27 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20210526_0724'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='filter_attributes',
            new_name='filters_attributes',
        ),
    ]
