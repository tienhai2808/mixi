# Generated by Django 5.1 on 2024-10-11 10:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_spiritual_delete_spiritual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='element',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.element'),
        ),
    ]
