# Generated by Django 4.2.5 on 2023-10-21 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
    ]