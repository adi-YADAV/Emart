# Generated by Django 5.0.4 on 2024-05-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0003_product_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Mobile'), (2, 'Clothes'), (3, 'Footwear')], verbose_name='Category'),
        ),
    ]
