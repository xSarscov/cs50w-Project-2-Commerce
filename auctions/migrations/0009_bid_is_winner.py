# Generated by Django 5.0.1 on 2024-01-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]
