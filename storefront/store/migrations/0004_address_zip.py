# Generated by Django 4.1.5 on 2023-01-04 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_add_slug_to_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
