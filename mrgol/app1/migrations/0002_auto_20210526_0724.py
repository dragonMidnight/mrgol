# Generated by Django 3.1.5 on 2021-05-26 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='filter_filter_attribute',
        ),
        migrations.AddField(
            model_name='product',
            name='filter_attributes',
            field=models.ManyToManyField(to='app1.Filter_Attribute', verbose_name='آيتم هاي فيلتر'),
        ),
    ]
