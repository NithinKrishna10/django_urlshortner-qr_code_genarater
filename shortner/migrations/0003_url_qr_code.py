# Generated by Django 4.2.1 on 2023-06-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortner', '0002_url_description_url_image_url_url_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
