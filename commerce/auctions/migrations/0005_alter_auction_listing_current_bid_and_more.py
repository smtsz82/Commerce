# Generated by Django 4.2.9 on 2024-02-07 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_user_id_auction_listing_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='current_bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='initial_bid',
            field=models.FloatField(),
        ),
    ]
