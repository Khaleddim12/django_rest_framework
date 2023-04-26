# Generated by Django 4.1.7 on 2023-04-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_app', '0002_product_delete_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/original'),
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='images/products/thumbnail'),
        ),
    ]