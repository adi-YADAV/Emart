# Generated by Django 5.0.4 on 2024-05-09 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0004_alter_product_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
    ]