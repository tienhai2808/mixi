# Generated by Django 5.1 on 2024-10-11 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_spiritual_alter_product_slug_product_spiritual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='spiritual',
        ),
        migrations.DeleteModel(
            name='Spiritual',
        ),
    ]
