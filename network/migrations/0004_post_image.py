# Generated by Django 3.2.7 on 2021-10-29 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_temp'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d/'),
        ),
    ]
