# Generated by Django 3.2.7 on 2021-10-25 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='followers',
            field=models.ManyToManyField(blank=True, to='network.Author'),
        ),
    ]
