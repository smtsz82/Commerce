# Generated by Django 4.2.9 on 2024-02-07 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auction_listing_listing_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='listing_desc',
            field=models.CharField(max_length=1000),
        ),
    ]
