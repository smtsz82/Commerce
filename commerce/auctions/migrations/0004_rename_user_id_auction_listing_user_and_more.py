# Generated by Django 4.2.9 on 2024-02-07 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auction_listing_listing_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction_listing',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='auction_listing',
            name='listing_desc',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
